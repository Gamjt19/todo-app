import os
import logging

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

# --------------------------------------------------
# Configuration
# --------------------------------------------------

app.config["TESTING"] = (
    os.getenv("TESTING", "false").lower() == "true"
)

DB_USER = os.getenv("MYSQL_USER", "todo_user")
DB_PASSWORD = os.getenv("MYSQL_PASSWORD", "todo_password")
DB_HOST = os.getenv("MYSQL_HOST", "db")
DB_NAME = os.getenv("MYSQL_DATABASE", "todo_db")

# Production database: MySQL
app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}/{DB_NAME}"
)

# Testing database: temporary SQLite
if app.config["TESTING"]:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# --------------------------------------------------
# Database
# --------------------------------------------------

db = SQLAlchemy(app)

# --------------------------------------------------
# Logging
# --------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

# --------------------------------------------------
# Model
# --------------------------------------------------


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)


# --------------------------------------------------
# Health Check
# --------------------------------------------------


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy"}), 200


# --------------------------------------------------
# Get all todos
# --------------------------------------------------


@app.route("/todos", methods=["GET"])
def get_todos():
    todos = Todo.query.all()

    return jsonify([
        {
            "id": todo.id,
            "title": todo.title,
            "completed": todo.completed
        }
        for todo in todos
    ]), 200


# --------------------------------------------------
# Create todo
# --------------------------------------------------


@app.route("/todos", methods=["POST"])
def create_todo():
    data = request.get_json()

    if not data or "title" not in data:
        return jsonify({
            "error": "title is required"
        }), 400

    todo = Todo(
        title=data["title"],
        completed=False
    )

    db.session.add(todo)
    db.session.commit()

    app.logger.info("Created todo: %s", todo.title)

    return jsonify({
        "id": todo.id,
        "title": todo.title,
        "completed": todo.completed
    }), 201


# --------------------------------------------------
# Update todo
# --------------------------------------------------


@app.route("/todos/<int:todo_id>", methods=["PUT"])
def update_todo(todo_id):
    todo = db.session.get(Todo, todo_id)

    if todo is None:
        return jsonify({
            "error": "Todo not found"
        }), 404

    data = request.get_json()

    if "title" in data:
        todo.title = data["title"]

    if "completed" in data:
        todo.completed = data["completed"]

    db.session.commit()

    return jsonify({
        "id": todo.id,
        "title": todo.title,
        "completed": todo.completed
    }), 200


# --------------------------------------------------
# Delete todo
# --------------------------------------------------


@app.route("/todos/<int:todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    todo = db.session.get(Todo, todo_id)

    if todo is None:
        return jsonify({
            "error": "Todo not found"
        }), 404

    db.session.delete(todo)
    db.session.commit()

    app.logger.info("Deleted todo: %s", todo_id)

    return jsonify({
        "message": "Todo deleted"
    }), 200


# --------------------------------------------------
# Create database tables
# --------------------------------------------------

if not app.config["TESTING"]:
    with app.app_context():
        db.create_all()


# --------------------------------------------------
# Run application
# --------------------------------------------------

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000
    )
