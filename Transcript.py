import streamlit as st
from googleapiclient.discovery import build
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi
import re
from fpdf import FPDF


#API KEY------------------

# Configure Google Gemini API key
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
# YouTube API configuration
YOUTUBE_API_KEY = st.secrets["YOUTUBE_API_KEY"]
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)



#Function------------------

# Function to extract video ID using regex
def extract_video_id(youtube_video_url):
    video_id = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", youtube_video_url)
    return video_id.group(1) if video_id else None


# Function to extract transcript details
def extract_transcript_details(youtube_video_url):
    try:
        video_id = extract_video_id(youtube_video_url)
        if video_id:
            transcript_text = YouTubeTranscriptApi.get_transcript(video_id)
            transcript = " ".join([item['text'] for item in transcript_text])
            return transcript
        else:
            st.error("Could not extract video ID. Please check the URL.")
    except Exception as e:
        st.error(f"An error occurred while extracting the transcript: {e}")
        return None
    
    
    
    
def generate_gemini_content(transcript_text):
    prompt = f"""
    You are an expert video summarizer. Given the transcript of a YouTube video, 
    your task is to create a concise and informative summary that:
    
    Please provide the summary for the following transcript: 
    
    {transcript_text}
    
    - captures the key points, 
    - main ideas, and essential details of the video.
    - Learning part
    - How May It help
    
    The summary should be structured as a list of bullet points. Focus on clarity and coherence, and ensure that the summary is 
    useful for someone who wants to understand the video’s content quickly. 
    """
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt)
    return response.text



# Streamlit UI-----------------------
with st.sidebar:
    "[View the source code](https://github.com/sadia4444a/llm-gemini-yt-tools/blob/main/Transcript.py)"
    
st.title("YouTube Transcript to Summarized Notes")

# Persistent text input for YouTube link
youtube_link = st.text_input("Enter YouTube Video Link...")

if youtube_link:
    video_id = extract_video_id(youtube_link)
    if video_id:
        st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)

transcript_text = None
summary = None

Raw_Transcript=st.button('Raw Transcript')
if Raw_Transcript:
    transcript_text = extract_transcript_details(youtube_link)
    st.markdown("## Raw Transcript ")
    st.write(transcript_text)



if 'summary_history' not in st.session_state:
    st.session_state['summary_history'] = []
    
if st.button("Summarized Note"):
    transcript_text = extract_transcript_details(youtube_link)

    if transcript_text:
        summary = generate_gemini_content(transcript_text)
        if summary:
            st.markdown("## Summarized Notes:")
            st.write(summary)
            st.session_state['summary_history'].append({
        'video_link': youtube_link,
        'response': summary
        })
            

if summary:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, summary)
    pdf_output = pdf.output(dest='S').encode('latin1')
    st.download_button(label="Download PDF", data=pdf_output, file_name='summary.pdf', mime='application/pdf', type='primary')
    
    
st.header(":red[History]" , divider='violet' )    
if st.session_state['summary_history']:
    for idx, entry in enumerate(st.session_state['summary_history'], 1):
        st.subheader(f":red[Analysis for Video {idx}]")
        st.write(f"**:green[Video Link]:** {entry['video_link']}")
        st.write(entry['response'])
        st.divider()
