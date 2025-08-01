from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from flask_cors import CORS
from PIL import Image
from datetime import timedelta
import mysql.connector
import os
import io
import base64

app = Flask(__name__) # run the Flask app, create a new Flask web application
CORS(app) # restricts requests from different domains
app.secret_key = 'abc'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(seconds=300)

UPLOAD_FOLDER = 'uploads' # save the copy of the upload file to this directory
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


# refresh session timeout on each request
@app.before_request
def make_session_permanent():
    if session.get('log_in'):
        session.permanent = True
        session.modified = True

# connect to the MySQL database
def get_db_connection():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='mysql123',
        database='odpc'
    )
    return conn

@app.route('/api')
def api():
    return {"message": "Hello from Backend!"}

@app.route('/', methods=['GET', 'POST'])
def index():
    # session['log_in'] = False
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute('select * from users')
            users = cursor.fetchall()
            for user in users:
                if username == user[1] and password == user[2]:
                    session['log_in'] = True
                    return redirect(url_for('index'))
            return render_template('index.html', message="Invalid username or password")
        except Exception as e:
            return jsonify({'Error': 'An error occurred during file open'}), 500
    return render_template('index.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/sign_up')
def sign_up():
    return render_template('sign_up.html')

@app.route('/create_account', methods=['get', 'post'])
def create_account():
    username = request.form['username']
    password = request.form['password']
    print(username, password)

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('select * from users where username = %s', (username,))
    user = cursor.fetchone()
    print(user)

    if user:
        conn.close()
        return render_template('index.html', message="Username already exists.")
    
    cursor.execute('insert into users (username, password) values (%s, %s)', (username, password))
    conn.commit()
    conn.close()

    # return redirect(url_for('index'))
    # return redirect(url_for('index'), message="Account created successfully.")
    return redirect(url_for('index', message='Account created successfully.'))
    return render_template('index.html', message="Account created successfully.")

@app.route('/show_photos')
def show_all_photos():
    name = request.args.get('name')
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('select * from person where name = %s', (name,))
        name_exists = cursor.fetchone()

        if name_exists:
            cursor.execute('select * from photo where person_id = %s', (name_exists[0],))
            photos = cursor.fetchall()
            
            image_data = []
            for photo in photos[::-1]:
                binary_data = photo[2]
                try:
                    image = Image.open(io.BytesIO(binary_data))
                    image_format = image.format.lower()  # file extension 
                    encoded_img = base64.b64encode(binary_data).decode('utf-8')
                    image_data.append({'type': image_format, 'data': encoded_img})
                except Exception as e:
                    return jsonify({'error': 'An error occurred during file open'}), 500

            cursor.close()
            conn.close()

            return render_template('photos.html', images=image_data, name=name)
        else:
            return render_template('index.html', message=f'Name: {name} not found.')
    except Exception as e:
        return jsonify({'Error': 'An error occurred during file open'}), 500

@app.route('/search')
def search():
    name = request.args.get('name')
    print(name)
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('select * from person where name = %s', (name,))
        name_exists = cursor.fetchone()

        if name_exists:
            cursor.execute('select * from photo where person_id = %s', (name_exists[0],))
            photos = cursor.fetchall()
            
            image_data = []
            for photo in photos[-1: -4: -1]:
                binary_data = photo[2]
                try:
                    image = Image.open(io.BytesIO(binary_data))
                    image_format = image.format.lower()  # file extension 
                    encoded_img = base64.b64encode(binary_data).decode('utf-8')
                    image_data.append({'type': image_format, 'data': encoded_img})
                except Exception as e:
                    return jsonify({'error': 'An error occurred during file open'}), 500

            cursor.close()
            conn.close()

            return render_template('search.html', images=image_data, name=name)
        else:
            return render_template('index.html', message=f'Name: {name} not found.')
    except Exception as e:
        return jsonify({'Error': 'An error occurred during file open'}), 500

@app.route('/upload', methods=['POST'])
def upload_photo():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        file = request.files['file']
        name = request.form['name']
        visibility = request.form['visibility']

        if not file or not name:
            return jsonify({'error': 'Missing file or name'}), 400

        # log the file name and name field for debugging
        print(f"Received name: {name}")
        print(f"Received file: {file.filename}")

        # connect to the database and insert data
        conn = get_db_connection()
        cursor = conn.cursor()

        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)  # save the file in the 'uploads' directory

        with open(file_path, 'rb') as f:
            photo_data = f.read() # read the file's binary data

        cursor.execute('select id from person where name = %s', (name,))
        name_exists = cursor.fetchone()

        if name_exists:
            person_id = name_exists[0]
        else:
            cursor.execute('insert into person (name) VALUES (%s)', (name,))
            person_id = cursor.lastrowid

        cursor.execute('insert into photo (person_id, photo, file_name) VALUES (%s, %s, %s)', (person_id, photo_data, file.filename))
        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for('index'))

    except Exception as e:
        return jsonify({'error': 'An error occurred during file upload'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=3001)  # run on port 3001
