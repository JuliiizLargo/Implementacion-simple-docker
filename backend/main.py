from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pymysql
import os
import time

app = FastAPI(title="Gestor de Tareas con R/W Split")

# ---------------- CORS ----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- MODELO ----------------
class Task(BaseModel):
    id: int | None = None
    title: str
    description: str | None = None

# ---------------- CONEXIONES ----------------
def connect_primary():
    try:
        return pymysql.connect(
            host=os.getenv("PRIMARY_DB_HOST", "gestor-db-primary"),
            port=int(os.getenv("PRIMARY_DB_PORT", 3306)),
            user=os.getenv("PRIMARY_DB_USER", "admin"),
            password=os.getenv("PRIMARY_DB_PASS", "admin123"),
            database=os.getenv("PRIMARY_DB_NAME", "tasks_db"),
            cursorclass=pymysql.cursors.DictCursor
        )
    except:
        raise HTTPException(status_code=500, detail="No se pudo conectar con la base de datos primaria")


def connect_replica():
    try:
        return pymysql.connect(
            host=os.getenv("REPLICA_DB_HOST", "gestor-db-replica"),
            port=int(os.getenv("REPLICA_DB_PORT", 3306)),
            user=os.getenv("REPLICA_DB_USER", "admin"),
            password=os.getenv("REPLICA_DB_PASS", "admin123"),
            database=os.getenv("REPLICA_DB_NAME", "tasks_db"),
            cursorclass=pymysql.cursors.DictCursor
        )
    except:
        raise HTTPException(status_code=500, detail="No se pudo conectar con la base de datos réplica")

# ---------------- INICIALIZACIÓN ----------------
@app.on_event("startup")
def init_db():
    conn = connect_primary()
    with conn.cursor() as cur:
        cur.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            description TEXT NULL
        );
        """)
    conn.commit() #Guarda los datos en la base de datos
    conn.close()
    print("Tabla tasks verificada.")

# ---------------- RUTAS ----------------

@app.get("/")
def root():
    return {"message": "API del Gestor de Tareas activa"}

# ---------- LISTAR ----------
@app.get("/tasks")
def list_tasks():
    print("READ: REPLICA")
    try:
        start = time.time()
        conn = connect_replica()
        with conn.cursor() as cur:
            cur.execute("SELECT id, title, description FROM tasks ORDER BY id ASC;")
            data = cur.fetchall()
        elapsed = (time.time() - start) * 1000
        print(f"[GET] Lectura réplica: {elapsed:.2f} ms")
        return data

    except Exception as e:
        print("❌ Error leyendo desde la réplica:", str(e))
        raise HTTPException(status_code=500, detail="Error al cargar tareas (réplica caída)")

    finally:
        try:
            conn.close()
        except:
            pass

# ---------- CREAR ----------
@app.post("/tasks")
def create_task(task: Task):
    print("WRITE: PRIMARY")
    try:
        start = time.time()
        conn = connect_primary()
        with conn.cursor() as cur:
            cur.execute("INSERT INTO tasks (title, description) VALUES (%s, %s);",
                        (task.title, task.description))
            conn.commit()
            task.id = cur.lastrowid

        elapsed = (time.time() - start) * 1000
        print(f"[POST] Insertado en {elapsed:.2f} ms")

        # Verificar sincronización
        synced = False
        while not synced:
            try:
                conn_r = connect_replica()
                with conn_r.cursor() as cur_r:
                    cur_r.execute("SELECT id FROM tasks WHERE id=%s;", (task.id,))
                    synced = cur_r.fetchone() is not None
                conn_r.close()
            except:
                break

        return {"message": "creado", "task": task}

    except Exception as e:
        print("❌ Error al insertar:", str(e))
        raise HTTPException(status_code=500, detail="Error al crear tarea (primaria caída)")

    finally:
        try:
            conn.close()
        except:
            pass

# ---------- ACTUALIZAR ----------
@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: Task):
    print("WRITE: PRIMARY")
    try:
        conn = connect_primary()
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE tasks SET title=%s, description=%s WHERE id=%s;",
                (task.title, task.description, task_id)
            )
            conn.commit()

        print(f"[PUT] Actualizado ID {task_id}")
        return {"message": "actualizado"}

    except Exception as e:
        print("❌ Error UPDATE:", str(e))
        raise HTTPException(status_code=500, detail="Error al actualizar (primaria caída)")

    finally:
        try:
            conn.close()
        except:
            pass

# ---------- ELIMINAR ----------
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    print("WRITE: PRIMARY")
    try:
        conn = connect_primary()
        with conn.cursor() as cur:
            cur.execute("DELETE FROM tasks WHERE id=%s;", (task_id,))
            conn.commit()

        print(f"[DELETE] Eliminado ID {task_id}")
        return {"message": "eliminado"}

    except Exception as e:
        print("❌ Error DELETE:", str(e))
        raise HTTPException(status_code=500, detail="Error al eliminar (primaria caída)")

    finally:
        try:
            conn.close()
        except:
            pass
