import os
import io
import errno
from app import app
from flask import Flask, flash, request, redirect, render_template
from werkzeug.utils import secure_filename

from config import settings


def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in settings.ALLOWED_EXTENSIONS

def unzip(zip_file, extraction_path):
    """
    code to unzip files
    """
    print("[INFO] Unzipping")
    try:
        files = []
        with zipfile.ZipFile(zip_file, "r") as z:
            for fileinfo in z.infolist():
                filename = fileinfo.filename
                dat = z.open(filename, "r")
                files.append(filename)
                outfile = os.path.join(extraction_path, filename)
                if not os.path.exists(os.path.dirname(outfile)):
                    try:
                        os.makedirs(os.path.dirname(outfile))
                    except OSError as exc:  # Guard against race condition
                        if exc.errno != errno.EEXIST:
                            print("\n[WARN] OS Error: Race Condition")
                if not outfile.endswith("/"):
                    with io.open(outfile, mode='wb') as f:
                        f.write(dat.read())
                dat.close()
        return files
    except Exception as e:
        print("[ERROR] Unzipping Error") + str(e)

@app.route('/', methods=['GET'])
def upload_form():
	return render_template('upload.html')

@app.route('/uploads', methods=['POST'])
def upload_file():
	if request.method == 'POST':
		extraction_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "uploads")
		if 'file' not in request.files:
			flash('No file part')
			return redirect("No file part")
		file_uploaded = request.files['file']
		if file_uploaded.filename == '':
			flash('No file selected for uploading')
			return redirect("No file selected for uploading")
		if file and allowed_file(file_uploaded.filename):
			filename = secure_filename(file_uploaded.filename)
			write_to_file = os.path.join(extraction_path, filename)
			file_uploaded.save(write_to_file)
			unzip(write_to_file, extraction_path)
			flash('File successfully uploaded')
			return "Successfully uploaded"

if __name__ == "__main__":
    app.run()