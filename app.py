from flask import Flask, render_template, request, redirect, url_for, jsonify, json, session
from flask_sqlalchemy import SQLAlchemy
from jinja2.exceptions import TemplateError
from flask_mail import Mail, Message
from werkzeug.security import check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://admin:admin@localhost/your_database_name'  # Replace with your database connection details
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

app.secret_key = 'your_secret_key'

def load_users():
    with open('users.json', 'r') as file:
        return json.load(file)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('email')
        password = request.form.get('password')
        session['admin']=False
        if authenticate_user(username, password):
            #session['user'] = username  # Create a session for the logged-in user
            users_data = load_data()
            users_list = users_data['user']
            name=''
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
        error_message = "Invalid credentials. Please try again."
        return render_template('login.html', error_message=error_message)

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



app.config['MAIL_SERVER'] = 'smtp.example.com'   # Your mail server
app.config['MAIL_PORT'] = 587                    # Mail server port
app.config['MAIL_USE_TLS'] = True                # Use TLS
app.config['MAIL_USE_SSL'] = False               # Not using SSL
app.config['MAIL_USERNAME'] = 'vladut.petrea02@e-uvt.ro'  # Your email
app.config['MAIL_PASSWORD'] = 'rumidotuba52'    # Your email password
app.config['MAIL_DEFAULT_SENDER'] = 'maintanance@taskpulse.com' # Default sender

mail = Mail(app)

@app.route('/request-account', methods=['POST'])
def request_account():
    # ... code to handle account request ...

    # Assuming you have the requestor's email and name
    email = request.form.get('email')
    name = request.form.get('name')
    msg = Message("Account Request Received", recipients=[email])
    msg.body = f"Hello {name},\n\nYour account request has been received. We will process it shortly."

    mail.send(msg)

    return "Account request received. Email sent."





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
    user_name = request.args.get('name')  # Extracted the 'name' parameter
    user_photo = request.args.get('user_photo')
    data = load_data()
    tasks_planned = [task for task in data['task'] if task['status'] == 'Planned']
    tasks_in_progress = [task for task in data['task'] if task['status'] == 'In Progress']
    tasks_needs_review = [task for task in data['task'] if task['status'] == 'Needs Review']
    tasks_done = [task for task in data['task'] if task['status'] == 'Done']
    users = {user['user_id']: user for user in data['user']}
    team=data['team']
    cur_members=[members for members in data['user_team'] if members['team_id'] == session.get('team')]

    return render_template('admin_dashboard.html', 
                           tasks_planned=tasks_planned, 
                           tasks_in_progress=tasks_in_progress, 
                           tasks_needs_review=tasks_needs_review, 
                           tasks_done=tasks_done, users=users, user_email=user_email, user_name=user_name, user_photo=user_photo,team=team, cur_members=cur_members)

@app.route('/task/add', methods=['GET', 'POST'])
def add_task():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        status = request.form.get('status')
        user_id = int(request.form.get('user_id'))
        difficulty = request.form.get('difficulty')

        data = load_data()
        new_task_id = max(task['task_id'] for task in data['task']) + 1
        new_task = {"task_id": new_task_id, "title": title, "description": description, "status": status, "user_id": user_id, "difficulty": difficulty}
        data['task'].append(new_task)
        save_data(data)

        return redirect(url_for('dashboard'))
    return render_template('add_task.html')

@app.route('/task/edit/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)

    if request.method == 'POST':
        task.title = request.form.get('title')
        task.description = request.form.get('description')
        task.status = request.form.get('status')
        # user_id is not updated, but you can add it if needed

        db.session.commit()
        return redirect(url_for('show_tasks'))

    return render_template('edit_task.html', task=task)  # Create a template for editing a task

@app.route('/task/delete/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('show_tasks'))

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

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

