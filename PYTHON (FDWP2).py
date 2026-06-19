from flask import Flask, jsonify, render_template, Response
import cv2
import os
from datetime import datetime

app = Flask(__name__)

# 1. Snapshots folder
folder_name = "Snapshots"
os.makedirs(folder_name, exist_ok=True)

# 2. Camera start karo (index 1 aapke system ke hisaab se)
cap = cv2.VideoCapture(0)

# 3. MJPEG stream ke liye frames generate karne wala function
def generate_frames():
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

# 4. Home page
@app.route('/')
def index():
    return render_template('index.html')

# 5. Live video stream route — HTML me <img src="/video_feed"> yahi use karta hai
@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

# 6. Snapshot save karo
@app.route('/save_photo', methods=['POST'])
def save_photo():
    ret, frame = cap.read()
    if ret:
        filename = datetime.now().strftime("snapshot_%Y%m%d_%H%M%S.jpg")
        filepath = os.path.join(folder_name, filename)
        cv2.imwrite(filepath, frame)
        return jsonify({"message": f"Success! Photo saved as {filename} in folder."})
    else:
        return jsonify({"message": "Error: Camera se photo nahi aayi!"}), 500

if __name__ == '__main__':
    # host='0.0.0.0' — poore network pe accessible (localhost bhi chalega)
    # Pehle wala 'http://localhost:5000' galat tha, sirf IP/hostname chahiye
    app.run(host='0.0.0.0', port=5000, debug=True)
