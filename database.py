import sqlite3
import json
import csv
import logging

class BaseDatosGIC:
    """Manejo de la persistencia de datos en SQLite, JSON y CSV."""
    
    def __init__(self, db_name="gic_database.db"):
        self.db_name = db_name
        self._crear_tablas()

    def _conectar(self):
        return sqlite3.connect(self.db_name)

    def _crear_tablas(self):
        """Crea la tabla de clientes si no existe en la BD."""
        with self._conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS clientes (
                    id_cliente TEXT PRIMARY KEY,
                    nombre TEXT NOT NULL,
                    email TEXT NOT NULL,
                    telefono TEXT NOT NULL,
                    tipo TEXT NOT NULL,
                    extra TEXT
                )
            """)
            conn.commit()

    def guardar_cliente(self, cliente, tipo, extra=""):
        """Inserta o actualiza un cliente en SQLite."""
        with self._conectar() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT OR REPLACE INTO clientes VALUES (?, ?, ?, ?, ?, ?)",
                (cliente.id_cliente, cliente.nombre, cliente.email, cliente.telefono, tipo, extra)
            )
            conn.commit()
            logging.info(f"Cliente con ID {cliente.id_cliente} guardado/actualizado en SQLite.")

    def eliminar_cliente(self, id_cliente):
        """Elimina un cliente de SQLite por su ID."""
        with self._conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM clientes WHERE id_cliente = ?", (id_cliente,))
            conn.commit()
            logging.info(f"Cliente con ID {id_cliente} eliminado de SQLite.")

    def obtener_todos(self):
        """Recupera todos los registros almacenados en la base de datos."""
        with self._conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM clientes")
            return cursor.fetchall()

    def exportar_json(self, filepath="clientes.json"):
        """Exporta la lista de clientes a un archivo JSON."""
        datos = self.obtener_todos()
        lista = [
            {"id": d[0], "nombre": d[1], "email": d[2], "telefono": d[3], "tipo": d[4], "extra": d[5]} 
            for d in datos
        ]
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(lista, f, indent=4, ensure_ascii=False)
        logging.info("Datos exportados exitosamente a archivo JSON.")

    def exportar_csv(self, filepath="clientes.csv"):
        """Exporta la lista de clientes a un archivo CSV."""
        datos = self.obtener_todos()
        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["ID", "Nombre", "Email", "Telefono", "Tipo", "Extra"])
            writer.writerows(datos)
        logging.info("Datos exportados exitosamente a archivo CSV.")