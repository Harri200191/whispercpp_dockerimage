import socket
from flask import Flask, request, jsonify
import subprocess
import os
import tempfile
import re

app = Flask(__name__)

@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    if 'file' not in request.files:
        return jsonify(error="No file part"), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify(error="No selected file"), 400
 
    temp = tempfile.NamedTemporaryFile(delete=False)
    file.save(temp.name)
    temp.close()
 
    converted_temp = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
    print(temp.name)
    print(converted_temp.name)
    subprocess.run([
        "ffmpeg.exe", "-i", "./test.mp3",
        "-ar", "16000",
        "-acodec", "pcm_s16le",
        "./Test.wav"
    ], check=True)
    os.remove(temp.name)   
 
    result = subprocess.run(["./main.exe", "-m", "./ggml-base.en.bin", "./Test.wav", "-osrt"], capture_output=True, text=True)
    
    app.logger.info(f"Return code: {result.returncode}")
    if result.returncode != 0:
        app.logger.error(f"Error output: {result.stderr}")

    transcription = result.stdout if result.returncode == 0 else "Error in transcription"
 
    srt_file_path = converted_temp.name.replace('.wav', '.srt')
    with open("Test.wav.srt", 'r') as srt_file:
        lines = srt_file.readlines()
        transcription = ''
        for line in lines:
            if line.strip().isdigit():
                continue
            elif line.strip() == '':
                transcription += '\n'  
            else:
                transcription += line.strip() + ' '

    os.remove("./Test.wav")
    if result.returncode == 0: 
        print('Transcription',transcription)
        return jsonify(transcription=transcription)
    else:
        return jsonify(error="Error in transcription"), 50

def parse_transcription(transcription):
    pattern = re.compile(r'\[(\d{2}:\d{2}:\d{2}\.\d{3}) --> (\d{2}:\d{2}:\d{2}\.\d{3})\](.*?)\n', re.DOTALL)
    matches = pattern.findall(transcription)
    parsed_transcription = []
    for start_time, end_time, text in matches:
        text = text.strip()
        entry = {
            "start_time": start_time,
            "end_time": end_time,
            "text": text
        }
        parsed_transcription.append(entry)
    return parsed_transcription

if __name__ == '__main__':
    app.run(debug = False)