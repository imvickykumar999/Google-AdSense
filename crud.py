
from flask import (Flask,
    render_template,
    request, redirect,
    url_for, flash,
    session,
)

from werkzeug.utils import secure_filename
from functools import wraps
import os, random, secrets
import sqlite3 as sql

try: os.mkdir('mysite/static')
except: pass

try: os.mkdir('mysite/static/files')
except: pass

app=Flask(__name__)
secret_key = secrets.token_hex(16)
app.config['SECRET_KEY'] = secret_key


UPLOAD_FOLDER ="static/files"
FILE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'avi'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_extensions(file_name):
    return '.' in file_name and file_name.rsplit('.',1)[1].lower() in FILE_EXTENSIONS

@app.route('/login',methods=['POST','GET'])
def login():
    status=True
    con=sql.connect("mysite/db_sample.db")

    if request.method=='POST':
        email=request.form["email"]
        pwd=request.form["upass"]
        cur=con.cursor()
        cur.execute("select UNAME from users where EMAIL=? and UPASS=?",(email,pwd))
        data=cur.fetchone()

        print(data)
        if data:
            session['logged_in']=True
            session['username']=data[0]
            flash('Login Successfully','success')
            return redirect('index')
        else:
            flash('Invalid Login. Try Again','danger')
    return render_template("login.html")
  

def is_logged_in(f):
	@wraps(f)
	def wrap(*args,**kwargs):
		if 'logged_in' in session:
			return f(*args,**kwargs)
		else:
			flash('Unauthorized, Please Login','danger')
			return redirect(url_for('login'))
	return wrap
  

@app.route('/reg',methods=['POST','GET'])
def reg():
    error = 'Only ADMIN can make CRUD Operation.'
    return render_template('404.html', error=error), 404

    # status=False
    # con=sql.connect("mysite/db_sample.db")

    # if request.method=='POST':
    #     name=request.form["uname"]
    #     email=request.form["email"]
    #     pwd=request.form["upass"]
    #     cur=con.cursor()
    #     cur.execute("insert into users(UNAME,UPASS,EMAIL) values(?,?,?)",(name,pwd,email))
    #     con.commit()
    #     cur.close()
    #     flash('Registration Successfully. Login Here...','success')
    #     return redirect('login')
    # return render_template("reg.html",status=status)


@app.route("/logout")
def logout():
	session.clear()
	flash('You are now logged out','success')
	return redirect(url_for('login'))


@app.route("/")
@app.route("/index")
def index():

    con=sql.connect("mysite/db_web.db")
    con.row_factory=sql.Row
    cur=con.cursor()

    cur.execute("select * from users")
    data=cur.fetchall()
    return render_template("index.html",datas=data)


@app.route("/add_user",methods=['POST','GET'])
@is_logged_in
def add_user():

    if request.method=='POST':
        uname=request.form['uname']
        contact=request.form['contact']
        name=request.form['name']

        if 'file' not in request.files:
            flash('No file part','danger')

        file = request.files['file']
        if file.filename == '':
            flash('No file selected','danger')

        if file and allowed_extensions(file.filename):
            filename, file_extension = os.path.splitext(file.filename)
            new_filename = secure_filename(filename+str(random.randint(10000,99999))+"."+file_extension)
            file.save(os.path.join(app.root_path, UPLOAD_FOLDER, new_filename))

        con=sql.connect("mysite/db_web.db")
        cur=con.cursor()

        cur.execute("insert into users(UNAME,CONTACT,NAME,FILE) values (?,?,?,?)",(uname,contact,name,new_filename))
        con.commit()

        flash('Currency Added','success')
        return redirect(url_for("index"))
    return render_template("add_user.html")


@app.route("/edit_user/<string:uid>",methods=['POST','GET'])
@is_logged_in
def edit_user(uid):

    if request.method=='POST':
        uname=request.form['uname']
        contact=request.form['contact']
        name=request.form['name']

        con=sql.connect("mysite/db_web.db")
        cur=con.cursor()

        if 'file' not in request.files:
            flash('No file part','danger')

        file = request.files['file']
        if file.filename == '':
            flash('No file selected','warning')

            cur.execute("update users set UNAME=?,CONTACT=?,NAME=? where UID=?",(uname,contact,name,uid))
            con.commit()

        else:
            if file and allowed_extensions(file.filename):
                filename, file_extension = os.path.splitext(file.filename)
                new_filename = secure_filename(filename+str(random.randint(10000,99999))+"."+file_extension)
                file.save(os.path.join(app.root_path, UPLOAD_FOLDER, new_filename))

            data = cur.execute("select FILE from users where UID=?",(uid,)).fetchall()
            data = f'./static/files/{data[0][0]}'
            os.remove(data)

            cur.execute("update users set UNAME=?,CONTACT=?,NAME=?,FILE=? where UID=?",(uname,contact,name,new_filename,uid))
            con.commit()

        flash('Currency Updated','success')
        return redirect(url_for("index"))

    con=sql.connect("mysite/db_web.db")
    con.row_factory=sql.Row
    cur=con.cursor()

    cur.execute("select * from users where UID=?",(uid,))
    data=cur.fetchone()
    return render_template("edit_user.html",datas=data)


@app.route("/delete_user/<string:uid>",methods=['GET'])
@is_logged_in
def delete_user(uid):
    con=sql.connect("mysite/db_web.db")

    cur=con.cursor()
    data = cur.execute("select FILE from users where UID=?",(uid,)).fetchall()

    data = f'mysite/static/files/{data[0][0]}'
    os.remove(data)

    cur.execute("delete from users where UID=?",(uid,))
    con.commit()

    flash('Currency Deleted','warning')
    return redirect(url_for("index"))


@app.errorhandler(404)
def page_not_found(e):
    error = 'Error 404, Page Not Found.'
    return render_template('404.html', error=error), 404


if __name__=='__main__':
    app.run(debug=True)
