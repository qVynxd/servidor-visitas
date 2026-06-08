from flask import Flask, request
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)

# --------------------------------
# RUTA FIJA A LA BASE DE DATOS
# --------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "datos.db")

# --------------------------------
# CREAR BASE DE DATOS SI NO EXISTE
# --------------------------------

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS aperturas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        equipo TEXT,
        fecha TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()

# --------------------------------
# RECIBIR REGISTRO DEL .EXE
# --------------------------------

@app.route("/registro", methods=["POST"])
def registro():

    datos = request.json

    equipo = datos.get("equipo")
    fecha = datetime.now().isoformat()

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute(
        "INSERT INTO aperturas (equipo, fecha) VALUES (?, ?)",
        (equipo, fecha)
    )

    conn.commit()
    conn.close()

    print("✔ Registro recibido:", equipo, fecha)

    return {"ok": True}

# --------------------------------
# VER TOTAL DE APERTURAS
# --------------------------------

@app.route("/total")
def total():

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("SELECT COUNT(*) FROM aperturas")
    total = c.fetchone()[0]

    conn.close()

    print("📊 Consultando total:", total)

    return {"total": total}

# --------------------------------
# PÁGINA PRINCIPAL (OPCIONAL)
# --------------------------------

@app.route("/")
def home():
    return "Servidor funcionando correctamente 🚀"

# --------------------------------
# INICIAR SERVIDOR
# --------------------------------

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)