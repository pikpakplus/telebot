import sqlite3


class Database:
    def __init__(self, db_name="apllication.db"):
        self.db_name = db_name
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
            self._init_tables()
            print(f"Соединение с базой данных {self.db_name} успешно установлено.")
        except sqlite3.Error as e:
            print(f"Ошибка при подключении к базе данных: {e}")

    def _init_tables(self):
        try:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS reviews (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    contact TEXT,
                    visit_date DATE,
                    rate INTEGER CHECK(rate BETWEEN 1 AND 5),
                    extra_comments TEXT
                )
            """)
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS book (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    year INTEGER CHECK(year > 0),
                    author TEXT,
                    genre TEXT,
                    price INTEGER CHECK(price >= 0)
                )
            """)
            self.conn.commit()
            print("Таблицы успешно созданы или уже существуют.")
        except sqlite3.Error as e:
            print(f"Ошибка при создании таблиц: {e}")

    def save_review(self, name, contact, visit_date, rate, extra_comments):
        try:
            self.cursor.execute("""
                INSERT INTO reviews (name, contact, visit_date, rate, extra_comments)
                VALUES (?, ?, ?, ?, ?)
            """, (name, contact, visit_date, rate, extra_comments))
            self.conn.commit()
            print("Отзыв успешно сохранен.")
        except sqlite3.Error as e:
            print(f"Ошибка при сохранении отзыва: {e}")

    def save_book(self, name, year, author, genre, price):
        try:
            self.cursor.execute("""
                INSERT INTO book (name, year, author, genre, price)
                VALUES (?, ?, ?, ?, ?)
            """, (name, year, author, genre, price))
            self.conn.commit()
            print("Книга успешно добавлена.")
        except sqlite3.Error as e:
            print(f"Ошибка при добавлении книги: {e}")

    def get_reviews(self):
        try:
            self.cursor.execute("SELECT * FROM reviews")
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Ошибка при получении отзывов: {e}")

    def get_books(self):
        """Получение всех книг"""
        try:
            self.cursor.execute("SELECT * FROM book")
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Ошибка при получении книг: {e}")

    def close(self):
        try:
            self.conn.close()
            print("Соединение с базой данных закрыто.")
        except sqlite3.Error as e:
            print(f"Ошибка при закрытии соединения: {e}")


if __name__ == "__main__":
    db = Database()

    db.save_review("Иван Иванов", "ivan@example.com", "2024-01-29", 5, "Отлично!")

    db.save_book("Война и мир", 1869, "Лев Толстой", "Роман", 1200)

    print("Отзывы:", db.get_reviews())

    print("Книги:", db.get_books())

    db.close()
