from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__, template_folder="templates")


def get_data(req):
    con = sqlite3.connect('db/persons.sqlite')
    cur = con.cursor()
    res = cur.execute(req).fetchall()
    con.close()
    colums = ['id', 'name', 'bio', 'photo', 'status']
    return [dict(zip(colums, r)) for r in res]


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'GET':
        res = get_data("""SELECT * FROM persons""")
        return render_template('index.html', persons=res)
    elif request.method == 'POST':
        search = request.form['search']
        res = get_data(f"""SELECT * FROM persons WHERE name LIKE '%{search}%' OR bio LIKE '%{search}%'""")
        return render_template('index.html', persons=res)


@app.route('/add', methods=['POST', 'GET'])
def add_pers():
    if request.method == 'GET':
        return render_template('add.html')
    elif request.method == 'POST':
        name, status, bio = request.form['name'], request.form['status'], request.form['bio']
        file = request.files['file']
        file.save(f"static/img/{file.filename}")
        con = sqlite3.connect('db/persons.sqlite')
        cur = con.cursor()
        res = cur.execute(f"""INSERT INTO persons VALUES (NULL, '{name}', '{bio}', '{file.filename}', '{status}');""")
        con.commit()
        con.close()
        return "Форма отправлена"


@app.route('/teachers', methods=['POST', 'GET'])
def show_teachers():
    if request.method == 'GET':
        res = get_data("""SELECT * FROM persons WHERE status = 'преподаватель'""")
        return render_template('teachers.html', persons=res)
    elif request.method == 'POST':
        search = request.form['search']
        res = get_data(
            f"""SELECT * FROM persons WHERE (name LIKE '%{search}%' OR bio LIKE '%{search}%') AND status = 'преподаватель'""")
        return render_template('teachers.html', persons=res)


@app.route('/students', methods=['POST', 'GET'])
def show_students():
    if request.method == 'GET':
        res = get_data("""SELECT * FROM persons WHERE status = 'студент'""")
        return render_template('students.html', persons=res)
    elif request.method == 'POST':
        search = request.form['search']
        res = get_data(
            f"""SELECT * FROM persons WHERE (name LIKE '%{search}%' OR bio LIKE '%{search}%') AND status = 'студент'""")
        return render_template('students.html', persons=res)


if __name__ == '__main__':
    ip = '0.0.0.0'
    app.run()
