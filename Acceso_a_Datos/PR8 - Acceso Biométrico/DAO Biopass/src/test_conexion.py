from src.conexion_db import DBConnection

if __name__ == "__main__":
    conn = DBConnection.get_connection()
    with conn.cursor() as cur: # with gestiona el cursor automáticamente y lo cierra al terminar
        cur.execute("SELECT 1;") # . Sirve para decirle a la base de datos: "¿Estás ahí? Devuélveme un 1"
        resultado = cur.fetchone() # métod para recoger ese "1"
    print("✅ Conexión y consulta OK:", resultado)
