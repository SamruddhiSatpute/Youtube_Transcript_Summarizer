import streamlit as st
from dotenv import load_dotenv

load_dotenv()
import os
# FIXED: new google.genai package
from google import genai
from google.genai import types
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import NoTranscriptFound, TranscriptsDisabled

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

prompt = """You are a YouTube video summarizer. You will be taking the transcript text
and summarizing the entire video and providing the important summary in points
within 250 words. Please provide the summary of the text given here: """


def extract_video_id(youtube_video_url):
    if "v=" in youtube_video_url:
        return youtube_video_url.split("v=")[1].split("&")[0]
    elif "youtu.be/" in youtube_video_url:
        return youtube_video_url.split("youtu.be/")[1].split("?")[0]
    elif "youtube.com/shorts/" in youtube_video_url:
        return youtube_video_url.split("shorts/")[1].split("?")[0]
    else:
        raise ValueError("Invalid YouTube URL format.")


def extract_transcript_details(youtube_video_url):
    try:
        video_id = extract_video_id(youtube_video_url)

        ytt = YouTubeTranscriptApi()

        try:
            fetched = ytt.fetch(video_id, languages=['en'])
        except NoTranscriptFound:
            transcript_list = ytt.list(video_id)
            first_transcript = next(iter(transcript_list))
            st.warning(f"No English transcript. Using: {first_transcript.language}")
            fetched = ytt.fetch(video_id, languages=[first_transcript.language_code])
        except TranscriptsDisabled:
            return None, "Transcripts are disabled for this video."

        full_transcript = " ".join([snippet.text for snippet in fetched])
        return full_transcript, None

    except ValueError as ve:
        return None, str(ve)
    except Exception as e:
        return None, f"Unexpected error: {str(e)}"


def generate_gemini_content(transcript_text, prompt):
    # FIXED: new google.genai syntax
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt + transcript_text
    )
    return response.text


# --- UI ---
st.title("YouTube Transcript to Detailed Notes Converter")
youtube_link = st.text_input("Enter YouTube Video Link:")

if youtube_link:
    try:
        video_id = extract_video_id(youtube_link)
        # FIXED: width='stretch' replaces use_container_width=True
        st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", width='stretch')
    except ValueError as e:
        st.error(str(e))

if st.button("Get Detailed Notes"):
    if not youtube_link:
        st.warning("Please enter a YouTube link first.")
    else:
        with st.spinner("Fetching transcript..."):
            transcript_text, error = extract_transcript_details(youtube_link)

        if error:
            st.error(error)
        elif transcript_text:
            with st.spinner("Generating summary with Gemini..."):
                summary = generate_gemini_content(transcript_text, prompt)
            st.markdown("## Detailed Notes:")
            st.write(summary)