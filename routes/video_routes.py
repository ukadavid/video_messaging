# routes/video_routes.py

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
    data = request.get_json()
    user_id = data.get('user_id')
    video_url = data.get('video_url')
    title = data.get('title')
    description = data.get('description')

    user = User.query.get(user_id)
    if not user:
        return jsonify(message='User not found'), 404

    # Upload the video to Cloudinary
    try:
        upload_response = cloudinary.uploader.upload(video_url)
        cloudinary_url = upload_response['secure_url']
    except Exception as e:
        return jsonify(message='Failed to upload video to Cloudinary'), 500

    new_video = Video(
        user_id=user_id,
        video_url=cloudinary_url,  # Store the Cloudinary URL
        title=title,
        description=description
    )
    db.session.add(new_video)
    db.session.commit()

    return jsonify(message='Video uploaded to Cloudinary and database successfully'), 201
