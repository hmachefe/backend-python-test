from alayatodo import app, user_dao
from flask import (
    redirect,
    render_template,
    jsonify, request,
    session, flash
    )
from flask_paginate import Pagination, get_page_args

# main route that leads to root directory
@app.route('/')
def home():
    with app.open_resource('../README.md', mode='r') as f:
        readme = "".join(l.decode('utf-8') for l in f)
        return render_template('index.html', readme=readme)


# route that drives users to authentication page for new session
@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')


# authentication route that checks requests for username/password
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


# route by which users exit: sessions terminate
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('user', None)
    return redirect('/')


# route by which task is described by HTML content
@app.route('/todo/<id>', methods=['GET'])
def todo(id):
    todo = user_dao.find_description_by_id(id)
    return render_template('todo.html', todo=todo)


# route by which task is detailed in JSON format
@app.route('/todo/<id>/json', methods=['GET'])
def todo_json(id):
    todo = user_dao.find_description_by_id(id)
    return jsonify(id=todo['id'], user_id=todo['user_id'], description=todo['description'])


# route by which tasks are listed page by page
@app.route('/todo', methods=['GET'])
@app.route('/todo/', methods=['GET'])
def todos():
    if not session.get('logged_in'):
        return redirect('/login')
    page, per_page, offset = get_page_args()
    lenA, todosA = user_dao.find_all_description(offset, per_page)
    pagination = get_pagination(page=page,
                                per_page=per_page,
                                total=lenA,
                                record_name='todos',
                                format_total=True,
                                format_number=True,
                                )
    return render_template('todos.html', todos=todosA,
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           )

# route by which new task is entered and stored
@app.route('/todo', methods=['POST'])
@app.route('/todo/', methods=['POST'])
def todos_POST():
    if not session.get('logged_in'):
        return redirect('/login')
    user = session['user']['id']
    description = request.form.get('description', '')
    if (description != '') and (len(description.strip()) != 0):
        flash("description added")
        user_dao.insert_description(user, description, 0)
    else:
        print "empty description is not granted. User shall fill in desc with relevant content"

    return redirect('/todo')


# route by which known task is destroyed
@app.route('/todo/<id>', methods=['POST'])
def todo_delete(id):
    if not session.get('logged_in'):
        return redirect('/login')
    flash("description deleted")
    user_dao.delete_description(id)
    return redirect('/todo')


# route by which known task has been achieved
@app.route('/todo/complete/<id>', methods=['POST'])
def todo_complete(id):
    if not session.get('logged_in'):
        return redirect('/login')
    flash("description completed")
    user_dao.complete_description(id)
    return redirect('/todo')

# Helpers used by pagination
def get_css_framework():
    return app.config.get('CSS_FRAMEWORK', 'bootstrap3')

def get_link_size():
    return app.config.get('LINK_SIZE', 'sm')

def show_single_page_or_not():
    return app.config.get('SHOW_SINGLE_PAGE', False)

def get_pagination(**kwargs):
    kwargs.setdefault('record_name', 'records')
    return Pagination(css_framework=get_css_framework(),
                      link_size=get_link_size(),
                      show_single_page=show_single_page_or_not(),
                      **kwargs
                      )