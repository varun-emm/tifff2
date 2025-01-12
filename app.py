from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
from werkzeug.utils import secure_filename
import zipfile

app = Flask(__name__)

# Configure upload folders
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['BACKUP_FOLDER'] = 'static/uploadsbck'

# Ensure the upload directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['BACKUP_FOLDER'], exist_ok=True)

@app.route('/')
def page1():
    return render_template('page1.html')

@app.route('/upload_page1', methods=['POST'])
def upload_page1():
    text = request.form['text']
    image = request.files['image']

    if image and text:
        image_filename = secure_filename(image.filename)
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
        image.save(image_path)

        # ---- Print to console (terminal) ----
        print(f"\nSubmitted Text: {text}")

        # Generate a full URL to the uploaded_file route. This requires the /uploads/<filename> route below
        image_link = url_for('uploaded_file', filename=image_filename, _external=True)
        print(f"Image Link: {image_link}\n")

        # Now create a text file with the content
        text_filename = 'submitted_text.txt'
        text_path = os.path.join(app.config['UPLOAD_FOLDER'], text_filename)
        with open(text_path, 'w') as text_file:
            text_file.write(text)

        # Create a ZIP file for the uploads
        zip_filename = 'submission.zip'
        zip_path = os.path.join(app.config['UPLOAD_FOLDER'], zip_filename)
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            zipf.write(image_path, image_filename)
            zipf.write(text_path, text_filename)

        print(f'Zip file created: {zip_path}')

        return redirect(url_for('page3'))

@app.route('/page2')
def page2():
    return render_template('page2.html')

@app.route('/upload_page2', methods=['POST'])
def upload_page2():
    image = request.files['image']

    if image:
        image_filename = secure_filename(image.filename)
        image_path = os.path.join(app.config['BACKUP_FOLDER'], image_filename)
        image.save(image_path)

    return redirect(url_for('page3'))

@app.route('/page3')
def page3():
    images = os.listdir(app.config['BACKUP_FOLDER'])
    return render_template('page3.html', images=images)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/reset')
def reset():
    for folder in [app.config['UPLOAD_FOLDER'], app.config['BACKUP_FOLDER']]:
        for file in os.listdir(folder):
            file_path = os.path.join(folder, file)
            if os.path.isfile(file_path):
                os.unlink(file_path)
    return redirect(url_for('page1'))

if __name__ == '__main__':
    app.run(debug=True)
