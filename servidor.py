from flask import Flask, request, jsonify
import psycopg2
import os

app = Flask(__name__)

# --------------------------------
# CONEXIÓN A POSTGRESQL
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
# PÁGINA PRINCIPAL
# --------------------------------

@app.route("/")
def home():
    return "Servidor funcionando correctamente 🚀"

# --------------------------------
# REGISTRO DE APERTURAS
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

    print("✔ Registro recibido:", equipo)

    return jsonify({"ok": True})

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
# INFORMACIÓN DE LA BASE
# --------------------------------

@app.route("/db-info")
def db_info():

    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("SELECT current_database();")
        database = cur.fetchone()[0]

        cur.close()
        conn.close()

        return jsonify({
            "database": database
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        })

# --------------------------------
# DEPURACIÓN
# --------------------------------

@app.route("/debug")
def debug():

    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("SELECT COUNT(*) FROM registros")
        total = cur.fetchone()[0]

        cur.execute("""
            SELECT id, equipo, fecha
            FROM registros
            ORDER BY id DESC
            LIMIT 10
        """)

        filas = cur.fetchall()

        cur.close()
        conn.close()

        return jsonify({
            "total": total,
            "ultimos_registros": [
                {
                    "id": f[0],
                    "equipo": f[1],
                    "fecha": str(f[2])
                }
                for f in filas
            ]
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        })

# --------------------------------
# ARRANQUE
# --------------------------------

if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port
    )
