from flask import Flask, render_template, Response, jsonify
import cv2
import time

app = Flask(__name__)

VIDEO_PATH = "templates_media/clips/runout1.mp4"
SPRITE_PATH = "templates_media/sprites/"

cap = cv2.VideoCapture(VIDEO_PATH)
frame_pos = 0

mode = "video"      # video / image
current_image = None


def frame_generator():
    global frame_pos, mode, current_image

    while True:
        if mode == "video":
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_pos)
            success, frame = cap.read()
            if not success:
                continue
        else:
            frame = cv2.imread(SPRITE_PATH + current_image)

        _, buffer = cv2.imencode(".jpg", frame)
        frame_bytes = buffer.tobytes()

        yield (b"--frame\r\n"
               b"Content-Type: image/jpeg\r\n\r\n" +
               frame_bytes + b"\r\n")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/video_feed")
def video_feed():
    return Response(
        frame_generator(),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )


@app.route("/control/<action>")
def control(action):
    global frame_pos, mode, current_image

    if action == "next_fast":
        frame_pos += 15
        mode = "video"

    elif action == "next_slow":
        frame_pos += 1
        mode = "video"

    elif action == "prev_fast":
        frame_pos = max(0, frame_pos - 15)
        mode = "video"

    elif action == "prev_slow":
        frame_pos = max(0, frame_pos - 1)
        mode = "video"

    elif action == "out":
        mode = "image"
        current_image = "drs_out.png"

    elif action == "not_out":
        mode = "image"
        current_image = "drs_not_out.png"

    elif action == "decision":
        mode = "image"
        current_image = "drs_decision.png"

    elif action == "sponsor":
        mode = "image"
        current_image = "sponsor.png"

    return jsonify(status="ok")


@app.route("/sequence/<decision>")
def sequence(decision):
    global mode, current_image

    mode = "image"
    current_image = "drs_decision.png"
    time.sleep(1.5)

    current_image = "sponsor.png"
    time.sleep(1.2)

    if decision == "out":
        current_image = "drs_out.png"
    else:
        current_image = "drs_not_out.png"

    return jsonify(status="done")


if __name__ == "__main__":
    app.run(debug=True)
