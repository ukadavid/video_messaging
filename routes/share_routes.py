

from flask import Blueprint, request, jsonify
from models.share import Share, db
from models.video import Video
from models.user import User

share_bp = Blueprint('share', __name__)

@share_bp.route('/share', methods=['POST'])
def share_video():
    data = request.get_json()
    user_id = data.get('user_id')
    video_id = data.get('video_id')
    
    user = User.query.get(user_id)
    video = Video.query.get(video_id)

    if not user or not video:
        return jsonify(message='User or Video not found'), 404

    # Create a new share record
    new_share = Share(user_id=user_id, video_id=video_id)
    db.session.add(new_share)
    db.session.commit()

    return jsonify(message='Video shared successfully'), 201

@share_bp.route('/shared_videos/<int:user_id>', methods=['GET'])
def get_shared_videos(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify(message='User not found'), 404

    shared_videos = (
        db.session.query(Video)
        .join(Share, Share.video_id == Video.id)
        .filter(Share.user_id == user_id)
        .all()
    )

    video_list = []
    for video in shared_videos:
        video_info = {
            'video_url': video.video_url,
            'title': video.title,
            'description': video.description,
            'share_date': video.shares[0].share_date.strftime('%Y-%m-%d %H:%M:%S')
        }
        video_list.append(video_info)

    return jsonify(videos=video_list), 200
