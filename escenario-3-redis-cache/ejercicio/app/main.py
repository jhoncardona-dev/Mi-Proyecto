import json
import os
import time
from typing import Optional

import psycopg2
import redis
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr

app = FastAPI(title="App FastAPI + Redis + PostgreSQL")

REDIS_HOST = os.environ.get("REDIS_HOST", "redis")
REDIS_PORT = int(os.environ.get("REDIS_PORT", 6379))
RATE_LIMIT = int(os.environ.get("RATE_LIMIT", 10))
CACHE_TTL = int(os.environ.get("CACHE_TTL", 60))

redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    decode_responses=True,
)


def get_db_connection():
    return psycopg2.connect(
        host=os.environ.get("DB_HOST", "db"),
        port=int(os.environ.get("DB_PORT", 5432)),
        user=os.environ.get("DB_USER", "postgres"),
        password=os.environ.get("DB_PASSWORD", "postgres"),
        database=os.environ.get("DB_NAME", "cachedb"),
    )


class UsuarioCreate(BaseModel):
    nombre: str
    email: EmailStr


def check_rate_limit(client_ip: str) -> None:
    key = f"rate_limit:{client_ip}"
    current = redis_client.get(key)
    if current is None:
        redis_client.setex(key, 60, 1)
        return
    if int(current) >= RATE_LIMIT:
        raise HTTPException(
            status_code=429,
            detail=f"Rate limit excedido: máximo {RATE_LIMIT} requests por minuto",
        )
    redis_client.incr(key)


@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    client_ip = request.client.host if request.client else "unknown"
    try:
        check_rate_limit(client_ip)
    except HTTPException as exc:
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})
    return await call_next(request)


@app.get("/")
def index():
    return {"servicio": "FastAPI + Redis + PostgreSQL", "status": "activo"}


@app.get("/health")
def health():
    try:
        redis_ok = redis_client.ping()
    except Exception:
        redis_ok = False
    try:
        conn = get_db_connection()
        conn.close()
        db_ok = True
    except Exception:
        db_ok = False
    status = "healthy" if redis_ok and db_ok else "degraded"
    return {"status": status, "redis": redis_ok, "postgres": db_ok}


@app.get("/contador")
def contador():
    visitas = redis_client.incr("visitas_totales")
    return {"visitas": visitas}


def obtener_datos_lentos():
    time.sleep(2)
    return {"mensaje": "Datos procesados", "timestamp": time.time()}


@app.get("/datos")
def obtener_datos():
    cache_key = "datos_cache"
    cached = redis_client.get(cache_key)
    if cached:
        return {
            "origen": "cache",
            "datos": json.loads(cached),
            "ttl_restante": redis_client.ttl(cache_key),
        }
    datos = obtener_datos_lentos()
    redis_client.setex(cache_key, CACHE_TTL, json.dumps(datos))
    return {"origen": "base_de_datos", "datos": datos, "cacheado_por": f"{CACHE_TTL} segundos"}


@app.get("/usuarios")
def listar_usuarios():
    cache_key = "usuarios:all"
    cached = redis_client.get(cache_key)
    if cached:
        return {"origen": "cache", "usuarios": json.loads(cached)}

    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id, nombre, email FROM usuarios ORDER BY id")
            rows = [{"id": r[0], "nombre": r[1], "email": r[2]} for r in cur.fetchall()]
        redis_client.setex(cache_key, CACHE_TTL, json.dumps(rows))
        return {"origen": "postgres", "usuarios": rows}
    finally:
        conn.close()


@app.post("/usuarios", status_code=201)
def crear_usuario(usuario: UsuarioCreate):
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO usuarios (nombre, email) VALUES (%s, %s) RETURNING id, nombre, email",
                (usuario.nombre, usuario.email),
            )
            row = cur.fetchone()
            conn.commit()
        redis_client.delete("usuarios:all")
        return {"id": row[0], "nombre": row[1], "email": row[2]}
    except Exception as exc:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    finally:
        conn.close()


@app.get("/cache/estadisticas")
def estadisticas_cache():
    info = redis_client.info()
    return {
        "keys_totales": redis_client.dbsize(),
        "memoria_usada": info.get("used_memory_human"),
        "hits": info.get("keyspace_hits"),
        "misses": info.get("keyspace_misses"),
    }


@app.delete("/cache/limpiar")
def limpiar_cache():
    redis_client.flushdb()
    return {"mensaje": "Caché limpiada exitosamente"}
