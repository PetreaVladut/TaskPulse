from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://admin:admin@localhost/your_database_name'  # Replace with your database connection details
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    tasks = db.relationship('Task', backref='user', lazy=True)
    teams = db.relationship('Team', secondary='user_team', back_populates='users')

class Task(db.Model):
    __tablename__ = 'task'
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))

class Team(db.Model):
    __tablename__ = 'team'
    team_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    users = db.relationship('User', secondary='user_team', back_populates='teams')

class UserTeam(db.Model):
    __tablename__ = 'user_team'
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('team.team_id'), primary_key=True)

@app.route('/tasks')
def show_tasks():
    tasks = Task.query.all()
    return render_template('tasks.html', tasks=tasks)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()


