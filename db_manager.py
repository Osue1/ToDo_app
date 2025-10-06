import sqlite3
from task import Task

class DatabaseManager:
    # データベース初期化
    def __init__(self, db_name="tasks.db"):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.create_table()

    # テーブル作成
    def create_table(self):
        cur = self.conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                done INTEGER DEFAULT 0,
                created_at TEXT DEFAULT (DATETIME('now','localtime'))
            )
        """)
        self.conn.commit()


    # タスク追加
    def add_task(self, title):
        cur = self.conn.cursor()
        cur.execute("INSERT INTO tasks (title, done) VALUES (?, 0)", (title,))
        self.conn.commit()

    # 全タスク取得
    def get_all_tasks(self):
        cur = self.conn.cursor()
        cur.execute("""
            SELECT id, title, done, created_at
            FROM tasks
            ORDER BY done ASC, created_at DESC
        """)
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
