from app import app
from flask import Flask, flash, request, redirect, render_template, Blueprint
from werkzeug.utils import secure_filename
import cv2
import numpy as np
import io
from PIL import Image
import base64
from Helpers import *
from urllib.parse import quote as url_quote

main = Blueprint(
    'main', __name__,
)

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return render_template("home.html")
                

@app.route('/resize')
def upload_form_resize():
    return render_template('upload_resize.html')


@app.route('/resize', methods=['GET', 'POST'])
def upload_image_resize():
    images = []
    height = request.form.get("dim1")
    print("height: ", height)
    height = int(height)
    length = request.form.get("dim2")
    length = int(length)
    print("length: ", length)

    
    for file in request.files.getlist("file[]"):
        print("***************************")
        print("image: ", file)
        if file.filename == '':
            flash('No image selected for uploading')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filestr = file.read()
            npimg = np.frombuffer(filestr, np.uint8)
            image = cv2.imdecode(npimg, cv2.IMREAD_UNCHANGED)
            ratio = image.shape[0] / 500.0
            orig = image.copy()
            image = Helpers.resize(image, height = 500)

            img_resized = cv2.resize(image, (height, length))
            file_object = io.BytesIO()
            img= Image.fromarray(Helpers.resize(img_resized,width=500))
            img.save(file_object, 'PNG')
            base64img = "data:image/png;base64,"+base64.b64encode(file_object
                                 .getvalue()).decode('ascii')
            images.append([base64img])

    print("New image size:", img_resized.shape)
    return render_template('upload_resize.html', images=images )
    #return render_template(url_for('upload_form_resize'))


@app.route('/blur')
def upload_form_blur():
    return render_template('upload_blur.html')

@app.route('/blur', methods=['POST'])
def upload_image_blur():
    images = []
    for file in request.files.getlist("file[]"):
        print("***************************")
        print("image: ", file)
        if file.filename == '':
            flash('No image selected for uploading')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filestr = file.read()
            npimg = np.frombuffer(filestr, np.uint8)
            image = cv2.imdecode(npimg, cv2.IMREAD_UNCHANGED)
            ratio = image.shape[0] / 500.0
            orig = image.copy()
            image = Helpers.resize(image, height = 500)

            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            fm = cv2.Laplacian(gray, cv2.CV_64F).var()
            result = "Not Blurry"

            if fm < 100:
                result = "Blurry"

            sharpness_value = "{:.0f}".format(fm)
            message = [result,sharpness_value]

            img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            file_object = io.BytesIO()
            img= Image.fromarray(Helpers.resize(img,width=500))
            img.save(file_object, 'PNG')
            base64img = "data:image/png;base64,"+base64.b64encode(file_object.getvalue()).decode('ascii')
            images.append([message,base64img])

    print("images:", len(images))
    return render_template('upload_blur.html', images=images)

@app.route('/grayscale')
def upload_form():
    return render_template('upload_grayscale.html')


@app.route('/grayscale', methods=['POST'])
def upload_image():
    images = []
    for file in request.files.getlist("file[]"):
        print("***************************")
        print("image: ", file)
        if file.filename == '':
            flash('No image selected for uploading')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filestr = file.read()
            npimg = np.frombuffer(filestr, np.uint8)
            image = cv2.imdecode(npimg, cv2.IMREAD_UNCHANGED)
            ratio = image.shape[0] / 500.0
            orig = image.copy()
            image = Helpers.resize(image, height = 500)

            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            file_object = io.BytesIO()
            img= Image.fromarray(Helpers.resize(gray,width=500))
            img.save(file_object, 'PNG')
            base64img = "data:image/png;base64,"+base64.b64encode(file_object.getvalue()).decode('ascii')
            images.append([base64img])

    print("images:", len(images))
    return render_template('upload_grayscale.html', images=images )
    

if __name__ == "__main__":
    app.run(debug=True)