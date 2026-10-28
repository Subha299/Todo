from flask import Flask , render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    SNo = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.String(200), nullable = False)
    Description = db.Column(db.String(500), nullable = False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)
    def __repr__(self):
        return f"{self.SNo}-{self.Title}"

@app.route("/", methods=['GET','POST'])
def hello_world():
    if request.method=='POST':
        print("Post")
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(Title = title , Description = desc)
        db.session.add(todo)
        db.session.commit()
    allTodo = Todo.query.all()  
    return render_template('index.html',allTodo=allTodo)

@app.route("/show")
def products():
    allTodo = Todo.query.all()
    print(allTodo)
    return "This is Our Project Page."

@app.route("/update/<int:sno>", methods=['GET', 'POST'])
def update(sno):

    todo = Todo.query.filter_by(SNo=sno).first()

    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']

        todo.Title = title
        todo.Description = desc

        db.session.commit()

        return redirect("/")

    return render_template('update.html', todo=todo)


@app.route("/delete/<int:sno>")
def delete(sno):
    todo = Todo.query.filter_by(SNo=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")
if __name__ == '__main__':
    app.run(debug=True,port=8000)
