from flask import Flask
from flask_cors import CORS
import mysql.connector
import os

app = Flask(__name__)
CORS(app)  # Allow all origins (fine for local testing)

@app.route('/api')
def api():
    return {"message": "Hello from API!"}

def get_db_connection():
    conn = mysql.connector.connect(
        host='host',
        user='username',
        password='password',
        database='database'
    )
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_photo():
    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']
    name = request.form['name']
    
    if file and name:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        photo_data = file.read()
        cursor.execute('INSERT INTO photos (name, photo) VALUES (%s, %s)', (name, photo_data))
        conn.commit()
        cursor.close()
        conn.close()
        
        return 'File uploaded successfully', 200

@app.route('/search', methods=['GET'])
def search_photo():
    name = request.args.get('name')
    if not name:
        return 'Name parameter is required', 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT id, name FROM photos WHERE name LIKE %s', ('%' + name + '%',))
    photos = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template('search_results.html', photos=photos)

@app.route('/view/<int:photo_id>', methods=['GET'])
def view_photo(photo_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT name, photo FROM photos WHERE id = %s', (photo_id,))
    photo = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    if photo:
        return send_file(photo[1], mimetype='image/jpeg', as_attachment=False, download_name=photo[0])
    else:
        return 'Photo not found', 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3001)