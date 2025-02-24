# ----------------- Write your code below this line. -------------------- #

import os
from io import BytesIO

from flask import Flask, render_template, request # micro-framework for Python that makes it easier to create web apps

from config import config
from hotdogclassifier import HotDogClassifier



app = Flask(__name__) # Creating an instance means that we’re saying app is an object of Flask and can use any of its methods

model = HotDogClassifier()
model.load_model(config["model_weight"])



# In Flask we have a decorator, a feature that adds functionality to the code, called route().
#  This decorator tells Flask which functions should be loaded based on the URL accessed.
# Here we want it to call template
@app.route("/", methods=["GET"])
def home():
    return render_template("index.html", flag=False, project_description=config["project_description"], project_name=config["project_name"])

# setting the flag = False will make sure that the image only shows up when it’s been uploaded


@app.route("/", methods=["POST"])  # this decorator wats image upload so its POST
def classify():
        uploaded_file = request.files["files"]
        data = BytesIO(uploaded_file.read())      # we convert it to a series of bytes
        if uploaded_file.filename != "":          # check if image is uploaded
            img, predicted = model.predict(data)
        else:
            predicted, img = "", ""
        return render_template("index.html", predicted=predicted, img=img, flag=True, project_description=config["project_description"], project_name=config["project_name"])



# ----------------- You do NOT need to understand what the code below does. -------------------- #

if __name__ == '__main__':
    PORT = os.environ.get('PORT') or 8080
    DEBUG = os.environ.get('DEBUG') != 'TRUE'
    app.run(host='0.0.0.0', port=PORT, debug=DEBUG)
