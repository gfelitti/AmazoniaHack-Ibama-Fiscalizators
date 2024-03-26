from flask import Flask, request, render_template, redirect, url_for, jsonify
from sqlalchemy import distinct
from flask_sqlalchemy import SQLAlchemy
import os
import datetime
from datetime import date, time, datetime
from werkzeug.utils import secure_filename
import boto3
from botocore.exceptions import NoCredentialsError
from dotenv import load_dotenv
import os
import base64
import requests
import json
import logging

load_dotenv()

app = Flask(__name__)

if not app.debug:
    logHandler = logging.FileHandler('flask-app.log')
    logHandler.setLevel(logging.INFO)
    app.logger.addHandler(logHandler)
    app.logger.setLevel(logging.INFO)
    
PSQL_URI = os.getenv("PSQL_URI")
app.config['SQLALCHEMY_DATABASE_URI'] = PSQL_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
S3_BUCKET = os.getenv("S3_BUCKET")
S3_KEY_PREFIX = os.getenv("S3_KEY_PREFIX", "")
OPENAI_KEY=os.getenv("OPENAI_KEY")
PROMPT_VISION=os.getenv("PROMPT_VISION")

def encode_image(file_storage):
    file_stream = file_storage.stream
    file_stream.seek(0)
    return base64.b64encode(file_stream.read()).decode('utf-8')

headers_CV = {
  "Content-Type": "application/json",
  "Authorization": f"Bearer {OPENAI_KEY}"
}


s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

class Image(db.Model):
    __tablename__ = 'images'
    
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    file_url = db.Column(db.Text, nullable=False)
    upload_date = db.Column(db.Date, default=date.today)
    upload_time = db.Column(db.Time, default=time)
    picture_date = db.Column(db.Date)
    picture_time = db.Column(db.Time)
    coordinates_dms = db.Column(db.String(255))
    description = db.Column(db.Text)

    def __init__(self, filename, file_url, upload_date, upload_time, 
                 picture_date=None, picture_time=None, coordinates_dms=None, description=None):
        self.filename = filename
        self.file_url = file_url
        self.upload_date = upload_date
        self.upload_time = upload_time
        self.picture_date = picture_date
        self.picture_time = picture_time
        self.coordinates_dms = coordinates_dms
        self.description = description

    def __repr__(self):
        return f'<Image {self.filename}>'
    
    
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/upload', methods=['POST'])
def upload_files():
    uploaded_files = request.files.getlist('files')
    successful_uploads = 0

    for file in uploaded_files:
        if file and file.filename:
            filename = secure_filename(file.filename)
            file_key = f"{S3_KEY_PREFIX}/{filename}" if S3_KEY_PREFIX else filename
            
            #implementar openai
            image_base64 = encode_image(file)
            payload_CV = {
                    "model": "gpt-4-vision-preview",
                    "messages": [
                        {
                        "role": "user",
                            "content": [
                                {
                            "type": "text",
                            "text": PROMPT_VISION
                                },
                            {
                                "type": "image_url",
                                "image_url": {
                                "url": f"data:image/jpeg;base64,{image_base64}"
                            }}]}],    "max_tokens": 300}
            response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers_CV, json=payload_CV)
            a=response.json()
            b=a['choices'][0]['message']['content']
            try:
                c=json.loads(b)
            except json.decoder.JSONDecodeError:
                c={'coordinates_DMS': None, 'date_picture': None, 'time_picture': None}
            
            try:
                file.stream.seek(0)
                s3_client.upload_fileobj(
                    file,
                    S3_BUCKET,
                    file_key
                )   
                new_image = Image(filename=filename, 
                                  file_url= f"https://{S3_BUCKET}.s3.amazonaws.com/{file_key}"
, 
                                  upload_date=date.today(), 
                                  upload_time=datetime.now().time(),
                                  picture_date=c['date_picture'],
                                  picture_time=c['time_picture'],
                                  coordinates_dms=c['coordinates_DMS'])
                db.session.add(new_image)
                db.session.commit()
                successful_uploads += 1
            except Exception as e:
                print(f"Failed to upload {filename}: {e}")
    return render_template('upload_success.html', num_files=successful_uploads)


@app.route('/gallery')
def gallery():
    try:
        bucket_contents = s3_client.list_objects_v2(Bucket=S3_BUCKET, Prefix=S3_KEY_PREFIX)
        images = []
        for obj in bucket_contents.get('Contents', []):
            if obj['Key'].lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                #image_url = f"https://{S3_BUCKET}.s3.amazonaws.com/{obj['Key']}"
                #images.append({'key': obj['Key'], 'url': image_url})
                presigned_url = s3_client.generate_presigned_url('get_object', Params={'Bucket': S3_BUCKET, 'Key': obj['Key']}, ExpiresIn=3600)
                images.append({'key': obj['Key'], 'url': presigned_url})
    except NoCredentialsError:
        images = []
        print("No credentials to access S3")

    return render_template('gallery.html', images=images)
    

@app.route('/photos')
def get_photos():
    date_str = request.args.get('upload_date')  # Formato esperado: 'YYYY-MM-DD'

    try:
        if date_str:
            upload_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            photos = Image.query.filter_by(upload_date=upload_date).all()
        else:
            photos = Image.query.all()
    except ValueError:
        return jsonify({'error': 'Not valid date. Use the format YYYY-MM-DD'}), 400

    photos_data = [{
        'id': photo.id,
        'filename': photo.filename,
        'file_url': photo.file_url,
        'upload_date': photo.upload_date.isoformat() if photo.upload_date else None,
        'upload_time': photo.upload_time.isoformat() if photo.upload_time else None,
        'picture_date': photo.picture_date.isoformat() if photo.picture_date else None,
        'picture_time': photo.picture_time.isoformat() if photo.picture_time else None,
        'coordinates_dms': photo.coordinates_dms,
        'description': photo.description
    } for photo in photos]

    return jsonify(photos_data)

@app.route('/map')
def mapview():
    return render_template('map.html')

with app.app_context():
    db.create_all()
    
if __name__ == '__main__':
    
    app.run(debug=True)
