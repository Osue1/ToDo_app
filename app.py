from flask import Flask, render_template, request, redirect
from db_manager import DatabaseManager

app = Flask(__name__)
db = DatabaseManager()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        title = request.form.get("title")
        if title:
            db.add_task(title)
        return redirect("/")
    tasks = db.get_all_tasks()
    return render_template("index.html", tasks=tasks)

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
