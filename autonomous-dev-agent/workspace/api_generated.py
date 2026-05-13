# API REST Gerada Autonomamente
from flask import Flask, jsonify, request

app = Flask(__name__)
tasks = []

@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks)

@app.route('/tasks', methods=['POST'])
def create_task():
    task = request.json
    tasks.append(task)
    return jsonify(task), 201

@app.route('/tasks/<int:id>', methods=['GET'])
def get_task(id):
    return jsonify(tasks[id]) if id < len(tasks) else ("Not found", 404)

if __name__ == '__main__':
    app.run(debug=True)
