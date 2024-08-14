from flask import Flask, send_file, request, jsonify
from dotenv import load_dotenv
import boto3
import os
import tempfile

path = ".env"
load_dotenv(dotenv_path=path)

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def hello_polly():
    # Get the 'text' parameter from the request
    query = request.args.get("text")

    if not query:
        return jsonify({"error": "No text provided"}), 400

    # Convert the text to speech
    output_file_path = text_to_speech(query)

    if output_file_path:
        return send_file(
            output_file_path,
            mimetype="audio/mp3",
            as_attachment=True,
            download_name="polly_speech.mp3",
        )
    else:
        return jsonify({"error": "Failed to generate speech"}), 500

def text_to_speech(text):
    polly = boto3.client(
        "polly",
        region_name="us-east-1",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )

    try:
        # Synthesize speech from the provided text
        response = polly.synthesize_speech(Text=text, OutputFormat="mp3", VoiceId="Aditi")

        if "AudioStream" in response:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio_file:
                temp_audio_file.write(response["AudioStream"].read())
                return temp_audio_file.name
        else:
            return None

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

if __name__ == "__main__":
    app.run()
