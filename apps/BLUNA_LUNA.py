import streamlit as st
import plotly
import plotly.express as px
import statsmodels.api as sm
import pandas as pd
import json

def app():

    #st.set_page_config(layout="wide")
    st.title("bLUNA vs LUNA pricing")
    st.text ("https://app.flipsidecrypto.com/velocity/queries/ff2592e2-9fb6-4635-a1af-795c8dabd681")
    st.text('Null values are due to grouping, impact on visualizations is negligible')
    st.text('')
    st.text("""
The time period displayed below is the beginning of May 1st, 2021 to May 31st, 2021. 
This was done intentionally to address the 'Black Swan' event and because returning 30 second windows of data outside 
of a month long time period would exceed the allowable row limit on flipside.
    """)
    st.text("")
    st.text("""Details of Black Swan can be found here: 
https://medium.com/@terra-bites/luna-black-swan-do-kwon-ama-on-what-weve-learned-anchor-action-plan-9d3abdacaf02
    """)
    st.markdown("""
    ---
    """)


    bluna_luna_flipside_df = pd.read_json('https://api.flipsidecrypto.com/api/v2/queries/ff2592e2-9fb6-4635-a1af-795c8dabd681/data/latest')
    bluna_luna_flipside_df['TIME_GROUP'] = pd.to_datetime(bluna_luna_flipside_df['TIME_GROUP'])

    original_time_group = bluna_luna_flipside_df['TIME_GROUP']
    
    t_f = False
    st.sidebar.write("Choose y-axis scale")
    check = st.sidebar.checkbox("Linear/Log")
    if check: 
        t_f = True


    time_floor = st.sidebar.selectbox(
        'Choose your time group',
        ('30 Seconds', 'Min', 'H', 'D', '7D'))

    
    if time_floor == '30 Seconds':
        bluna_luna_flipside_df['TIME_GROUP'] = original_time_group
        bluna_luna_flipside_df = bluna_luna_flipside_df.groupby('TIME_GROUP', as_index=False).mean()
        bluna_luna_flipside_df['PRICE_DIFF'] = (bluna_luna_flipside_df['PRICE_BLUNA'] - bluna_luna_flipside_df['PRICE_LUNA'])
        bluna_luna_flipside_df['PRICE_LUNA_RoR_DIFF'] = bluna_luna_flipside_df['PRICE_LUNA'].diff()
        bluna_luna_flipside_df['PRICE_bLUNA_RoR_DIFF'] = bluna_luna_flipside_df['PRICE_BLUNA'].diff()
        bluna_luna_flipside_df.sort_values(by = ['TIME_GROUP'], ascending=False, inplace = True)
    
    elif time_floor:
        bluna_luna_flipside_df['TIME_GROUP'] = pd.to_datetime(bluna_luna_flipside_df['TIME_GROUP']).dt.floor(time_floor)
        bluna_luna_flipside_df = bluna_luna_flipside_df.groupby('TIME_GROUP', as_index=False).mean()
        bluna_luna_flipside_df['PRICE_DIFF'] = (bluna_luna_flipside_df['PRICE_BLUNA'] - bluna_luna_flipside_df['PRICE_LUNA'])
        bluna_luna_flipside_df['PRICE_LUNA_RoR_DIFF'] = bluna_luna_flipside_df['PRICE_LUNA'].diff()
        bluna_luna_flipside_df['PRICE_bLUNA_RoR_DIFF'] = bluna_luna_flipside_df['PRICE_BLUNA'].diff()
        bluna_luna_flipside_df.sort_values(by = ['TIME_GROUP'], ascending=False, inplace = True)
    

#-------------------------------------------------------
    
    st.markdown("""
    ### bLUNA vs LUNA - Base Table
    """)

    st.dataframe(bluna_luna_flipside_df)

    st.markdown("""
    """)
    


    bluna_luna_graph = px.line(
        bluna_luna_flipside_df, #this is the dataframe you are trying to plot
        x = "TIME_GROUP",
        y = ['PRICE_BLUNA', 'PRICE_LUNA'],
        title = "<b>bLUNA vs LUNA</b>",
        orientation = "v",
        template = "plotly_white",
        width = 1000,
        height = 600,
        log_y = t_f
    )
    

    st.plotly_chart(bluna_luna_graph)

    st.text("")
    st.write("""
    Looking at the pricing for bLUNA and LUNA one can hardly tell a difference between the two graphically.
    Even when changing the scale from Linear to Log, the difference is hardly noticeable (on sidebar).
    """)

# ----------------------------------------------------------------

 
    bluna_luna_graph2 = px.line(
    bluna_luna_flipside_df, #this is the dataframe you are trying to plot
    x = "TIME_GROUP",
    y = "PRICE_DIFF",
    #color = columns,
    title = "<b>bLUNA vs LUNA pricing DIFFERENCE</b>",
    orientation = "v",
    template = "plotly_white",
    width = 1000,
    height = 600,
    log_y = t_f
    )
    

    st.plotly_chart(bluna_luna_graph2)
    st.caption ("""
    The price difference is calculated as the price of bLUNA MINUS the price of LUNA for the given time period.
    There is a respective column for this value on the base table.
    """)
    
    st.text("")
    st.text(f'The most bLuna has drifted below LUNA in a {time_floor} long window')
    st.text(bluna_luna_flipside_df['PRICE_DIFF'].min())
    st.text("")
    st.text(f'The most bLuna has drifted above LUNA in a {time_floor} long window')
    st.text(bluna_luna_flipside_df['PRICE_DIFF'].max())
    st.text("")

#--------------------------------------------------------------------------------------------

    bluna_luna_graph3 = px.line(
    bluna_luna_flipside_df, #this is the dataframe you are trying to plot
    x = "TIME_GROUP",
    y = ['PRICE_LUNA_RoR_DIFF', 'PRICE_bLUNA_RoR_DIFF'],
    #color = columns,
    title = "<b>bLUNA vs LUNA pricing ROW OVER ROW DIFFERENCE</b>",
    orientation = "v",
    template = "plotly_white",
    width = 1000,
    height = 600,
    log_y = t_f
    )
    

    st.plotly_chart(bluna_luna_graph3)
    st.caption ("""
    The row over row difference is calculated as the price of the asset in the current time period minus the 
    price of the asset in the previous time period. There are respective columns for these values on the base table.
    """)

    st.text("")
    st.text(f'The most bLuna has dipped in a {time_floor} long window')
    st.text(bluna_luna_flipside_df['PRICE_bLUNA_RoR_DIFF'].min())
    st.text("")
    st.text(f'The most LUNA has dipped in a {time_floor} long window')
    st.text(bluna_luna_flipside_df['PRICE_LUNA_RoR_DIFF'].min())
    st.text("")
    st.text(f'The most bLuna has risen in a {time_floor} long window')
    st.text(bluna_luna_flipside_df['PRICE_bLUNA_RoR_DIFF'].max())
    st.text("")
    st.text(f'The most LUNA has risen in a {time_floor} long window')
    st.text(bluna_luna_flipside_df['PRICE_LUNA_RoR_DIFF'].max())
    st.text("")
    # ------------------------------------------------


