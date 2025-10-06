class Task:
    # クラス初期化
    def __init__(self, id, title, done=False, created_at=None):
        self.id = id
        self.title = title
        self.done = done
        self.created_at = created_at

    # タスク完了状態を切り替え
    def toggle(self):
        self.done = not self.done
