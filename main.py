import os
import io
import base64
import emoji
import unicodedata
#
import requests
import time
import giphy_client
from giphy_client.rest import ApiException
from pprint import pprint
#
from bs4 import BeautifulSoup
from google.cloud import vision
from flask import Flask, request, render_template, send_from_directory
from werkzeug.utils import secure_filename

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

api_instance = giphy_client.DefaultApi()
api_key = 'dc6zaTOxFJmzC'

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=['POST'])
def upload():
    target = os.path.join(APP_ROOT, 'static')
    print(target)
    filename = ""
    destination = ""
    if not os.path.isdir(target):
        os.mkdir(target)

    if not request.files.get('file', None):
        return 'No selected file'

    file = request.files.getlist("file")[0]
    filename = secure_filename(file.filename)
    destination = "/".join([target, filename])
    file.save(destination)

    labels = googlecloud(destination)
    #######
    memeSearch(labels[0].description)
    #######

    # create a list of emojis 
    emojis = []
    for i in range(3):
        e = getEmoji(labels[i].description)
        string_emoji = repr(e)
        emojis.append(string_emoji)
    print (emojis)
    quotes = []
    for label in labels:
        quotes.extend(getQuotes(label.description)[:3])

    for quote in quotes:
        quote + emojis

    encoded_string = ""
    with open(destination, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    os.remove(destination)
    return render_template("caption.html", quotes = quotes, image = encoded_string)

def googlecloud(destination):
    vision_client = vision.Client()
    file_name = destination

    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()
        image = vision_client.image(
        content=content, )

    labels = image.detect_labels()
    #for label in labels:
    #    print(label.description)
    return labels

def getQuotes(keyword):
    quoteArray = []

    base_url = "http://www.brainyquote.com/quotes/keywords/"
    url = base_url + keyword + ".html"
    response_data = requests.get(url).text[:]
    soup = BeautifulSoup(response_data, 'html.parser')
    
    for item in soup.find_all("a", class_="b-qt"):
        quoteArray.append(item.get_text().rstrip())

    return quoteArray

def memeSearch(text):
    key = text
    limit = 1

    try: 
    # Search Endpoint
        api_response = api_instance.gifs_search_get(api_key, key, limit=limit)
        #print(api_response.data[0].embed_url)
    except ApiException as e:
        print("Exception when calling DefaultApi->gifs_search_get: %s\n" % e)


def getEmoji(text):
    #words = text.split()
    #for word in words:
        #print emoji.emojize(':'+word+':')
    return emoji.emojize(':'+text+':')
