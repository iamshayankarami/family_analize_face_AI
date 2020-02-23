from flask import Flask, request, g, redirect, url_for, abort, render_template,send_from_directory
from werkzeug.utils import secure_filename
from hashlib import md5
from PIL import Image
import sqlite3
import os
import time

DEBUG              = True
BASE_DIR           = '/var/www/flaskgur/'
UPLOAD_DIR         = BASE_DIR + 'pics'
DATABASE           = BASE_DIR + 'flaskgur.db'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config.from_object(__name__)

# Make sure extension is in the ALLOWD_EXTENSIONS set
def check_extension(extension):
    return extension in ALLOWED_EXTENSIONS

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

# Return a list of the last 25 uploaded images  
def get_last_pics():
    cur = g.db.execute('select * from pics order by id desc limit 25')
    filenames = [dict(id=row[0], filename=row[1], label=row[2]) for row in cur.fetchall()]
    #filenames = [row[0] for row in cur.fetchall()]
    return filenames

# Insert filename into database 
def add_pic(filename, label):
    g.db.executemany('insert into pics (filename, label) values (?, ?)', [filename, label])
    g.db.commit()

# Generate thumbnail image
def gen_thumbnail(filename):
    height = width = 200
    original = Image.open(os.path.join(app.config['UPLOAD_DIR'], filename))
    thumbnail = original.resize((width, height), Image.ANTIALIAS)
    thumbnail.save(os.path.join(app.config['UPLOAD_DIR'], 'thumb_'+filename))


def add_label(label):
    label = request.form['label']
    g.db.execute('INSERT INTO pics (label) VALUES (?)', [label])
    g.db.commit()


# Taken from flask example app
@app.before_request
def before_request():
    g.db = connect_db()

# Taken from flask example app
@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/', methods=['GET','POST'])
def upload_pic():
    if request.method == 'POST':
        file = request.files['file']
        extension = file.filename.rsplit('.', 1)[1].lower()
        if file and check_extension(extension):
            # Salt and hash the file contents
            filename = md5(file.read() + str(round(time.time() * 1000))).hexdigest() + '.' + extension
            file.seek(0) # Move cursor back to beginning so we can write to disk
            file.save(os.path.join(app.config['UPLOAD_DIR'], filename, label))
            add_pic(filename)
            add_label(label)
            gen_thumbnail(filename)
            return redirect(url_for('show_pic', filename=filename))
        else: # Bad file extension
            abort(404)
    else:
        return render_template('upload.html', pics=get_last_pics())

@app.route('/show')
def show_pic():
    filename = request.args.get('filename','')
    return render_template('upload.html', filename=filename, label=label)
def show_label():
    g.db = connect_db()
    cur = g.db.execute('SELECT label FROM pics WHERE id=(?)')
    labels = cur.fetchone()
    return render_template('upload.html', labels=labels)

@app.route('/pics/<filename>')
def return_pic(filename):
    return send_from_directory(app.config['UPLOAD_DIR'], secure_filename(filename))

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
