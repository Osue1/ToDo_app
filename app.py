from flask import Flask, render_template, request, redirect, session, url_for, flash
from db_manager import DatabaseManager

app = Flask(__name__)
app.secret_key = "my_super_secret_key_12345"
db = DatabaseManager() # DatabaseManagerクラスのインスタンス化

###########################################################################################
#                                   ログイン・ログアウト
###########################################################################################
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username").strip()
        password = request.form.get("password")
        if not username or not password:
            flash("ユーザー名とパスワードを入力してください")
            return redirect("/login")

        # 既存ユーザー取得
        user = db.get_user_by_name(username)
        if not user:
            # 新規登録（必ず User オブジェクトを返す）
            user = db.add_user(username, password)
            flash("新規ユーザー登録しました")
        else:
            # パスワード認証
            if user.password != password:
                flash("パスワードが違います")
                return redirect("/login")

        if not user:
            flash("ユーザー登録に失敗しました")
            return redirect("/login")

        session["user_id"] = user.id
        session["username"] = user.username
        return redirect("/")

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()  # セッション情報を削除
    flash("ログアウトしました")
    return redirect("/login")

###########################################################################################
###########################################################################################
# メイン画面
@app.route("/", methods=["GET", "POST"])
def index():
    user_id = session.get("user_id")
    if not user_id:
        flash("ログインしてください")
        return redirect("/login")  # ログイン画面にリダイレクト
    
    username = session.get("username")
    
    if request.method == "POST":
        title = request.form.get("title")
        if title:
            db.add_task(user_id, title)
        return redirect("/")
    
    tasks = db.get_tasks_by_user(user_id)
    return render_template("index.html", tasks=tasks, username=username)

# タスク完了状態切り替え
@app.route("/toggle/<int:task_id>")
def toggle(task_id):
    user_id = session.get("user_id")
    tasks = db.get_tasks_by_user(user_id)  # 自分のタスクのみ取得
    for t in tasks:
        if t.id == task_id:
            t.toggle()
            db.update_task(task_id, t.done)
            break
    return redirect("/")

# タスク削除
@app.route("/delete/<int:task_id>")
def delete(task_id):
    db.delete_task(task_id)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)

