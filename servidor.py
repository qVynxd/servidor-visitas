from flask import Flask, request, jsonify
import psycopg2
import os

app = Flask(__name__)

# --------------------------------
# CONEXIÓN A POSTGRESQL (RENDER)
# --------------------------------

def get_connection():
    return psycopg2.connect(
        os.environ["DATABASE_URL"],
        sslmode="require"
    )

# --------------------------------
# CREAR TABLA SI NO EXISTE
# --------------------------------

def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS registros (
            id SERIAL PRIMARY KEY,
            equipo TEXT,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    cur.close()
    conn.close()

init_db()

# --------------------------------
# RUTA PRINCIPAL
# --------------------------------

@app.route("/")
def home():
    return "Servidor funcionando correctamente 🚀"

# --------------------------------
# REGISTRO DE APERTURA
# --------------------------------

@app.route("/registro", methods=["POST"])
def registro():
    data = request.get_json()
    equipo = data.get("equipo", "desconocido")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO registros (equipo) VALUES (%s)",
        (equipo,)
    )

    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"status": "ok"})

# --------------------------------
# TOTAL DE REGISTROS
# --------------------------------

@app.route("/total")
def total():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM registros")
    total = cur.fetchone()[0]

    cur.close()
    conn.close()

    return jsonify({"total": total})

# --------------------------------
# ARRANQUE (RENDER)
# --------------------------------

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
