from flask import ( g )

class UserDao:
    """main class wrapping users and descriptions into SQL requests"""

    def find_user(self, username, password):
        """retrieve user from database by authentication params"""
    	sql = "SELECT * FROM users WHERE username = '%s' AND password = '%s'";
    	cur = g.db.execute(sql % (username, password))
    	user = cur.fetchone()
        cur.close()
    	return user

    def find_description_by_id(self, id):
        """retrieve any task from sqlite database by its identifier"""
    	cur = g.db.execute("SELECT * FROM todos WHERE id ='%s'" % id)
    	todo = cur.fetchone()
        cur.close()
    	return todo

    def find_all_description(self, offset, per_page):
        """retrieve every tasks from database and count them all"""
        cur = g.db.execute('select count(*) from todos')
        total = cur.fetchone()[0]
        sql = 'select * from todos limit {}, {}'.format(offset, per_page)
        cur = g.db.execute(sql)
        todos = cur.fetchall()
        cur.close()
        return (total, todos)

    def delete_description(self, id):
        """remove task from database"""
        g.db.execute("DELETE FROM todos WHERE id ='%s'" % id)
        g.db.commit()

    def complete_description(self, id):
        """mark planned task as done in database"""
        g.db.execute("UPDATE todos SET completed = 1 WHERE id ='%s'" % id)
        g.db.commit()

#TODO: avoid entering same description twice and even more
    def insert_description(self, user, description, completed):
        """add new task into database"""
        g.db.execute(
            "INSERT INTO todos (user_id, description, completed) VALUES ('%s', '%s', '%s')"
            % (user, description, completed)
            )
        g.db.commit()