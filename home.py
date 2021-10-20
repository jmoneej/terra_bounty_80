import streamlit as st
import plotly
import plotly.express as px
import statsmodels.api as sm
import pandas as pd
import json
from PIL import Image


def app():

    #st.set_page_config(layout="wide")
    st.title("Home Page / Tutorial")

    st.markdown("""
    ##### USE THE DROP DOWN NAVIGATION ABOVE TO VIEW THE QUERY DASHBOARDS. THIS PAGE COVERS HOW TO VIEW DATA, VERY BRIEF.
    """
    )
    st.write("""
    Utilizing Streamlit for Terra bounty #80. Links to original queries are below. 
    """
    )





    st.text ("")
    st.markdown("""
    ###### ORIGINAL QUERIES
    """)
    st.text ("https://app.flipsidecrypto.com/velocity/queries/6e7b6fd8-9b50-4a77-a26e-604fe6e932c0 - bETH vs ETH")
    st.text ("https://app.flipsidecrypto.com/velocity/queries/ff2592e2-9fb6-4635-a1af-795c8dabd681 - bLUNA vs LUNA")
    

#-------------------------------------------------------

    st.markdown("""
    ---
    """)
    st.markdown("""
    #### USING STREAMLIT
    """)
    
    tutorial_1 = Image.open("tutorial_1.png")
    st.image(tutorial_1)

    st.caption ("""
    Hover over graphs and tables to reveal menu and fullscreen mode. Arrows point out to enlarge, and point in to make small again.
    """)
    st.text("")

    tutorial_2 = Image.open("tutorial_2.png")
    st.image(tutorial_2)
    st.text("")
    st.caption ("""
    The sidebar opens by default on each page. Simply click on the x to hide it and then click on the arrow to reveal it again. 
    The sidebar contains options to customize visualizations.
    """)
    st.text("")

    tutorial_3 = Image.open("tutorial_3.png")
    st.image(tutorial_3)
    st.text("")
    st.caption ("""
    The sidebar contains options to make graphs either Linear or Log and to choose which time group to view data by. "Time group" changes the x-axis of graphs.
    """)
    st.text("")


   