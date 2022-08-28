from flask import Flask, redirect, url_for, render_template, request
import datetime

from flaskext.mysql import MySQL

app = Flask(__name__)

mysql = MySQL()
app.config["MYSQL_DATABASE_HOST"] = "172.27.0.3"
app.config["MYSQL_DATABASE_USER"] = "app"
app.config["MYSQL_DATABASE_PASSWORD"] = "pass"
app.config["MYSQL_DATABASE_DB"] = "chat_db"
mysql.init_app(app)


@app.route("/<id>", methods=["GET"])
def home(id):
    return render_template("index.html")


@app.route("/api/chat/<id>", methods=["POST", "GET"])
def api_chat(id):
    conn = mysql.connect()
    cur = conn.cursor()

    if request.method == "GET":
        cur.execute(f"SELECT * FROM chat WHERE ID={id}")
        data = cur.fetchall()
        chat_history = [f"[{record[3]}] {record[1]}: {record[2]}" for record in data]
        if not chat_history:
            chat_history.append("EMPTY HISTORY")
        return "\n".join(chat_history)

    if request.method == "POST":
        username = request.form.get("username")
        message = request.form.get("msg")
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
        cur.execute(
            f"INSERT INTO chat (ID,username,message,date) VALUES ('{id}','{username}','{message}','{date}');"
        )
        conn.commit()
        return f'{message}'


if __name__ == "__main__":
    app.run()
