from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Настройка базы данных SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Модель задачи
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500))
    deadline = db.Column(db.String(10), nullable=False)
    priority = db.Column(db.String(10), nullable=False)
    status = db.Column(db.String(10), default='active')

# Главная страница
@app.route('/')
def index():
    return render_template('index.html')

# Добавление задачи
@app.route('/add_task', methods=['POST'])
def add_task():
    data = request.json
    new_task = Task(
        title=data['title'],
        description=data.get('description', ''),
        deadline=data['deadline'],
        priority=data['priority']
    )
    db.session.add(new_task)
    db.session.commit()
    return jsonify({"message": "Task added successfully!"}), 201

# Получение всех активных задач
@app.route('/get_tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.filter_by(status='active').all()
    task_list = [
        {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "deadline": task.deadline,
            "priority": task.priority
        }
        for task in tasks
    ]
    return jsonify(task_list), 200

# Закрытие задачи
@app.route('/close_task/<int:task_id>', methods=['PUT'])
def close_task(task_id):
    task = Task.query.get(task_id)
    if task:
        task.status = 'inactive'
        db.session.commit()
        return jsonify({"message": "Task closed successfully!"}), 200
    return jsonify({"message": "Task not found!"}), 404

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Создание таблицы, если её нет
    app.run(debug=True)
