# # from datetime import datetime

# # from flask import Flask, render_template, request, redirect, url_for, send_file, send_from_directory
# # from werkzeug.utils import secure_filename

# # import os

# # app = Flask(__name__)

# # # Configure upload folder
# # UPLOAD_FOLDER = 'uploads'
# # ALLOWED_EXTENSIONS = {'wav'}
# # app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# # os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# # def allowed_file(filename):
# #     return '.' in filename and \
# #            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# # def get_files():
# #     files = []
# #     for filename in os.listdir(UPLOAD_FOLDER):
# #         if allowed_file(filename):
# #             files.append(filename)
# #             print(filename)
# #     files.sort(reverse=True)
# #     return files

# # @app.route('/')
# # def index():
# #     files = get_files()
# #     return render_template('index.html', files=files)

# # @app.route('/upload', methods=['POST'])
# # def upload_audio():
# #     if 'audio_data' not in request.files:
# #         flash('No audio data')
# #         return redirect(request.url)
# #     file = request.files['audio_data']
# #     if file.filename == '':
# #         flash('No selected file')
# #         return redirect(request.url)
# #     if file:
# #         # filename = secure_filename(file.filename)
# #         filename = datetime.now().strftime("%Y%m%d-%I%M%S%p") + '.wav'
# #         file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
# #         file.save(file_path)

# #         #
# #         #
# #         # Modify this block to call the speech to text API
# #         # Save transcript to same filename but .txt
# #         #
# #         #

# #     return redirect('/') #success

# # @app.route('/upload/<filename>')
# # def get_file(filename):
# #     return send_file(filename)

    
# # @app.route('/upload_text', methods=['POST'])
# # def upload_text():
# #     text = request.form['text']
# #     print(text)
# #     #
# #     #
# #     # Modify this block to call the stext to speech API
# #     # Save the output as a audio file in the 'tts' directory 
# #     # Display the audio files at the bottom and allow the user to listen to them
# #     #

# #     return redirect('/') #success

# # @app.route('/script.js',methods=['GET'])
# # def scripts_js():
# #     return send_file('./script.js')

# # @app.route('/uploads/<filename>')
# # def uploaded_file(filename):
# #     return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# # if __name__ == '__main__':
# #     app.run(debug=True)

# app.py
# from datetime import datetime
# from flask import Flask, render_template, request, redirect, url_for, send_from_directory
# from werkzeug.utils import secure_filename
# from google.cloud import speech, texttospeech
# import os

# app = Flask(__name__)

# UPLOAD_FOLDER = 'uploads'
# TTS_FOLDER = 'tts'
# ALLOWED_EXTENSIONS = {'wav'}
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.config['TTS_FOLDER'] = TTS_FOLDER

# os.makedirs(UPLOAD_FOLDER, exist_ok=True)
# os.makedirs(TTS_FOLDER, exist_ok=True)

# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# def get_files():
#     files = [f for f in os.listdir(UPLOAD_FOLDER) if allowed_file(f)]
#     files.sort(reverse=True)
#     return files

# def get_tts_files():
#     files = [f for f in os.listdir(TTS_FOLDER) if allowed_file(f)]
#     files.sort(reverse=True)
#     return files

# def transcribe_audio(file_path):
#     client = speech.SpeechClient()
#     with open(file_path, 'rb') as audio_file:
#         content = audio_file.read()
    
#     audio = speech.RecognitionAudio(content=content)
#     config = speech.RecognitionConfig(
#         encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
#         sample_rate_hertz=16000,
#         language_code="en-US",
#     )
    
#     response = client.recognize(config=config, audio=audio)
#     return " ".join(result.alternatives[0].transcript for result in response.results)

# def text_to_speech(text, output_file):
#     client = texttospeech.TextToSpeechClient()
#     synthesis_input = texttospeech.SynthesisInput(text=text)
    
#     voice = texttospeech.VoiceSelectionParams(
#         language_code="en-US",
#         ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
#     )
    
#     audio_config = texttospeech.AudioConfig(
#         audio_encoding=texttospeech.AudioEncoding.LINEAR16
#     )
    
#     response = client.synthesize_speech(
#         input=synthesis_input,
#         voice=voice,
#         audio_config=audio_config
#     )
    
#     with open(output_file, 'wb') as out:
#         out.write(response.audio_content)

# @app.route('/')
# def index():
#     return render_template('index.html', files=get_files(), tts_files=get_tts_files())

# @app.route('/upload', methods=['POST'])
# def upload_audio():
#     if 'audio_data' not in request.files:
#         return redirect('/')
#     file = request.files['audio_data']
#     if file and allowed_file(file.filename):
#         filename = datetime.now().strftime("%Y%m%d-%H%M%S") + '.wav'
#         file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#         file.save(file_path)
        
#         # Generate transcript
#         transcript = transcribe_audio(file_path)
#         transcript_path = os.path.join(app.config['UPLOAD_FOLDER'], filename + '.txt')
#         with open(transcript_path, 'w') as f:
#             f.write(transcript)
    
#     return redirect('/')

# @app.route('/upload_text', methods=['POST'])
# def upload_text():
#     text = request.form['text']
#     if text:
#         filename = datetime.now().strftime("%Y%m%d-%H%M%S") + '.wav'
#         file_path = os.path.join(app.config['TTS_FOLDER'], filename)
#         text_to_speech(text, file_path)
    
#     return redirect('/')

# @app.route('/uploads/<filename>')
# def uploaded_file(filename):
#     return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# @app.route('/tts/<filename>')
# def uploaded_tts_file(filename):
#     return send_from_directory(app.config['TTS_FOLDER'], filename)

# @app.route('/script.js', methods=['GET'])
# def scripts_js():
#     return send_from_directory('.', 'script.js')

# if __name__ == '__main__':
#     app.run(debug=True)

# app.py
# from datetime import datetime
# from flask import Flask, render_template, request, redirect, url_for, send_from_directory
# from werkzeug.utils import secure_filename
# from google.cloud import speech
# import os

# app = Flask(__name__)

# UPLOAD_FOLDER = 'uploads'
# TTS_FOLDER = 'tts'
# ALLOWED_EXTENSIONS = {'wav'}
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.config['TTS_FOLDER'] = TTS_FOLDER

# os.makedirs(UPLOAD_FOLDER, exist_ok=True)
# os.makedirs(TTS_FOLDER, exist_ok=True)

# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# def get_files():
#     files = [f for f in os.listdir(UPLOAD_FOLDER) if allowed_file(f)]
#     files.sort(reverse=True)
#     return files

# def get_tts_files():
#     files = [f for f in os.listdir(TTS_FOLDER) if allowed_file(f)]
#     files.sort(reverse=True)
#     return files

# def transcribe_audio(file_path):
#     """Transcribe audio file using Google Speech-to-Text"""
#     client = speech.SpeechClient()
    
#     with open(file_path, 'rb') as audio_file:
#         content = audio_file.read()
    
#     audio = speech.RecognitionAudio(content=content)
#     config = speech.RecognitionConfig(
#         encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
#         sample_rate_hertz=16000,  # Adjust if your audio has a different sample rate
#         language_code="en-US",
#     )
    
#     try:
#         response = client.recognize(config=config, audio=audio)
#         # Combine all transcript alternatives into one string
#         transcript = " ".join(result.alternatives[0].transcript for result in response.results)
#         return transcript if transcript else "No speech detected"
#     except Exception as e:
#         return f"Error transcribing audio: {str(e)}"

# @app.route('/')
# def index():
#     return render_template('index.html', files=get_files(), tts_files=get_tts_files())

# @app.route('/upload', methods=['POST'])
# def upload_audio():
#     if 'audio_data' not in request.files:
#         return redirect('/')
#     file = request.files['audio_data']
#     if file and allowed_file(file.filename):
#         filename = datetime.now().strftime("%Y%m%d-%H%M%S") + '.wav'
#         file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#         file.save(file_path)
        
#         # Generate transcript from the uploaded audio
#         transcript = transcribe_audio(file_path)
#         transcript_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{filename}.txt")
#         with open(transcript_path, 'w') as f:
#             f.write(transcript)
    
#     return redirect('/')

# @app.route('/upload_text', methods=['POST'])
# def upload_text():
#     # This route remains unchanged for now since we're focusing on audio-to-text
#     text = request.form['text']
#     if text:
#         # Note: This needs text-to-speech implementation which isn't included here
#         # You would need to add Google Text-to-Speech code here
#         filename = datetime.now().strftime("%Y%m%d-%H%M%S") + '.wav'
#         file_path = os.path.join(app.config['TTS_FOLDER'], filename)
#         # Placeholder - actual TTS implementation would go here
#         # For now, we'll just create an empty file
#         with open(file_path, 'wb') as f:
#             f.write(b'')
    
#     return redirect('/')

# @app.route('/uploads/<filename>')
# def uploaded_file(filename):
#     return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# @app.route('/tts/<filename>')
# def uploaded_tts_file(filename):
#     return send_from_directory(app.config['TTS_FOLDER'], filename)

# @app.route('/script.js', methods=['GET'])
# def scripts_js():
#     return send_from_directory('.', 'script.js')

# if __name__ == '__main__':
#     app.run(debug=True)

# app.py
# app.py
# from datetime import datetime
# from flask import Flask, render_template, request, redirect, url_for, send_from_directory
# from werkzeug.utils import secure_filename
# from google.cloud import speech, texttospeech
# import os
# import logging

# app = Flask(__name__)

# UPLOAD_FOLDER = 'uploads'
# TTS_FOLDER = 'tts'
# ALLOWED_EXTENSIONS = {'wav'}
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.config['TTS_FOLDER'] = TTS_FOLDER

# # Set up logging
# logging.basicConfig(level=logging.DEBUG)

# os.makedirs(UPLOAD_FOLDER, exist_ok=True)
# os.makedirs(TTS_FOLDER, exist_ok=True)

# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# def get_files():
#     files = [f for f in os.listdir(UPLOAD_FOLDER) if allowed_file(f)]
#     files.sort(reverse=True)
#     return files

# def get_tts_files():
#     files = [f for f in os.listdir(TTS_FOLDER) if allowed_file(f)]
#     files.sort(reverse=True)
#     return files

# def transcribe_audio(file_path):
#     try:
#         client = speech.SpeechClient()
        
#         with open(file_path, 'rb') as audio_file:
#             content = audio_file.read()
        
#         audio = speech.RecognitionAudio(content=content)
#         config = speech.RecognitionConfig(
#             encoding=speech.RecognitionConfig.AudioEncoding.WEBM_OPUS,  # Changed from LINEAR16
#             sample_rate_hertz=48000,  # Changed from 16000
#             language_code="en-US",
#             enable_automatic_punctuation=True,
#             enable_word_time_offsets=False,
#             model="default",
#         )
        
#         operation = client.long_running_recognize(config=config, audio=audio)
#         response = operation.result(timeout=90)
        
#         transcriptions = []
#         for result in response.results:
#             if result.alternatives:
#                 transcriptions.append(result.alternatives[0].transcript)
        
#         transcript = " ".join(transcriptions)
#         return transcript if transcript else "No transcription available"
        
#     except Exception as e:
#         logging.error(f"Error in transcription: {str(e)}")
#         return f"Error transcribing audio: {str(e)}"

# def text_to_speech(text, output_file):
#     try:
#         client = texttospeech.TextToSpeechClient()
#         synthesis_input = texttospeech.SynthesisInput(text=text)
        
#         voice = texttospeech.VoiceSelectionParams(
#             language_code="en-US",
#             ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
#         )
        
#         audio_config = texttospeech.AudioConfig(
#             audio_encoding=texttospeech.AudioEncoding.LINEAR16,
#             sample_rate_hertz=16000
#         )
        
#         response = client.synthesize_speech(
#             input=synthesis_input,
#             voice=voice,
#             audio_config=audio_config
#         )
        
#         with open(output_file, 'wb') as out:
#             out.write(response.audio_content)
#     except Exception as e:
#         logging.error(f"Error in text-to-speech: {str(e)}")

# @app.route('/')
# def index():
#     return render_template('index.html', files=get_files(), tts_files=get_tts_files())

# @app.route('/upload', methods=['POST'])
# def upload_audio():
#     try:
#         if 'audio_data' not in request.files:
#             return redirect('/')
        
#         file = request.files['audio_data']
#         if file and allowed_file(file.filename):
#             filename = datetime.now().strftime("%Y%m%d-%H%M%S") + '.wav'
#             file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#             file.save(file_path)
            
#             # Generate transcript
#             transcript = transcribe_audio(file_path)
#             transcript_path = os.path.join(app.config['UPLOAD_FOLDER'], filename + '.txt')
#             with open(transcript_path, 'w') as f:
#                 f.write(transcript)
            
#             return redirect('/')
#         return redirect('/')
#     except Exception as e:
#         logging.error(f"Error in upload: {str(e)}")
#         return redirect('/')

# # Rest of your routes remain the same...
# @app.route('/upload_text', methods=['POST'])
# def upload_text():
#     text = request.form['text']
#     if text:
#         filename = datetime.now().strftime("%Y%m%d-%H%M%S") + '.wav'
#         file_path = os.path.join(app.config['TTS_FOLDER'], filename)
#         text_to_speech(text, file_path)
#     return redirect('/')

# @app.route('/uploads/<filename>')
# def uploaded_file(filename):
#     return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# @app.route('/tts/<filename>')
# def uploaded_tts_file(filename):
#     return send_from_directory(app.config['TTS_FOLDER'], filename)

# if __name__ == '__main__':
#     app.run(debug=True)
# Old import

#new
#working
# from datetime import datetime
# from flask import Flask, render_template, request, redirect, url_for, send_from_directory
# from werkzeug.utils import secure_filename
# from google.cloud import speech, texttospeech
# from google.cloud.language_v1 import LanguageServiceClient, Document, types
# import os
# import logging

# app = Flask(__name__)

# UPLOAD_FOLDER = 'uploads'
# TTS_FOLDER = 'tts'
# ALLOWED_EXTENSIONS = {'wav', 'webm'}
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.config['TTS_FOLDER'] = TTS_FOLDER

# # Set up logging
# logging.basicConfig(level=logging.DEBUG)

# os.makedirs(UPLOAD_FOLDER, exist_ok=True)
# os.makedirs(TTS_FOLDER, exist_ok=True)

# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# def get_files():
#     files = [f for f in os.listdir(UPLOAD_FOLDER) if allowed_file(f)]
#     files.sort(reverse=True)
#     return files

# def get_tts_files():
#     files = [f for f in os.listdir(TTS_FOLDER) if allowed_file(f)]
#     files.sort(reverse=True)
#     return files

# def transcribe_audio(file_path):
#     try:
#         client = speech.SpeechClient()
#         with open(file_path, 'rb') as audio_file:
#             content = audio_file.read()
        
#         audio = speech.RecognitionAudio(content=content)
#         config = speech.RecognitionConfig(
#             encoding=speech.RecognitionConfig.AudioEncoding.WEBM_OPUS,
#             sample_rate_hertz=48000,
#             language_code="en-US",
#             enable_automatic_punctuation=True,
#         )
#         operation = client.long_running_recognize(config=config, audio=audio)
#         response = operation.result(timeout=90)
        
#         transcriptions = [result.alternatives[0].transcript for result in response.results if result.alternatives]
#         transcript = " ".join(transcriptions)
#         return transcript if transcript else "No transcription available"
#     except Exception as e:
#         logging.error(f"Error in transcription: {str(e)}")
#         return f"Error transcribing audio: {str(e)}"

# def analyze_sentiment(text):
#     try:
#         client = LanguageServiceClient()
#         document = Document(content=text, type_=Document.Type.PLAIN_TEXT)
#         response = client.analyze_sentiment(request={'document': document})
#         sentiment = response.document_sentiment
#         score = sentiment.score
#         if score > 0.25:
#             return "Positive"
#         elif score < -0.25:
#             return "Negative"
#         else:
#             return "Neutral"
#     except Exception as e:
#         logging.error(f"Error in sentiment analysis: {str(e)}")
#         return f"Error analyzing sentiment: {str(e)}"

# def text_to_speech(text, output_file):
#     try:
#         client = texttospeech.TextToSpeechClient()
#         synthesis_input = texttospeech.SynthesisInput(text=text)
#         voice = texttospeech.VoiceSelectionParams(language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL)
#         audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.LINEAR16, sample_rate_hertz=16000)
#         response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)
#         with open(output_file, 'wb') as out:
#             out.write(response.audio_content)
#     except Exception as e:
#         logging.error(f"Error in text-to-speech: {str(e)}")

# @app.route('/')
# def index():
#     return render_template('index.html', files=get_files(), tts_files=get_tts_files())

# @app.route('/upload', methods=['POST'])
# def upload_audio():
#     try:
#         if 'audio_data' not in request.files:
#             return redirect('/')
#         file = request.files['audio_data']
#         if file and allowed_file(file.filename):
#             filename = datetime.now().strftime("%Y%m%d-%H%M%S") + '.webm'
#             file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#             file.save(file_path)
            
#             # Transcription
#             transcript = transcribe_audio(file_path)
            
#             # Sentiment Analysis
#             sentiment = analyze_sentiment(transcript)
            
#             # Save transcript and sentiment
#             transcript_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{filename}.txt")
#             with open(transcript_path, 'w') as f:
#                 f.write(f"Transcript: {transcript}\nSentiment: {sentiment}")
            
#             return redirect('/')
#         return redirect('/')
#     except Exception as e:
#         logging.error(f"Error in upload: {str(e)}")
#         return redirect('/')

# @app.route('/upload_text', methods=['POST'])
# def upload_text():
#     try:
#         text = request.form['text']
#         if text:
#             filename = datetime.now().strftime("%Y%m%d-%H%M%S") + '.wav'
#             file_path = os.path.join(app.config['TTS_FOLDER'], filename)
#             text_to_speech(text, file_path)
            
#             # Sentiment Analysis
#             sentiment = analyze_sentiment(text)
#             transcript_path = os.path.join(app.config['TTS_FOLDER'], f"{filename}.txt")
#             with open(transcript_path, 'w') as f:
#                 f.write(f"Original Text: {text}\nSentiment: {sentiment}")
            
#             return redirect('/')
#         return redirect('/')
#     except Exception as e:
#         logging.error(f"Error in text upload: {str(e)}")
#         return redirect('/')

# @app.route('/uploads/<filename>')
# def uploaded_file(filename):
#     return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# @app.route('/tts/<filename>')
# def uploaded_tts_file(filename):
#     return send_from_directory(app.config['TTS_FOLDER'], filename)

# @app.route('/script.js', methods=['GET'])
# def scripts_js():
#     return send_from_directory('.', 'script.js')

# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

## Main.py latest code: - 19/03/2025

# from datetime import datetime
# from flask import Flask, render_template, request, redirect, url_for, send_from_directory
# from werkzeug.utils import secure_filename
# from google.cloud import storage
# import vertexai
# from vertexai.generative_models import GenerativeModel
# import os
# import logging

# app = Flask(__name__)

# UPLOAD_FOLDER = 'uploads'
# ALLOWED_EXTENSIONS = {'wav', 'webm'}
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# BUCKET_NAME = "my-audio-bucket-789"  # Replace with your GCS bucket name
# PROJECT_ID = "fifth-glazing-452704-m2"    # Replace with your project ID
# LOCATION = "us-central1"          # Replace with your region if different

# # Set up logging
# logging.basicConfig(level=logging.DEBUG)

# os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# # Initialize Vertex AI
# vertexai.init(project=PROJECT_ID, location=LOCATION)
# model = GenerativeModel("gemini-1.5-flash-002")

# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# def get_files():
#     files = [f for f in os.listdir(UPLOAD_FOLDER) if allowed_file(f)]
#     files.sort(reverse=True)
#     return files

# def upload_to_gcs(file_path, filename):
#     storage_client = storage.Client()
#     bucket = storage_client.bucket(BUCKET_NAME)
#     blob = bucket.blob(filename)
#     blob.upload_from_filename(file_path)
#     return f"gs://{BUCKET_NAME}/{filename}"

# def analyze_audio(file_path):
#     try:
#         # Upload to GCS
#         filename = os.path.basename(file_path)
#         gcs_uri = upload_to_gcs(file_path, filename)

#         # Prepare prompt for Gemini
#         prompt = f"""
#         Please transcribe the audio file at {gcs_uri} and perform sentiment analysis on the transcription.
#         Return the result in the following format:
#         Transcript: [transcription text]
#         Sentiment: [Positive/Negative/Neutral]
#         """
        
#         # Call Gemini API
#         response = model.generate_content(prompt)
#         result = response.text.strip()
        
#         return result
#     except Exception as e:
#         logging.error(f"Error in audio analysis: {str(e)}")
#         return f"Error analyzing audio: {str(e)}"

# @app.route('/')
# def index():
#     return render_template('index.html', files=get_files())

# @app.route('/upload', methods=['POST'])
# def upload_audio():
#     try:
#         if 'audio_data' not in request.files:
#             return redirect('/')
#         file = request.files['audio_data']
#         if file and allowed_file(file.filename):
#             filename = datetime.now().strftime("%Y%m%d-%H%M%S") + '.webm'
#             file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#             file.save(file_path)
            
#             # Analyze audio with Gemini
#             result = analyze_audio(file_path)
            
#             # Save result to text file
#             transcript_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{filename}.txt")
#             with open(transcript_path, 'w') as f:
#                 f.write(result)
            
#             return redirect('/')
#         return redirect('/')
#     except Exception as e:
#         logging.error(f"Error in upload: {str(e)}")
#         return redirect('/')

# @app.route('/uploads/<filename>')
# def uploaded_file(filename):
#     return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# @app.route('/script.js', methods=['GET'])
# def scripts_js():
#     return send_from_directory('.', 'script.js')

# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

#Day latest 22:34 19-03-2024

# from datetime import datetime
# from flask import Flask, render_template, request, redirect, url_for, send_from_directory
# from werkzeug.utils import secure_filename
# from google.cloud import storage
# import vertexai
# from vertexai.generative_models import GenerativeModel, Part
# import os
# import logging

# app = Flask(__name__)

# UPLOAD_FOLDER = 'uploads'
# ALLOWED_EXTENSIONS = {'wav', 'webm'}
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# BUCKET_NAME = "my-audio-bucket-789"  # Replace with your GCS bucket name
# PROJECT_ID = "fifth-glazing-452704-m2"    # Replace with your project ID
# LOCATION = "us-central1"

# # Set up logging
# logging.basicConfig(
#     level=logging.DEBUG,
#     format='%(asctime)s - %(levelname)s - %(message)s',
#     handlers=[
#         logging.FileHandler('app.log'),
#         logging.StreamHandler()
#     ]
# )

# os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# # Initialize Vertex AI
# vertexai.init(project=PROJECT_ID, location=LOCATION)
# model = GenerativeModel("gemini-1.5-flash-002")

# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# def get_files():
#     files = [f for f in os.listdir(UPLOAD_FOLDER) if allowed_file(f)]
#     files.sort(reverse=True)
#     return files

# def upload_to_gcs(file_path, filename):
#     logging.debug(f"Uploading {file_path} to GCS as {filename}")
#     storage_client = storage.Client()
#     bucket = storage_client.bucket(BUCKET_NAME)
#     blob = bucket.blob(filename)
#     blob.upload_from_filename(file_path)
#     return blob

# def analyze_audio(file_path):
#     try:
#         # Upload to GCS and get blob
#         filename = os.path.basename(file_path)
#         blob = upload_to_gcs(file_path, filename)
        
#         # Download audio content locally for Gemini
#         audio_content = blob.download_as_bytes()
#         audio_part = Part.from_data(
#             data=audio_content,
#             mime_type="audio/webm"
#         )

#         # Prepare prompt for Gemini
#         prompt = [
#             audio_part,
#             "Please transcribe the audio and perform sentiment analysis on the transcription. Return the result in this format:\nTranscript: [transcription text]\nSentiment: [Positive/Negative/Neutral]"
#         ]
        
#         # Single call to Gemini
#         response = model.generate_content(prompt)
#         result = response.text.strip()
#         logging.debug(f"Gemini response: {result}")
#         return result
#     except Exception as e:
#         logging.error(f"Error in audio analysis: {str(e)}")
#         if "403" in str(e) and "billing" in str(e).lower():
#             return "Error: Billing account is disabled. Please enable billing in Google Cloud Console."
#         return f"Error analyzing audio: {str(e)}"

# @app.route('/')
# def index():
#     logging.debug("Rendering index page")
#     return render_template('index.html', files=get_files())

# @app.route('/upload', methods=['POST'])
# def upload_audio():
#     logging.debug("Received upload request")
#     try:
#         if 'audio_data' not in request.files:
#             logging.error("No audio_data in request.files")
#             return redirect('/')
#         file = request.files['audio_data']
#         if file and allowed_file(file.filename):
#             filename = datetime.now().strftime("%Y%m%d-%H%M%S") + '.webm'
#             file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#             logging.debug(f"Saving file to {file_path}")
#             file.save(file_path)
            
#             # Analyze audio with Gemini
#             result = analyze_audio(file_path)
#             transcript_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{filename}.txt")
#             with open(transcript_path, 'w') as f:
#                 f.write(result)
#                 logging.debug(f"Saved result to {transcript_path}")
            
#             return redirect('/')
#         logging.error(f"File not allowed: {file.filename}")
#         return redirect('/')
#     except Exception as e:
#         logging.error(f"Error in upload: {str(e)}")
#         return redirect('/')

# @app.route('/uploads/<filename>')
# def uploaded_file(filename):
#     logging.debug(f"Serving file: {filename}")
#     return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# @app.route('/script.js', methods=['GET'])
# def scripts_js():
#     logging.debug("Serving script.js")
#     return send_from_directory('.', 'script.js')

# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
from google.cloud import storage, texttospeech
import vertexai
from vertexai.generative_models import GenerativeModel, Part
import os
import logging

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'wav', 'webm'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
BUCKET_NAME = "my-audio-bucket-789"  # Replace with your GCS bucket name
PROJECT_ID = "fifth-glazing-452704-m2"  # Replace with your project ID
LOCATION = "us-central1"

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize Vertex AI and TTS
vertexai.init(project=PROJECT_ID, location=LOCATION)
model = GenerativeModel("gemini-1.5-flash-002")
tts_client = texttospeech.TextToSpeechClient()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_files():
    files = [f for f in os.listdir(UPLOAD_FOLDER) if allowed_file(f)]
    files.sort(reverse=True)
    return files

def get_tts_files():
    files = [f for f in os.listdir(UPLOAD_FOLDER) if f.startswith('tts_') and f.endswith('.wav')]
    files.sort(reverse=True)
    return files

def upload_to_gcs(file_path, filename):
    logging.debug(f"Uploading {file_path} to GCS as {filename}")
    storage_client = storage.Client()
    bucket = storage_client.bucket(BUCKET_NAME)
    blob = bucket.blob(filename)
    blob.upload_from_filename(file_path)
    return blob

def analyze_audio(file_path):
    try:
        filename = os.path.basename(file_path)
        blob = upload_to_gcs(file_path, filename)
        
        audio_content = blob.download_as_bytes()
        audio_part = Part.from_data(
            data=audio_content,
            mime_type="audio/webm" if file_path.endswith('.webm') else "audio/wav"
        )

        prompt = [
            audio_part,
            "Please transcribe the audio and perform sentiment analysis on the transcription. Return the result in this format:\nTranscript: [transcription text]\nSentiment: [Positive/Negative/Neutral]"
        ]
        
        response = model.generate_content(prompt)
        result = response.text.strip()
        logging.debug(f"Gemini response: {result}")
        return result
    except Exception as e:
        logging.error(f"Error in audio analysis: {str(e)}")
        return f"Error analyzing audio: {str(e)}"

def text_to_audio(text):
    try:
        synthesis_input = texttospeech.SynthesisInput(text=text)
        voice = texttospeech.VoiceSelectionParams(
            language_code="en-US",
            ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
        )
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.LINEAR16
        )
        response = tts_client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )
        return response.audio_content
    except Exception as e:
        logging.error(f"Error in TTS: {str(e)}")
        return None

@app.route('/')
def index():
    logging.debug("Rendering index page")
    return render_template('index.html', files=get_files(), tts_files=get_tts_files())

@app.route('/upload', methods=['POST'])
def upload_audio():
    logging.debug("Received audio upload request")
    try:
        if 'audio_data' not in request.files:
            logging.error("No audio_data in request.files")
            return redirect('/')
        file = request.files['audio_data']
        if file and allowed_file(file.filename):
            filename = datetime.now().strftime("%Y%m%d-%H%M%S") + '.webm'
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            logging.debug(f"Saving audio to {file_path}")
            file.save(file_path)
            
            result = analyze_audio(file_path)
            transcript_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{filename}.txt")
            with open(transcript_path, 'w') as f:
                f.write(result)
                logging.debug(f"Saved audio result to {transcript_path}")
            
            return redirect('/')
        logging.error(f"File not allowed: {file.filename}")
        return redirect('/')
    except Exception as e:
        logging.error(f"Error in audio upload: {str(e)}")
        return redirect('/')

@app.route('/upload_text', methods=['POST'])
def upload_text():
    logging.debug("Received text upload request")
    try:
        text = request.form.get('text')
        if not text:
            logging.error("No text provided")
            return redirect('/')
        
        # Generate audio from text
        audio_content = text_to_audio(text)
        if not audio_content:
            return redirect('/')
        
        filename = f"tts_{datetime.now().strftime('%Y%m%d-%H%M%S')}.wav"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        with open(file_path, 'wb') as f:
            f.write(audio_content)
            logging.debug(f"Saved TTS audio to {file_path}")
        
        # Analyze the generated audio
        result = analyze_audio(file_path)
        transcript_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{filename}.txt")
        with open(transcript_path, 'w') as f:
            f.write(result)
            logging.debug(f"Saved TTS result to {transcript_path}")
        
        return redirect('/')
    except Exception as e:
        logging.error(f"Error in text upload: {str(e)}")
        return redirect('/')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    logging.debug(f"Serving file: {filename}")
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/script.js', methods=['GET'])
def scripts_js():
    logging.debug("Serving script.js")
    return send_from_directory('.', 'script.js')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

