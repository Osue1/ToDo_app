from flask import Flask, render_template, request, redirect, session, url_for, flash
from db_manager import DatabaseManager

app = Flask(__name__)
app.secret_key = "my_super_secret_key_12345"
db = DatabaseManager()

###########################################################################################
#                                   ログイン・ログアウト
###########################################################################################
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username").strip()
        if not username:
            flash("ユーザー名を入力してください")
            return redirect("/login")

        # 既存ユーザー取得
        user = db.get_user_by_name(username)
        if not user:
            # 新規登録（必ず User オブジェクトを返す）
            user = db.add_user(username)
        
        if not user:
            # ここはほぼ通らないはず
            flash("ユーザー登録に失敗しました")
            return redirect("/login")

        # ログイン成功
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

@app.route("/toggle/<int:task_id>")
def toggle(task_id):
    tasks = db.get_all_tasks()
    for t in tasks:
        if t.id == task_id:
            t.toggle()
            db.update_task(task_id, t.done)
            break
    return redirect("/")

@app.route("/delete/<int:task_id>")
def delete(task_id):
    db.delete_task(task_id)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
