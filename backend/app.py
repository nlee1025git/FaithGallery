from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_cors import CORS
import mysql.connector
import os

app = Flask(__name__) # run the Flask app, create a new Flask web application
CORS(app) # restricts requests from different domains

UPLOAD_FOLDER = 'uploads' # save the copy of the upload file to this directory
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# connect to the MySQL database
def get_db_connection():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='odpc'
    )
    return conn

@app.route('/api')
def api():
    return {"message": "Hello from Backend!"}


@app.route('/upload', methods=['POST'])
def upload_photo():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        file = request.files['file']
        name = request.form['name']

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

        cursor.execute('INSERT INTO photos (name, photo) VALUES (%s, %s)', (name, photo_data))
        conn.commit()
        cursor.close()
        conn.close()

        # return success response
        return {"message": 'File uploaded successfully'}
    
    except Exception as e:
        print(f"Error: {e}")  # log the exception for debugging
        return {"message": 'An error occurred during file upload'}

if __name__ == '__main__':
    app.run(debug=True, port=3001)  # run on port 3001
