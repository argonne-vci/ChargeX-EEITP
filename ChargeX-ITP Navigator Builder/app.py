import os
import sys
import json
import threading
import webbrowser
from flask import Flask, render_template, send_from_directory, jsonify

# Determine the base path for files (for PyInstaller compatibility)
if getattr(sys, 'frozen', False):
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Create Flask app with explicit template and static folders
app = Flask(__name__, template_folder=os.path.join(BASE_DIR, 'templates'),
                        static_folder=os.path.join(BASE_DIR, 'static'))

# Home route
@app.route('/')
def index():
    return render_template('index.html')

# Tree data route (loads JSON)
@app.route('/tree')
def get_tree():
    json_path = os.path.join(BASE_DIR, 'tree_data.json')
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            return jsonify(json.load(f))
    except Exception as e:
        print(f"Error loading tree_data.json: {e}")
        return "Error loading tree data", 500

# Route to serve test case HTML files
@app.route('/testcases/<filename>')
def get_testcase(filename):
    testcases_dir = os.path.join(BASE_DIR, 'static', 'testcases')
    return send_from_directory(testcases_dir, filename)

# Auto-launch browser on app start
def open_browser():
    webbrowser.open_new("http://localhost:5000")

# Run app
if __name__ == '__main__':
    threading.Timer(1.0, open_browser).start()
    app.run(debug=False, use_reloader=False)
