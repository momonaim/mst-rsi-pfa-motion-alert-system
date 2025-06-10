import socket

import cv2
from dotenv import load_dotenv
from flask import Flask, send_file, Response, render_template
import os
import smtplib
import threading
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

app = Flask(__name__)

# Path to temporarily save the captured photo
photo_path = 'photo_lowres.jpg'

# Load environment variables from .env file
load_dotenv()

# Email configuration
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT"))

# Shared webcam instance and frame
camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
latest_frame = None
lock = threading.Lock()

# Background thread to read frames
def camera_reader():
    global latest_frame
    while True:
        ret, frame = camera.read()
        if ret:
            with lock:
                latest_frame = frame
        time.sleep(0.05)  # ~20 FPS

# Start camera thread
threading.Thread(target=camera_reader, daemon=True).start()

def record_video(output_path='clip.mp4', duration=5, fps=20):
    width  = int(camera.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT))

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    start_time = time.time()
    while time.time() - start_time < duration:
        with lock:
            ret, frame = camera.read()
        if not ret:
            break
        out.write(frame)
        time.sleep(1 / fps)

    out.release()


@app.route('/take_photo')
def take_photo():
    with lock:
        if latest_frame is None:
            return "No frame captured", 500
        # Save frame with lower JPEG quality
        cv2.imwrite(photo_path, latest_frame, [int(cv2.IMWRITE_JPEG_QUALITY), 50])
    return send_file(photo_path, mimetype='image/jpeg', as_attachment=True)


@app.route('/stream')
def stream():
    return render_template('stream.html')

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/video_feed')
def video_feed():
    def generate():
        while True:
            with lock:
                if latest_frame is None:
                    continue
                _, jpeg = cv2.imencode('.jpg', latest_frame)
                frame = jpeg.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
            time.sleep(0.05)  # ~20 FPS

    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/alert')
def alert_and_send_email():
    video_path = "clip.mp4"

    # Save the current frame as a photo
    with lock:
        if latest_frame is None:
            return "No frame available", 500
        cv2.imwrite(photo_path, latest_frame, [int(cv2.IMWRITE_JPEG_QUALITY), 50])

    # Record a 5-second video
    record_video(video_path, duration=5, fps=24)

    # Get Wi-Fi IP
    def get_wifi_ip():
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(('10.255.255.255', 1))
            IP = s.getsockname()[0]
        except Exception:
            IP = '127.0.0.1'
        finally:
            s.close()
        return IP

    wifi_ip = get_wifi_ip()
    stream_url = f"http://{wifi_ip}:5000/stream"


    try:
        msg = MIMEMultipart()
        msg["Subject"] = "Alerte Sécurité"
        msg["From"] = EMAIL_SENDER
        msg["To"] = EMAIL_RECEIVER

        body_text = f"""\
        Alerte ! Mouvement détecté 🚨

        📷 Une photo est jointe à cet e-mail.
        🔴 Live Stream: {stream_url}
        """

        msg.attach(MIMEText(body_text, "plain"))

        # Attach photo
        with open(photo_path, "rb") as f:
            image = MIMEApplication(f.read(), _subtype="jpeg")
            image.add_header('Content-Disposition', 'attachment', filename=os.path.basename(photo_path))
            msg.attach(image)

        # Attach video
        with open(video_path, "rb") as f:
            video = MIMEApplication(f.read(), _subtype="mp4")
            video.add_header('Content-Disposition', 'attachment', filename=os.path.basename(video_path))
            msg.attach(video)

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())
        server.quit()

        return "✅ Email sent with photo and stream link"
    except Exception as e:
        return f"❌ Failed to send email: {e}", 500

if __name__ == '__main__':
    app.run(
        host=os.getenv("FLASK_HOST", "0.0.0.0"),  # Default to 0.0.0.0 if not set
        port=int(os.getenv("FLASK_PORT", "5000")))  # Default to 5000 if not set