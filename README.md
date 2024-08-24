# Recording-to-Meeting-Minutes
Simple tool made using whisper and google gemini that makes meeting minutes of recorded videos.

# Meeting Minutes Tool

This repository contains a Streamlit application that processes meeting videos, extracts the audio, converts it to text, and summarizes the content into meeting minutes using the Google Gemini Pro API.

## Features

- **Video Upload**: Upload meeting videos in formats like MP4, MOV, or AVI.
- **Audio Extraction**: Extract audio from the uploaded video file.
- **Speech-to-Text Conversion**: Convert the extracted audio into text using the Whisper model.
- **Meeting Summary Generation**: Generate a concise summary of the meeting, including key points, minutes, and agenda, using Google Gemini Pro.

## Requirements

To run this application, ensure you have the following Python packages installed:

```bash
pip install streamlit python-dotenv moviepy whisper google-generativeai
```

Additionally, you need to have FFmpeg installed, which is required by the `moviepy` library to handle video files.

## How It Works

### 1. Environment Setup

The application starts by loading environment variables using `dotenv`. The Google API key is retrieved from the environment and used to configure the Google Gemini Pro API.

```python
from dotenv import load_dotenv
import os
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
```

### 2. Prompt Definition

The application uses a predefined prompt to instruct the Google Gemini Pro API on how to summarize the meeting. The prompt asks for a summary of the meeting text, including key points, minutes, and agenda.

```python
prompt = """You are a meeting video summarizer. You will be taking the transcript text
and summarizing the entire video, providing the important summary in points alongside the meeting minutes and the agenda within 250 words. Please provide the summary 
of the text given here: """
```

### 3. Functions Overview

- **`generate_gemini_content()`**: This function sends the transcript text and the prompt to the Google Gemini Pro API and returns the generated summary.

    ```python
    def generate_gemini_content(transcript_text, prompt):
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt + transcript_text)
        return response.text
    ```

- **`extract_audio_from_video()`**: This function extracts the audio from the uploaded video file and saves it as a `.wav` file.

    ```python
    def extract_audio_from_video(video_file, audio_file):
        video = mp.VideoFileClip(video_file)
        video.audio.write_audiofile(audio_file)
    ```

- **`convert_audio_to_text()`**: This function converts the extracted audio file into text using the Whisper speech-to-text model.

    ```python
    def convert_audio_to_text(audio_file):
        model = whisper.load_model("base")
        result = model.transcribe(audio_file)
        return result['text']
    ```

- **`video_to_text()`**: This function integrates the audio extraction and speech-to-text conversion processes, returning the full transcript of the video.

    ```python
    def video_to_text(video_file):
        audio_file = "temp_audio.wav"
        extract_audio_from_video(video_file, audio_file)
        text = convert_audio_to_text(audio_file)
        return text
    ```

### 4. Streamlit Frontend

The Streamlit frontend allows users to interact with the application by uploading a video, processing it, and displaying the generated meeting minutes.

- **Video Upload**: The user uploads a video file through the Streamlit interface.

    ```python
    video = st.file_uploader("Upload a meeting video", type=["mp4", "mov", "avi"])
    ```

- **Processing the Video**: When the user clicks the "Get Detailed Notes" button, the application processes the video to extract the transcript text and then generates a summary.

    ```python
    if st.button("Get Detailed Notes"):
        if video:
            with st.spinner("Processing video..."):
                with tempfile.NamedTemporaryFile(delete=False) as tmp_video_file:
                    tmp_video_file.write(video.read())
                    tmp_video_path = tmp_video_file.name

                transcript_text = video_to_text(tmp_video_path)
    ```

- **Generating the Summary**: Once the transcript is obtained, it is sent to the Google Gemini Pro API to generate the meeting summary.

    ```python
    if transcript_text:
        with st.spinner("Generating summary..."):
            summary = generate_gemini_content(transcript_text, prompt)

        st.markdown("## Detailed Notes:")
        st.write(summary)
    ```

### 5. Error Handling

The application provides appropriate feedback to the user if the video processing fails or if no video is uploaded.

```python
else:
    st.error("Failed to extract text from the video.")
else:
    st.warning("Please upload a video file.")
```

## Running the Application

To run the application, use the following command:

```bash
streamlit run app.py
```

Make sure that your `.env` file contains the correct Google API key:

```
GOOGLE_API_KEY=your_api_key_here
```

**Note: This is just a basic implementations feel free to contribute to make this project better any constructive feedback is appreciated. Thanks <3 !**
