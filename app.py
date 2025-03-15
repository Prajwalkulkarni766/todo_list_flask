from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    time = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title} - {self.description}"

@app.route("/", methods=["GET", "POST"])
def root():
    if request.method == "POST":
        # Get form data
        title = request.form.get("todoHeading")
        description = request.form.get("todoBody")
        
        # Create a new Todo object
        new_todo = Todo(title=title, description=description)
        
        # Add and commit to the database
        db.session.add(new_todo)
        db.session.commit()

        return redirect(url_for("root"))
    
    # Query all todos from the database
    data = Todo.query.all()
    return render_template("index.html", data=data)

@app.route("/delete/<int:id>")
def delete_todo(id):
    # Find the Todo item by ID
    todo_to_delete = Todo.query.get(id)

    # If the item exists, delete it
    if todo_to_delete:
        db.session.delete(todo_to_delete)
        db.session.commit()

    # Redirect to the root page after deletion
    return redirect(url_for("root"))

@app.route("/update/<int:id>", methods=["GET", "POST"])
def update_todo(id):
    todo = Todo.query.get_or_404(id)

    if request.method == "POST":
        # Get form data
        todo.title = request.form["todoHeading"]
        todo.description = request.form["todoBody"]
        
        # Commit the updated values to the database
        db.session.commit()

        return redirect(url_for("root"))

    return render_template("update.html", todo=todo)

if __name__ == "__main__":
    app.run(debug=True)
