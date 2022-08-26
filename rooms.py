from flask import Flask, redirect, url_for, render_template, request

from flaskext.mysql import MySQL

app = Flask(__name__)

mysql = MySQL()
app.config["MYSQL_DATABASE_HOST"] = "172.17.0.2"
app.config["MYSQL_DATABASE_USER"] = "app"
app.config["MYSQL_DATABASE_PASSWORD"] = "sql_pass"
app.config["MYSQL_DATABASE_DB"] = "MyDB"
mysql.init_app(app)


@app.route("/<id>", methods=["GET", "POST"])
def home(id):
    return render_template("index.html")


@app.route("/api/chat/<id>", methods=["POST", "GET"])
def api_chat(id):
    conn = mysql.connect()
    cur = conn.cursor()
    if request.method == "GET":
        cur.execute(f"SELECT * FROM chat_table WHERE room_id={id}")
        data = cur.fetchall()
        chat_history = [f"({record[1]}): {record[2]}" for record in data]
        if not chat_history:
            chat_history.append("EMPTY HISTORY")
        return "\n".join(chat_history)
    if request.method == "POST":
        username = request.form.get("username")
        message = request.form.get("msg")
        cur.execute(
            f'INSERT INTO chat_table (room_id, username, message) VALUES ({id}, "{username}", "{message}")'
        )
        conn.commit()
        return f"{message}"


if __name__ == "__main__":
    app.run()
