
from flask import Flask, flash, request, redirect, url_for, jsonify, render_template
from werkzeug.utils import secure_filename

import os

from google.cloud import vision


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/app/cred.json"

#os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "cred.json"

UPLOAD_FOLDER = 'images/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

APP_VERSION = 0.1


def detect_labels(path):
    """Detects labels in the file."""
    from google.cloud import vision
    import io
    client = vision.ImageAnnotatorClient()

    # [START vision_python_migration_label_detection]
    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.label_detection(image=image)
    labels = response.label_annotations
    print('Labels:')
    
    for label in labels:
        print(label.description)

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))
    return labels




#@app.route('/api/image')
def get_from_vision(filename):
    #path = '/app/images/apple.jpg' + filename
    path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    response = detect_labels(path)
    #     client = vision.ImageAnnotatorClient()
    #     response = client.annotate_image({
    #         'image': {'source': {'image_uri': 'gs://fruit-360/fruits-360/Training/Apple Braeburn/154_100.jpg'}},
    #         'features': [{'type': vision.enums.Feature.Type.FACE_DETECTION}],
    #     })
    return response
    





def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/uploadFile', methods=['GET', 'POST'])
def upload_file():
    print(request)
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            #return "%s" %(filename)
            response = get_from_vision(filename)
            #return "RESPONSE %s" %(str(response))
            return render_template('output.html', response=response)

            #redirect(url_for('/api/image', filename=filename))
    #return ''


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    #upload_file(request)
    name = os.uname().nodename
    return render_template('index.html', name=name)









@app.route('/api/version')
def api_version():
    return 'Api version: %s' %(str(APP_VERSION))

if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='0.0.0.0', port=80, debug=True)
