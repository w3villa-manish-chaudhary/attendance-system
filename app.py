from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from flask_socketio import SocketIO



app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/photos', methods=['GET'])
def get_photos():
    return jsonify(photos)

@app.route('/photos/<int:photo_id>', methods=['DELETE'])
def delete_photo(photo_id):
    global photos
    photos = [photo for photo in photos if photo['id'] != photo_id]
    return '', 204

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/recognizer')
def recognizer():
    return render_template('recognizer.html')

@app.route('/capture')
def capture():
    return render_template('capture.html')

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    images = data.get('images', [])
    username = data.get('username', '')

    # Here, you would handle saving the images and username to your database or filesystem
    print(f"Received {len(images)} images for user '{username}'")

    return jsonify({'message': 'Images received successfully'})

if __name__ == '__main__':
    socketio.run(app, debug=True)
