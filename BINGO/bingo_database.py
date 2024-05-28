import sqlite3

class BingoDatabase:
    def __init__(self, db_name):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()

    def create_tables(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Usuarios (
                                    id INTEGER PRIMARY KEY,
                                    nombre TEXT UNIQUE,
                                    creditos INTEGER
                                )''')
        self.connection.commit()

    def insert_usuario(self, nombre, creditos):
        try:
            self.cursor.execute('''INSERT INTO Usuarios (nombre, creditos)
                                   VALUES (?, ?)''', (nombre, creditos))
            self.connection.commit()
            print("Usuario insertado correctamente.")
        except sqlite3.IntegrityError:
            print("El usuario ya existe en la base de datos.")

    def update_creditos(self, nombre, nuevos_creditos):
        self.cursor.execute('''UPDATE Usuarios
                               SET creditos = ?
                               WHERE nombre = ?''', (nuevos_creditos, nombre))
        self.connection.commit()
        print("Créditos actualizados correctamente.")

    def close_connection(self):
        self.connection.close()

# pa crear la base y las tablas
if __name__ == "__main__":
    db = BingoDatabase("bingo.db")
    db.create_tables()
    db.close_connection()