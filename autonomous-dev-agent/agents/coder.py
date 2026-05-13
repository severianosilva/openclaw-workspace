"""Agente Codificador - Gera código autônomo"""

from typing import Dict
import os

class CoderAgent:
    def __init__(self, workspace_path: str):
        self.workspace = workspace_path
        os.makedirs(workspace_path, exist_ok=True)
    
    def generate_code(self, plan: Dict) -> str:
        """Gera código baseado no plano"""
        request = plan.get("request", "")
        
        if "API" in request:
            return self._generate_api(plan)
        elif "script" in request.lower():
            return self._generate_script(plan)
        else:
            return self._generate_generic(plan)
    
    def _generate_api(self, plan: Dict) -> str:
        code = '''# API REST Gerada Autonomamente
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
'''
        filename = "api_generated.py"
        with open(os.path.join(self.workspace, filename), 'w') as f:
            f.write(code)
        return filename
    
    def _generate_script(self, plan: Dict) -> str:
        code = '''#!/usr/bin/env python3
# Script gerado autonomamente

def main():
    print("Executando script...")
    
if __name__ == "__main__":
    main()
'''
        filename = "script_generated.py"
        with open(os.path.join(self.workspace, filename), 'w') as f:
            f.write(code)
        return filename
    
    def _generate_generic(self, plan: Dict) -> str:
        filename = "generated.py"
        code = f"# Código gerado: {plan.get('request', 'unknown')}\nprint('Hello World')\n"
        with open(os.path.join(self.workspace, filename), 'w') as f:
            f.write(code)
        return filename