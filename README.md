# cap.py

Uploading a photo to your favorite social media platform is always a struggle when you can't think of the perfect caption. With cap.py, never worry again that your caption is holding back your image from getting the attention it deserves. 

Start by choosing the picture you want to capture. 
After uploading, your image will be paired with one of the generated captions. If you think that the first one doesn't fit your needs, you can regenerate another caption.

**View a live demo [here](http://cappy.pythonanywhere.com/)!**

### Instructions to run the app locally
```
virtualenv --no-site-packages --distribute .venv && source .venv/bin/activate && pip install -r requirements.txt
export FLASK_APP="main.py"
flask run
```
### If you run into errors:
Set Credentials:
> export GOOGLE_APPLICATION_CREDENTIALS=apikey.json  

Install required :
> sudo pip install google-cloud==0.27  

Install BeatifulSoup:
> sudo pip install bs4

Install Giphy:
> sudo pip install giphy_client

_Written by Abel and the Kids_
