import cloudinary
import os
from flask import Blueprint, request, jsonify
from models.video import Video, db
from models.user import User

video_bp = Blueprint('video', __name__)

# Configure Cloudinary using environment variables
cloudinary.config(
    cloud_name=os.environ.get('CLOUDINARY_CLOUD_NAME'),
    api_key=os.environ.get('CLOUDINARY_API_KEY'),
    api_secret=os.environ.get('CLOUDINARY_API_SECRET')
)

@video_bp.route('/upload', methods=['POST'])
def upload_video():
    user_id = request.form.get('user_id')
    title = request.form.get('title')
    description = request.form.get('description')

    user = User.query.get(user_id)
    if not user:
        return jsonify(message='User not found'), 404

    # Check if a file was uploaded
    if 'video' not in request.files:
        return jsonify(message='No video file provided'), 400

    video_file = request.files['video']

    # Check if the file has a valid extension (e.g., mp4)
    allowed_extensions = {'mp4', 'avi', 'mkv'}  # Add more as needed
    if '.' in video_file.filename and video_file.filename.rsplit('.', 1)[1].lower() not in allowed_extensions:
        return jsonify(message='Invalid file extension'), 400

    # Upload the video file to Cloudinary
    try:
        upload_response = cloudinary.uploader.upload(video_file)
        cloudinary_url = upload_response['secure_url']
    except Exception as e:
        return jsonify(message='Failed to upload video'), 500

    new_video = Video(
        user_id=user_id,
        video_url=cloudinary_url,  # Store the Cloudinary URL
        title=title,
        description=description
    )
    db.session.add(new_video)
    db.session.commit()

    return jsonify(message='Video uploaded successfully'), 201
