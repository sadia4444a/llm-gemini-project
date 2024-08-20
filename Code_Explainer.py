import streamlit as st
from googleapiclient.discovery import build
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi
import re




#API KEY------------------

# Configure Google Gemini API key
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])



#Function-----------------
    

# Function to generate LinkedIn post using Google Gemini
def generate_linkedin_post(code_segment):
    prompt = f"""
You are an expert programmer and social media content creator with a deep understanding of software engineering concepts, Ml engineering and Data science. 
Your task is to explain the following code segment in a clear and accessible manner, suitable for sharing on LinkedIn or in a technical blog post. 
The explanation should cover:

1. **Purpose:** What does this code aim to achieve?
2. **Functionality:**How does each part of the code work point by point?
5. **Key Takeaways:** What should someone learn from this code?

Ensure the explanation is engaging, easy to follow, and provides value to both beginners and experienced programmers. Use a friendly and approachable tone, and feel free to add relevant examples or analogies to enhance understanding.

Here’s the code segment:

```python
{code_segment} 
Write a LinkedIn post based on this information that feels personal, engaging, easy to read and understand and uses appropriate emojis.
"""

    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt)
    return response.text





# Streamlit UI----------------
with st.sidebar:
    "[View the source code](https://github.com/sadia4444a/llm-gemini-project/blob/master/Code_Explainer.py)"

st.title("Code Segment To Post ")

code_segment=st.text_area("Enter Code Segment..")

if 'code_history' not in st.session_state:
    st.session_state['code_history'] = []

if st.button("Explain Code"):
    Explanation = generate_linkedin_post(code_segment)
    st.markdown("### Code Explanation ")
    st.code(code_segment ,language="python" )
    st.write(Explanation)
    
    st.session_state['code_history'].append({
        'code': code_segment,
        'response': Explanation
    })
    
    
st.header(":red[History]" , divider='violet' )

if st.session_state['code_history']:
    for idx, entry in enumerate(st.session_state['code_history'], 1):
        st.subheader(f":red[Analysis for code {idx}]")
        st.code(entry['code'],language="python")
        st.write(entry['response'])
        st.divider()