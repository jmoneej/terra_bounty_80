import streamlit as st
from PIL import Image
from multiapp import MultiApp
from apps import home, BLUNA_LUNA, BETH_ETH # import your app modules here

app = MultiApp()

st.set_page_config(layout="wide")
terra = Image.open("terra.png")
st.image(terra)
st.markdown("""
# Historic bAssets Price Movements
""")


st.write("""What is the most bLuna has dipped in a X second window (based on bLuna price oracle timing)? Focus on the events of the Black swan event in mid-May. Make the default size of the window 30 seconds.""")

# Add all your application here
app.add_app("Home / Tutorial", home.app)
app.add_app("Bluna & Luna prices", BLUNA_LUNA.app)
app.add_app("bETH & ETH prices", BETH_ETH.app)



# The main app
app.run()