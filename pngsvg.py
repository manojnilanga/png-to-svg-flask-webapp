import os
from flask import Flask, flash, request, redirect, send_from_directory, render_template
from werkzeug.utils import secure_filename
import subprocess

UPLOAD_FOLDER = './uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
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
            #deleting exisiting files in the folder
            for filename_del in os.listdir(UPLOAD_FOLDER):
                file_path = os.path.join(UPLOAD_FOLDER, filename_del)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                except Exception as e:
                    print('Failed to delete %s. Reason: %s' % (file_path, e))

            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            subprocess.call(['java', '-jar', 'ImageTracer.jar',UPLOAD_FOLDER+filename])
            #file renaming
            new_filename = "".join(filename.split(".")[:-1])
            os.rename(r''+UPLOAD_FOLDER + filename + '.svg', r''+UPLOAD_FOLDER + new_filename + '.svg')
            return send_from_directory(UPLOAD_FOLDER, new_filename+".svg",as_attachment=True)

    return render_template('pngsvg.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=80)
