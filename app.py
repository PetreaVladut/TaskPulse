from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, jsonify, json, session
from flask_sqlalchemy import SQLAlchemy
from jinja2.exceptions import TemplateError
from flask_mail import Mail, Message
from werkzeug.security import check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://admin:admin@localhost/your_database_name' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

app.secret_key = 'your_secret_key'

def load_users():
    with open('users.json', 'r') as file:
        return json.load(file)

def append_recent_activity(activity):
    try:
        with open('logs.json', 'r') as file:
            activities = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        activities = []

    activities.append(activity)
    print("smth")
    with open('logs.json', 'w') as file:
        json.dump(activities, file, indent=4)

def get_recent_activities():
    try:
        print("smthreeed")
        with open('logs.json', 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []  # Return an empty list if file not found or empty

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        session['admin']=False
        if authenticate_user(email, password):
            #session['user'] = username  # Create a session for the logged-in user
            session['email']=email
            session['password']=password
            users_data = load_data()
            users_list = users_data['user']
            name='admin'
            image='images/profile2.jpg'
            for user_dict in users_list:
                if user_dict['email'] == email:
            # Found the user, return their image and username
                    name = user_dict.get('username', '')
                    image = user_dict.get('image', 'profile2.jpg')  # Replace with your image field name
                    print(name)
                    print(image)
            session['username']=name
            if session.get('admin'):
                print("da,nene")
                print(session.get('admin'))
                return redirect(url_for('admin_dashboard',user_email=email, name=name,user_photo=image) ) # Redirect to the dashboard after successful login
            else:
                return redirect(url_for('dashboard',user_email=email, name=name,user_photo=image) ) # Redirect to the dashboard after successful login
        error_message = "Invalid credentials. Please try again."
        return render_template('login.html', error_message=error_message)

    return render_template('login.html')

@app.route('/1')
def login1():
    username = session.get('email')
    password = session.get('password')
    session['admin']=False
    if authenticate_user(username, password):
        #session['user'] = username  # Create a session for the logged-in user
        users_data = load_data()
        users_list = users_data['user']
        name='admin'
        image='images/profile2.jpg'
        for user_dict in users_list:
            if user_dict['email'] == username:
        # Found the user, return their image and username
                name = user_dict.get('username', '')
                image = user_dict.get('image', 'profile2.jpg')  # Replace with your image field name
                print(name)
                print(image)
        if session.get('admin'):
            print("da,nene")
            print(session.get('admin'))
            return redirect(url_for('admin_dashboard',user_email=username, name=name,user_photo=image) ) # Redirect to the dashboard after successful login
        else:
            return redirect(url_for('dashboard',user_email=username, name=name,user_photo=image) ) # Redirect to the dashboard after successful login
    
    return render_template('login.html')

def authenticate_user(username, password):
    users_data = load_users()
    users_list = users_data['users']

    # Iterate through the list of user dictionaries
    for user_dict in users_list:
        # Check if the provided username (email) exists in the current user dictionary
        if username in user_dict:
            # Check if the provided password matches the stored password
            stored_password = user_dict[username]
            print(stored_password)
            print(password)
            if stored_password[0]['password'] == password:
                print('da')
                session['admin']=stored_password[0]['isadmin']
                print(session.get('admin'))
                return True
    return False


def load_data():
    with open('data.json', 'r') as file:
        return json.load(file)

def save_data(data):
    with open('data.json', 'w') as file:
        json.dump(data, file, indent=4)

"""
app.config['MAIL_SERVER']='sandbox.smtp.mailtrap.io'
app.config['MAIL_PORT'] = 2525
app.config['MAIL_USERNAME'] = '06090bccb975e2'
app.config['MAIL_PASSWORD'] = 'a394848e49fd4f'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False 
mail = Mail(app)


""" 
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'vladut.petrea0268@gmail.com'
app.config['MAIL_PASSWORD'] = 'pfoa jhui ugbf thof'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True 
mail = Mail(app)

@app.route('/sendemail')
def sendemail():
    # ... code to handle account request ...

    # Assuming you have the requestor's email and name
    email = request.args.get('email')
    name = request.args.get('name')
    reason = request.args.get('reason')
    msg = Message("Account Request Received",sender='vladut.petrea0268@gmail.com', recipients=['vladut.petrea0268@gmail.com'])
    msg.body = f"Hello Admin,\n\n {name} has requested a new account on the reason of {reason}. Please send your conclusion to {email}"

    if mail.send(msg):
        return redirect(url_for('login'))
    return redirect(url_for('login'))

@app.route('/request-account',  methods=['GET', 'POST'])
def request_account():
    if request.method == 'POST':
        user_email = request.form.get('email')
        print(user_email)
        user_name = request.form.get('name')  # Extracted the 'name' parameter
        reason = request.form.get('reason')  # Extracted the 'name' parameter
        return redirect(url_for('sendemail',email=user_email,name=user_name,reason=reason))

    return render_template('request_account.html')



@app.route('/tasks')
def dashboard():
    user_email = request.args.get('user_email')
    user_name = request.args.get('name')  # Extracted the 'name' parameter
    user_photo = request.args.get('user_photo')
    data = load_data()
    tasks_planned = [task for task in data['task'] if task['status'] == 'Planned']
    tasks_in_progress = [task for task in data['task'] if task['status'] == 'In Progress']
    tasks_needs_review = [task for task in data['task'] if task['status'] == 'Needs Review']
    tasks_done = [task for task in data['task'] if task['status'] == 'Done']

    users = {user['user_id']: user for user in data['user']}

    return render_template('dashboard.html', 
                           tasks_planned=tasks_planned, 
                           tasks_in_progress=tasks_in_progress, 
                           tasks_needs_review=tasks_needs_review, 
                           tasks_done=tasks_done, users=users, user_email=user_email, user_name=user_name, user_photo=user_photo)

@app.route('/tasksadmin')
def admin_dashboard():
    user_email = request.args.get('user_email')
    user_name = request.args.get('name')
    user_photo = request.args.get('user_photo')
    data = load_data()

    tasks = {
        'Planned': [task for task in data['task'] if task['status'] == 'Planned'],
        'In Progress': [task for task in data['task'] if task['status'] == 'In Progress'],
        'Needs Review': [task for task in data['task'] if task['status'] == 'Needs Review'],
        'Done': [task for task in data['task'] if task['status'] == 'Done']
    }

    users = {user['user_id']: user for user in data['user']}
    team = data['team']
    user_team = data['user_team']

    team_members = {}

    # Get current user's team based on their email
    current_user = next((user for user in users.values() if user['email'] == user_email), None)
    if current_user:
        user_id = current_user['user_id']
        current_team_id = next((ut['team_id'] for ut in user_team if ut['user_id'] == user_id), None)

        if current_team_id:
            # Get all users in the current team
            team_members = [users[ut['user_id']] for ut in user_team if ut['team_id'] == current_team_id]
        else:
            current_team_id=1
            team_members = [users[ut['user_id']] for ut in user_team if ut['team_id'] == current_team_id]
    recent_activity=get_recent_activities()
    return render_template('admin_dashboard.html', 
                           tasks=tasks, 
                           users=users, 
                           user_email=user_email, 
                           user_name=user_name, 
                           user_photo=user_photo,
                           team=team, 
                           team_members=team_members,team_id=current_team_id,logs=recent_activity)

@app.route('/task/add', methods=['GET', 'POST'])
def add_task():
    data=load_data()
    users=data['user']
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        status = request.form.get('status')
        user_id_1 = request.form.get('user_id')
        difficulty = request.form.get('difficulty')
        deadline = request.form.get('deadline')
        if(str(user_id_1)=='None'):
            user_id=0
        else:
            user_id=int(str(user_id_1))
        data = load_data()
        new_task_id = max(task['task_id'] for task in data['task']) + 1
        new_task = {"task_id": new_task_id, "title": title, "description": description, "status": status, "user_id": user_id, "difficulty": difficulty,"deadline":deadline}
        data['task'].append(new_task)    
        activity = {
        'description': f'Task {title} was added by {session.get("username")}',
        'timestamp': (datetime.fromisoformat(datetime.now().isoformat())).strftime("%B %d, %Y %H:%M:%S")
        }
        append_recent_activity(activity)
        save_data(data)
        return redirect(url_for('login1'))
    return render_template('add_task.html',users=users)

@app.route('/task/edit/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    data = load_data()
    print(task_id)
    # Find the task to be edited
    task = next((t for t in data['task'] if t['task_id'] == task_id), None)

    if not task:
        # Task not found
        return "Task not found", 404

    if request.method == 'POST':
        print("de ce?")
        # Update task details from the form data
        task['title'] = request.form.get('title', task['title'])
        task['description'] = request.form.get('description', task['description'])
        task['status'] = request.form.get('status', task['status'])
        task['user_id'] = int(request.form.get('user_id', task['user_id']))
        task['difficulty'] = request.form.get('difficulty', task['difficulty'])
        task['deadline'] = request.form.get('deadline', task['deadline'])

        # Save updated data
        activity = {
        'description': f'Task {task["title"]} was edited by {session.get("username")}',
        'timestamp': (datetime.fromisoformat(datetime.now().isoformat())).strftime("%B %d, %Y %H:%M:%S")
        }
        append_recent_activity(activity)
        save_data(data)

        # Redirect to the dashboard
        return redirect(url_for('login1'))

    # Render edit task template with existing task data
    return render_template('edit_task.html', task=task)

@app.route('/task/delete/<int:task_id>')
def delete_task(task_id):
    data = load_data()  # Load all data from your data.json file
    task_name=[task for task in data['task'] if task['task_id']==task_id]
    activity = {
        'description': f'Task {task_name[0]["title"]} was deleted by {session.get("username")}',
        'timestamp': (datetime.fromisoformat(datetime.now().isoformat())).strftime("%B %d, %Y %H:%M:%S")
    }
    append_recent_activity(activity)
    # Find and remove the task with the given task_id
    data['task'] = [task for task in data['task'] if task['task_id'] != task_id]
    save_data(data)  # Save the updated data back to the data.json file

    # Redirect to the dashboard or another appropriate page after deletion
    return redirect(url_for('login1'))  # Replace 'dashboard' with your dashboard route

@app.route('/update-task-status', methods=['POST'])
def update_task_status():
    try:
        data = request.json
        task_id = int(data.get('task_id'))
        new_status = data.get('new_status')

        all_data = load_data()  # Load all data from JSON file

        # Check if task exists
        for task in all_data['task']:
            if task['task_id'] == task_id:
                task['status'] = new_status  # Update the task's status
                save_data(all_data)  # Save the updated data back to the JSON file
                return jsonify({'status': 'success', 'message': 'Task updated successfully'})

        return jsonify({'status': 'error', 'message': 'Task not found'})

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/update-assignee', methods=['POST'])
def update_assignee():
    data = request.json
    task_id = int(data.get('task_id'))
    new_user_id = int(data.get('new_user_id'))

    all_data = load_data()
    task = next((task for task in all_data['task'] if task['task_id'] == task_id), None)
    
    if task:
        task['user_id'] = new_user_id
        save_data(all_data)
        return jsonify({'status': 'success', 'message': 'Assignee updated successfully'})
    
    return jsonify({'status': 'error', 'message': 'Task not found'})

@app.route('/delete_member/<int:user_id>/<int:team_id>', methods=['POST'])
def delete_member(user_id, team_id):
    print('da')
    data = load_data()
    user_team = data['user_team']

    # Find and remove the user from the team
    user_team[:] = [ut for ut in user_team if not (ut['user_id'] == user_id and ut['team_id'] == team_id)]

    # Save the updated data
    save_data(data)
    return jsonify({'status': 'success', 'message': 'Member removed successfully'})

@app.route('/reload', methods=['GET'])
def reload_page():
    # You can redirect to the same page or a different page by changing the URL in url_for
    return redirect(url_for('admin_dashboard'))

@app.route('/add-member-to-team', methods=['POST'])
def add_member_to_team():
    data = request.json
    user_id = int(data['user_id'])
    team_id = int(data['team_id'])

    all_data = load_data()
    user_team = all_data['user_team']

    # Check if the user is already in the team
    if any(ut for ut in user_team if ut['user_id'] == user_id and ut['team_id'] == team_id):
        return jsonify({'status': 'error', 'message': 'Member already in team'})

    # Add the member to the team
    user_team.append({'user_id': user_id, 'team_id': team_id})
    save_data(all_data)

    return jsonify({'status': 'success', 'message': 'Member added to team successfully'})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
