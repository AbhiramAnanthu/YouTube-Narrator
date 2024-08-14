from flask import Flask, send_file, request
from IPython.display import Audio
from dotenv import load_dotenv
from io import BytesIO
import boto3
import os

path = ".env"
load_dotenv(dotenv_path=path)

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def hello_polly():
    if request.method == "GET":
        query = request.args.get("text")
        output_file = text_to_speech(query)

        return send_file(
            output_file,
            mimetype="audio/wav",
            as_attachment=True,
            download_name="polly_speech.wav",
        )


def text_to_speech(text):
    polly = boto3.client(
        "polly",
        region_name="us-east-1",
        aws_access_key_id=os.getenv("AWS_SECRET_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_KEY"),
    )

    response = polly.synthesize_speech(Text=text, OutputFormat="mp3", VoiceId="Aditi")
    if "AudioStream" in response:
        with response["AudioStream"] as stream:
            output_file = "speech.mp3"
            try:
                # Open a file for writing the output as a binary stream
                with open(output_file, "wb") as file:
                    file.write(stream.read())
            except IOError as error:
                # Could not write to file, exit gracefully
                print(error)
    else:
        # The response didn't contain audio data, exit gracefully
        print("Could not stream audio")

    return output_file
