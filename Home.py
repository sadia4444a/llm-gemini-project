import streamlit as st


st.caption("🚀 A LLM App powered by Gemini")
# Home Page Title
st.markdown(" ### Welcome to the YouT App! 👩🏼‍💻")

# Demo Video
st.write(" ")
st.markdown("#### :red[ 🎥 Watch the full demo to see all the features in action!]")
video_file = open("/Users/mst.sadiakhatun/Desktop/YouT_App/video/YouT_App_demo.mov", "rb")
video_bytes = video_file.read()
st.video(video_bytes)



st.divider()
st.markdown("## :green[Features 🤯]")

st.subheader(":red[🕝 Calculate Time]")
st.markdown("""
            **User Input:** The user enters a YouTube playlist URL into the app.
            
            **Extract Playlist ID:** The app extracts the playlist ID from the URL using a regular expression.
            
            **YouTube API:** The app uses the YouTube Data API to fetch details of the videos in the playlist, including their durations.
            
            **Calculate Duration:** The app adds up the durations of all videos in the playlist.
            
            **Display Result:** The total time is displayed in hours, minutes, and seconds.
            
            **History:** The app keeps a history of previously calculated playlist durations for easy reference.
            """)


st.divider()


st.subheader(":red[😎 Find Popular]")
# st.image("path_to_feature1_screenshot.png", caption="Screenshot of Feature 1", use_column_width=True)
st.markdown("""
            **YouTube API Integration:** The app uses the YouTube Data API to fetch video details from a given playlist.
            
            **Most Popular Video Identification:** It analyzes the view counts of all videos in the playlist to identify the most popular one.
            
            **User Interface:** Provides a simple interface where users can input a playlist link, and it displays the most popular video along with a link to watch it and a thumbnail image.

    
""")

st.divider()
st.subheader(":red[📄 Transcript]")
st.markdown("""
            **Video Link Input:** The user provides a YouTube video link, from which the video ID is extracted.
            
            **Transcript Extraction:** When the user clicks “Raw Transcript,” the transcript is extracted and displayed.
            
            **Summarization:** Clicking “Summarized Note” generates a summary, which can then be downloaded as a PDF.
            
            **History Display:** The app shows the history of all video analyses conducted in the session.

            """)
st.divider()	

st.subheader(":red[🌏 Create LinkedIn Post]")
st.markdown("""
            **Video Link Input:** Users provide a YouTube video link, from which the video ID is extracted.
            
            **Video Details and Transcript:** The app fetches video details and the transcript text.
            
            **Post Generation:** Clicking “Generate LinkedIn Post” creates a LinkedIn post, which can then be viewed and saved.
            
            **History Display:** The app shows a history of all posts generated during the session.
            """)

st.divider()

st.subheader(":red[📝 Code Explainer]")
st.markdown("""
	**Text Area for Code Input:** Users can paste a Python code segment into the text area provided.
 
	**Explanation Generation:** When the “Explain Code” button is pressed, the app sends the code segment to Google Gemini, which returns an explanation that covers the purpose, functionality, and key takeaways of the code.
 
	**Display of Code and Explanation:** The code segment and its explanation are displayed on the same page for easy reference.
 
	**History Display:** The app maintains a session-based history of all explanations, allowing users to revisit past explanations.
""")
st.divider()


st.subheader(":red[📝 Code Explainer]")
st.markdown("""
	**API Key Configuration:**
	The Google Gemini API and YouTube Data API are configured using API keys stored securely in Streamlit secrets.
 
	**Function to Extract Video ID:**
	The extract_video_id function extracts the unique video ID from various formats of YouTube URLs using regular expressions.
 
	**Fetching YouTube Comments:**
	The get_youtube_comments function fetches comments from the specified YouTube video using the YouTube Data API. It retrieves the top-level comments and stores them in a list.
 
	**Analyzing Comments:**
	The analyze_comments_with_prompt function sends the fetched comments to Google Gemini Pro. The prompt asks for an analysis that covers the overall sentiment, common themes, specific praises or criticisms, and a summary of viewer opinions.
	The generated analysis is then returned and displayed in the Streamlit app.
""")
st.divider()


# Closing Remarks
st.markdown("""
Thank you for using the YouT App 🤩. 
""")

st.divider()

st.markdown("#### :red[Contact Information 📞]")
st.write("For any queries or feedback, feel free to reach out to me:")
st.markdown("""
- **Email:** 📧 [sadiasultana4444a@gmail.com](mailto:sadiasultana4444a@gmail.com)
- **LinkedIn:** 💼 [sadiakhatun](https://www.linkedin.com/in/sadiakhatun)
- **GitHub:** 🖥️ [sadia4444a](https://github.com/sadia4444a)
""")