from flask import Flask, redirect, render_template, url_for, request
from flask_sqlalchemy import SQLAlchemy
import database_entry


app = Flask(__name__)
app.config.from_object(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = database_entry.database_credentials
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    comment = db.Column(db.String(2000))


db.create_all()


@app.route("/")
def index():
    return render_template('index.html')


@app.route('/view')
def view():
    return render_template('view.html')


@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if request.method == 'POST':
        chatname = request.form['chatname']
        message = request.form['message']
        chat_mes = Posts(name=chatname,
                         comment=message)
        db.session.add(chat_mes)
        db.session.commit()
        result = Posts.query.paginate(per_page=10,
                                      page=1,
                                      error_out=True)

        return render_template('chat.html', result=result)

    result = Posts.query.paginate(per_page=10,
                                  page=1,
                                  error_out=True)
    return render_template('chat.html', result=result)


@app.route('/posts/<int:page_num>', methods=['GET'])
def thread(page_num):
    threads = Posts.query.paginate(per_page=5,
                                   page=page_num,
                                   error_out=True)

    return render_template('view.html', result=threads)


@app.route('/posts', methods=['POST'])
def posts():
    name = request.form['name']
    post = request.form['post']
    if name == '' or post == '':
        return render_template('index.html', blank=True)
    else:
        signature = Posts(name=name, comment=post)
        db.session.add(signature)
        db.session.commit()

        result = Posts.query.all()
        reversed(result)
        return redirect(url_for('thread', page_num=1))
        # return render_template('view.html', result=result)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
