import os
import io
from google.cloud import vision
from flask import Flask, request, render_template, send_from_directory

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=['POST'])
def upload():
    target = os.path.join(APP_ROOT, 'images')
    print(target)

    if not os.path.isdir(target):
        os.mkdir(target)

    for file in request.files.getlist("file"):
        print(file)
        filename = file.filename
        destination = "/".join([target, filename])
        print(destination)
        file.save(destination)

    return render_template("caption.html")

vision_client = vision.Client()
file_name = filename

with io.open(file_name, 'rb') as image_file:
    content = image_file.read()
    image = vision_client.image(
        content=content, )

labels = image.detect_labels()
for label in labels:
    print(label.description)
