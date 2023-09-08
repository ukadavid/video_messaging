from flask import Flask, Blueprint, request, jsonify
import assemblyai as aai
from moviepy.editor import VideoFileClip

app = Flask(__name__)
aai.settings.api_key = "1ad0d21812aa408597e1e986fb33b6d5"
transcriber = aai.Transcriber()

transcribe_bp = Blueprint('transcribe', __name__)

@transcribe_bp.route('/transcribe', methods=['POST'])
def transcribe():
    try:
        if "file" not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        file = request.files["file"]
        if not file.filename:
            return jsonify({"error": "No file selected"}), 400

        video_path = f"uploads/{file.filename}"
        audio_path = f"uploads/{file.filename.replace('.mp4', '.wav')}"

        file.save(video_path)

        video_clip = VideoFileClip(video_path)
        audio_clip = video_clip.audio
        audio_clip.write_audiofile(audio_path)
        audio_clip.close()
        video_clip.close()

        with open(audio_path, "rb") as f:
            result = transcriber.transcribe(audio=f)

        transcript = ""
        for utterance in result.get("utterances", []):
            for word in utterance.get("words", []):
                transcript += word["text"] + " "

        return jsonify({"transcript": transcript}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500