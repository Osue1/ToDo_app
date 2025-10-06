import sqlite3
from task import Task
from user import User

class DatabaseManager:
    # データベース初期化
    def __init__(self, db_name="tasks.db"):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.create_table()

    # テーブル作成
    def create_table(self):
        cur = self.conn.cursor()
        # ユーザーテーブル
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL
            )
        """)
        # タスクテーブル
        cur.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                done INTEGER DEFAULT 0,
                created_at TEXT DEFAULT (DATETIME('now','localtime')),
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        """)
        self.conn.commit()


    # タスク追加
    def add_task(self, user_id, title):
        cur = self.conn.cursor()
        cur.execute(
            "INSERT INTO tasks (user_id, title, done) VALUES (?, ?, 0)",
            (user_id, title)
        )
        self.conn.commit()

    # 全タスク取得
    def get_tasks_by_user(self, user_id):
        cur = self.conn.cursor()
        cur.execute("SELECT id, title, done, created_at FROM tasks WHERE user_id=? ORDER BY done ASC, created_at DESC", (user_id,))
        rows = cur.fetchall()
        return [Task(id=row[0], title=row[1], done=bool(row[2]), created_at=row[3]) for row in rows]
    
    # タスク更新
    def update_task(self, task_id, done):
        cur = self.conn.cursor()
        cur.execute("UPDATE tasks SET done=? WHERE id=?", (int(done), task_id))
        self.conn.commit()

    # タスク削除
    def delete_task(self, task_id):
        cur = self.conn.cursor()
        cur.execute("DELETE FROM tasks WHERE id=?", (task_id,))
        self.conn.commit()

    # ユーザー名からユーザー情報を取得
    def get_user_by_name(self, username):
        cur = self.conn.cursor()
        cur.execute("SELECT id, username FROM users WHERE username=?", (username,))
        row = cur.fetchone()
        if row:
            return User(id=row[0], username=row[1])
        return None
    
    # 新規ユーザー登録
    def add_user(self, username):
        cur = self.conn.cursor()
        try:
            cur.execute("INSERT INTO users (username) VALUES (?)", (username,))
            self.conn.commit()
        except sqlite3.IntegrityError:
            # すでに同じ username が存在しても OK
            pass
        # 必ずユーザーオブジェクトを返す
        return self.get_user_by_name(username)


