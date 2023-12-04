from app import db, User, Task, Team, UserTeam

# Create sample users
user1 = User(username='user1', email='user1@example.com')
user2 = User(username='user2', email='user2@example.com')
user3 = User(username='user3', email='user3@example.com')

# Create sample tasks
task1 = Task(title='Task 1', description='Sample task 1', status='Pending', user=user1)
task2 = Task(title='Task 2', description='Sample task 2', status='Completed', user=user2)
task3 = Task(title='Task 3', description='Sample task 3', status='In Progress', user=user3)

# Create sample teams
team1 = Team(name='Team A', description='Sample team A')
team2 = Team(name='Team B', description='Sample team B')

# Associate users with teams (customize as needed)
user1.teams.append(team1)
user2.teams.append(team1)
user2.teams.append(team2)
user3.teams.append(team2)

# Add objects to the session and commit to the database
db.session.add(user1)
db.session.add(user2)
db.session.add(user3)
db.session.add(task1)
db.session.add(task2)
db.session.add(task3)
db.session.add(team1)
db.session.add(team2)
db.session.commit()

print("Sample data has been added to the database.")
