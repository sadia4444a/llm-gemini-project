import streamlit as st

st.title(':red[YouT APP]', help='YouTube Video Analysis App and So On')

# define page here
PlayListHour = st.Page("PlayListHour.py", title="Calculate Time",icon='🕝')
PopularVideo = st.Page("PopularVideo.py", title="Find Popular",icon='😎')
Transcript =st.Page("Transcript.py",title="Transcript",icon='📄')
CreatePost =st.Page("CreatePost.py",title="Create LinkedIn Post",icon='🌏')
Code_Explainer =st.Page("Code_Explainer.py",title="Code_Explainer",icon='📝')
commentA =st.Page("commentA.py",title="Comment Analysis",icon='📨')
Home =st.Page("Home.py",title="Home",icon='🏠')

pg = st.navigation([Home,PlayListHour, PopularVideo,Transcript,CreatePost,Code_Explainer,commentA])
pg.run()