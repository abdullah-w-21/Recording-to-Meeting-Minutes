import streamlit as st
from dotenv import load_dotenv
import os
import whisper
import moviepy.editor as mp
import google.generativeai as genai
import tempfile


load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# prompt -------------------
prompt = """You are a meeting video summarizer. You will be taking the transcript text
and summarizing the entire video, providing the important summary in points alongside the meeting minutes and the agenda within 250 words. Please provide the summary 
of the text given here: """

def generate_gemini_content(transcript_text, prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt + transcript_text)
    return response.text

def extract_audio_from_video(video_file, audio_file):
    video = mp.VideoFileClip(video_file)
    video.audio.write_audiofile(audio_file)

def convert_audio_to_text(audio_file):
    model = whisper.load_model("base")
    result = model.transcribe(audio_file)
    return result['text']

def video_to_text(video_file):
    audio_file = "temp_audio.wav"
    extract_audio_from_video(video_file, audio_file)
    text = convert_audio_to_text(audio_file)
    return text


# streamlit frontend
st.title("Meeting Minutes Tool")
video = st.file_uploader("Upload a meeting video", type=["mp4", "mov", "avi"])

if st.button("Get Detailed Notes"):
    if video:
        with st.spinner("Processing video..."):
            with tempfile.NamedTemporaryFile(delete=False) as tmp_video_file:
                tmp_video_file.write(video.read())
                tmp_video_path = tmp_video_file.name

            transcript_text = video_to_text(tmp_video_path)

        if transcript_text:
            with st.spinner("Generating summary..."):
                summary = generate_gemini_content(transcript_text, prompt)

            st.markdown("## Detailed Notes:")
            st.write(summary)
        else:
            st.error("Failed to extract text from the video.")
    else:
        st.warning("Please upload a video file.")
