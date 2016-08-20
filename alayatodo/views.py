from alayatodo import app, user_dao
from flask import (
    redirect,
    render_template,
    request,
    session
    )


@app.route('/')
def home():
    with app.open_resource('../README.md', mode='r') as f:
        readme = "".join(l.decode('utf-8') for l in f)
        return render_template('index.html', readme=readme)


@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login_POST():
    username = request.form.get('username')
    password = request.form.get('password')

    user = user_dao.find_user(username, password)
    if user:
        session['user'] = dict(user)
        session['logged_in'] = True
        return redirect('/todo')

    return redirect('/login')


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('user', None)
    return redirect('/')


@app.route('/todo/<id>', methods=['GET'])
def todo(id):
    todo = user_dao.findDescriptionById(id)
    return render_template('find_description_by_id.html', todo=todo)


@app.route('/todo', methods=['GET'])
@app.route('/todo/', methods=['GET'])
def todos():
    if not session.get('logged_in'):
        return redirect('/login')
    todos = user_dao.find_all_description()
    return render_template('todos.html', todos=todos)


@app.route('/todo', methods=['POST'])
@app.route('/todo/', methods=['POST'])
def todos_POST():
    if not session.get('logged_in'):
        return redirect('/login')
    user = session['user']['id']
    description = request.form.get('description', '')
    if (description != '') and (len(description.strip()) != 0):
        user_dao.insert_description(user, description, 0)
    else:
        print "empty description is not granted. User shall fill in desc with relevant content"

    return redirect('/todo')


@app.route('/todo/<id>', methods=['POST'])
def todo_delete(id):
    if not session.get('logged_in'):
        return redirect('/login')
    user_dao.delete_description(id)
    return redirect('/todo')

@app.route('/todo/complete/<id>', methods=['POST'])
def todo_complete(id):
    if not session.get('logged_in'):
        return redirect('/login')
    user_dao.complete_description(id)
    return redirect('/todo')