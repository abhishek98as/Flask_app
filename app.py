from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from flask_pymongo import PyMongo
from bson import ObjectId
from datetime import datetime
import os
import pymongo
import sys
import urllib.parse

app = Flask(__name__)

# URL encode username and password to handle special characters
username = urllib.parse.quote_plus("abhishek98as")
password = urllib.parse.quote_plus("12345")

# Updated connection string with new credentials
atlas_uri = f"mongodb+srv://{username}:{password}@cluster0.0zpxbbm.mongodb.net/todo_app?retryWrites=true&w=majority&appName=Cluster0"
app.config["MONGO_URI"] = os.environ.get("MONGO_URI", atlas_uri)
app.secret_key = os.environ.get("SECRET_KEY", "dev_secret_key")

# Initialize MongoDB with error handling
mongo = PyMongo()
db_connected = True
srv_error = False
error_message = ""
auth_error = False

try:
    # Set a shorter server selection timeout for faster feedback
    app.config["MONGO_OPTIONS"] = {
        "serverSelectionTimeoutMS": 5000,
        "connectTimeoutMS": 5000
    }
    
    mongo.init_app(app)
    
    # Test connection by making a simple query
    mongo.db.command('ping')
    print("Successfully connected to MongoDB Atlas!")
    
    # Test if we can access the todos collection
    # This creates the collection if it doesn't exist
    todos_count = mongo.db.todos.count_documents({})
    print(f"Found {todos_count} todos in the database")
    
except pymongo.errors.ConfigurationError as e:
    db_connected = False
    if "dnspython" in str(e):
        srv_error = True
        error_message = f"""Missing dependency: dnspython

To fix this error, install pymongo with the srv extra:
{sys.executable} -m pip install "pymongo[srv]"

Or run:
pip install dnspython pymongo[srv]
"""
    else:
        error_message = f"MongoDB Configuration Error: {e}"
    print(error_message)
    
except pymongo.errors.OperationFailure as e:
    db_connected = False
    auth_error = True
    error_message = f"Authentication Error: {e}\n\nPossible causes:\n1. Incorrect username or password\n2. User doesn't have access to the todo_app database\n3. IP address not whitelisted in MongoDB Atlas Network Access"
    print(error_message)
    
except pymongo.errors.ServerSelectionTimeoutError as e:
    db_connected = False
    error_message = f"MongoDB Server Selection Error: {e}\n\nPossible causes:\n1. Network connectivity issues\n2. Firewall blocking connection\n3. MongoDB Atlas cluster is down or not responding"
    print(error_message)

@app.route('/')
def index():
    todos = []
    if db_connected:
        try:
            todos = list(mongo.db.todos.find().sort('created_at', -1))
            for todo in todos:
                todo['_id'] = str(todo['_id'])
        except Exception as e:
            print(f"Error fetching todos: {e}")
    return render_template('index.html', todos=todos, db_connected=db_connected, 
                          srv_error=srv_error, error_message=error_message)

@app.route('/add_todo', methods=['POST'])
def add_todo():
    if not db_connected:
        flash("Database is not connected. Cannot add todo.", "error")
        return redirect(url_for('index'))
        
    text = request.form.get('text')
    due_date = request.form.get('due_date')
    due_time = request.form.get('due_time')
    
    if text:
        try:
            todo = {
                'text': text,
                'due_date': due_date,
                'due_time': due_time,
                'completed': False,
                'created_at': datetime.now()
            }
            mongo.db.todos.insert_one(todo)
            flash("Todo added successfully!", "success")
        except Exception as e:
            flash(f"Error adding todo: {e}", "error")
    
    return redirect(url_for('index'))

@app.route('/update_todo/<todo_id>', methods=['POST'])
def update_todo(todo_id):
    if not db_connected:
        flash("Database is not connected. Cannot update todo.", "error")
        return redirect(url_for('index'))
        
    text = request.form.get('text')
    due_date = request.form.get('due_date')
    due_time = request.form.get('due_time')
    
    if text:
        try:
            mongo.db.todos.update_one(
                {'_id': ObjectId(todo_id)},
                {'$set': {
                    'text': text,
                    'due_date': due_date,
                    'due_time': due_time
                }}
            )
            flash("Todo updated successfully!", "success")
        except Exception as e:
            flash(f"Error updating todo: {e}", "error")
    
    return redirect(url_for('index'))

@app.route('/toggle_todo/<todo_id>', methods=['POST'])
def toggle_todo(todo_id):
    if not db_connected:
        flash("Database is not connected. Cannot toggle todo.", "error")
        return redirect(url_for('index'))
        
    try:
        todo = mongo.db.todos.find_one({'_id': ObjectId(todo_id)})
        if todo:
            mongo.db.todos.update_one(
                {'_id': ObjectId(todo_id)},
                {'$set': {'completed': not todo.get('completed', False)}}
            )
    except Exception as e:
        flash(f"Error toggling todo: {e}", "error")
    
    return redirect(url_for('index'))

@app.route('/delete_todo/<todo_id>', methods=['POST'])
def delete_todo(todo_id):
    if not db_connected:
        flash("Database is not connected. Cannot delete todo.", "error")
        return redirect(url_for('index'))
        
    try:
        mongo.db.todos.delete_one({'_id': ObjectId(todo_id)})
        flash("Todo deleted successfully!", "success")
    except Exception as e:
        flash(f"Error deleting todo: {e}", "error")
    
    return redirect(url_for('index'))

@app.route('/get_todo/<todo_id>', methods=['GET'])
def get_todo(todo_id):
    if not db_connected:
        return jsonify({'error': 'Database is not connected'}), 500
        
    try:
        todo = mongo.db.todos.find_one({'_id': ObjectId(todo_id)})
        if todo:
            todo['_id'] = str(todo['_id'])
            return jsonify(todo)
        return jsonify({'error': 'Todo not found'}), 404
    except Exception as e:
        return jsonify({'error': f"Error fetching todo: {e}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
