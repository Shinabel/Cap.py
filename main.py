import os
import io
import base64
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
    """
    first page users will see.
    """
    return render_template("index.html")

@app.route("/loading", methods=['POST'])
def loading():
    """
    creates a page loading page that shows a GIFs relevant to the
    inserted image.
    """
    target = os.path.join(APP_ROOT, 'static')
    print(target)

    filename = ""
    destination = ""
    if not os.path.isdir(target):
        os.mkdir(target)

    if not request.files.get('file', None):
        return 'No selected file'

    #load the file
    file = request.files.getlist("file")[0]
    filename = secure_filename(file.filename)
    destination = "/".join([target, filename])
    file.save(destination)

    labels = googlecloud(destination)
    stringLabels = ""
    for label in labels:
        stringLabels += label.description + ", "

    #modify the embeded url acquired for better fit in the webpage.
    memeLink = memeSearch(labels[0].description) + "/200.gif"
    memeLink = memeLink.replace("embed", "media")
    memeLink = memeLink.replace("https://", "https://media2.")
    #print (memeLink)

    return render_template("loading.html", gif_link = memeLink, labels = stringLabels, image_destination = destination)

@app.route("/upload", methods=['POST'])
def upload():
    """
    Creates a page with a picture inserted, quotes generated,
    and the key words with hashtag in front of them.
    """
    destination = request.form['destination']
    stringlabels = request.form['labels']
    labels = stringlabels.split(", ")
    labels = labels[:-1]
    quotes = []
    hashtags = ""

    for label in labels:
        #pick 7 quotes from the brainyquote.com.
        quotes.extend(getQuotes(label)[:7])
        # add "#" in front of the key word that were generated from google cloud vision.1
        hashtags += "#" + label.replace(" ", '') + " "

    encoded_string = ""
    with open(destination, "rb") as image_file:
    	encoded_string = base64.b64encode(image_file.read())
    os.remove(destination)
    return render_template("caption.html", quotes = quotes, image = encoded_string, hashtags = hashtags)

def googlecloud(destination):
    """
    Use the google cloud vision to acquire key words that are relevant
    from the inserted image.
    """
    vision_client = vision.Client()
    file_name = destination

    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()
        image = vision_client.image(
        content=content, )

    labels = image.detect_labels()

    #for label in labels:
    #   print(label.description)
    return labels

def getQuotes(keyword):
    """
    Acquire quotes that are relevant to the keyword inserted
    by web scarping (using BeautifulSoup) brainyquote.com
    """
    quoteArray = []

    #url used
    base_url = "http://www.brainyquote.com/quotes/keywords/"
    url = base_url + keyword + ".html"
    response_data = requests.get(url).text[:]
    soup = BeautifulSoup(response_data, 'html.parser')
    
    # loop through the html source code of the website and find specific keys
    for item in soup.find_all("a", class_="b-qt"):
        quoteArray.append(item.get_text().rstrip())

    return quoteArray

def memeSearch(text):
    """
    Using GIPHY API, generate a GIFs that are related to the
    inputted text (key word).
    """
    key = text
    limit = 1

    try: 
    # Search Endpoint
        api_response = api_instance.gifs_search_get(api_key, key, limit=limit)
        print api_response.data[0].embed_url
        return api_response.data[0].embed_url
    except ApiException as e:
        print("Exception when calling gifs_search_get: %s\n" % e)
