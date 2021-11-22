import streamlit as st
import plotly
import plotly.express as px
import statsmodels.api as sm
import pandas as pd
import json

def app():

    #st.set_page_config(layout="wide")
    st.title("bETH vs ETH pricing")
    st.text ("https://api.flipsidecrypto.com/api/v2/queries/6e7b6fd8-9b50-4a77-a26e-604fe6e932c0/data/latest")
    st.text('Null values are due to grouping, impact on visualizations is negligible')
    st.text('')
    st.text("""
The earliest timestamp for recorded data is 2021-09-14T22:17:30Z.
Data from ETH is limited to anything after this date because there are no records of bETH prices
before the timestamp. The queries will regularly refresh until enough data has been collected to
exceed the row limit on Flipside.
    """)
    st.markdown("""
    ---
    """)


    beth_eth_flipside_df = pd.read_json('https://api.flipsidecrypto.com/api/v2/queries/6e7b6fd8-9b50-4a77-a26e-604fe6e932c0/data/latest')
    beth_eth_flipside_df['TIME_GROUP'] = pd.to_datetime(beth_eth_flipside_df['TIME_GROUP'])

    original_time_group = beth_eth_flipside_df['TIME_GROUP']
    
    t_f = False
    st.sidebar.write("Choose y-axis scale")
    check = st.sidebar.checkbox("Linear/Log")
    if check: 
        t_f = True


    time_floor = st.sidebar.selectbox(
        'Choose your time group',
        ('30 Seconds', 'Min', 'H', 'D', '7D'))

    
    if time_floor == '30 Seconds':
        beth_eth_flipside_df['TIME_GROUP'] = original_time_group
        beth_eth_flipside_df = beth_eth_flipside_df.groupby('TIME_GROUP', as_index=False).mean()
        beth_eth_flipside_df['PRICE_DIFF'] = (beth_eth_flipside_df['PRICE_BETH'] - beth_eth_flipside_df['PRICE_ETH'])
        beth_eth_flipside_df['price_ETH_RoR_DIFF'] = beth_eth_flipside_df['PRICE_ETH'].diff()
        beth_eth_flipside_df['price_bETH_RoR_DIFF'] = beth_eth_flipside_df['PRICE_BETH'].diff()
        beth_eth_flipside_df.sort_values(by = ['TIME_GROUP'], ascending=False, inplace = True)
    
    elif time_floor:
        beth_eth_flipside_df['TIME_GROUP'] = pd.to_datetime(beth_eth_flipside_df['TIME_GROUP']).dt.floor(time_floor)
        beth_eth_flipside_df = beth_eth_flipside_df.groupby('TIME_GROUP', as_index=False).mean()
        beth_eth_flipside_df['PRICE_DIFF'] = (beth_eth_flipside_df['PRICE_BETH'] - beth_eth_flipside_df['PRICE_ETH'])
        beth_eth_flipside_df['price_ETH_RoR_DIFF'] = beth_eth_flipside_df['PRICE_ETH'].diff()
        beth_eth_flipside_df['price_bETH_RoR_DIFF'] = beth_eth_flipside_df['PRICE_BETH'].diff()
        beth_eth_flipside_df.sort_values(by = ['TIME_GROUP'], ascending=False, inplace = True)
    

#-------------------------------------------------------
    
    st.markdown("""
    ### bETH vs ETH - Base Table
    """)

    st.dataframe(beth_eth_flipside_df)

    st.markdown("""
    """)
    


    beth_eth_graph = px.line(
        beth_eth_flipside_df, #this is the dataframe you are trying to plot
        x = "TIME_GROUP",
        y = ['PRICE_BETH', 'PRICE_ETH'],
        title = "<b>bETH vs ETH</b>",
        orientation = "v",
        template = "plotly_white",
        width = 1000,
        height = 600,
        log_y = t_f
    )
    

    st.plotly_chart(beth_eth_graph)

    st.text("")
    st.write("""
    When comparing to bLUNA and LUNA, the pricing differences between bETH and ETH are much more apparent.

    """)

# ----------------------------------------------------------------

 
    beth_eth_graph2 = px.line(
    beth_eth_flipside_df, #this is the dataframe you are trying to plot
    x = "TIME_GROUP",
    y = "PRICE_DIFF",
    #color = columns,
    title = "<b>bETH vs ETH pricing DIFFERENCE</b>",
    orientation = "v",
    template = "plotly_white",
    width = 1000,
    height = 600,
    log_y = t_f
    )
    

    st.plotly_chart(beth_eth_graph2)
    st.caption ("""
    The price difference is calculated as the price of bETH MINUS the price of ETH for the given time period.
    There is a respective column for this value on the base table.
    """)
    
    st.text("")

    st.text(f'The most bETH has drifted below ETH in a {time_floor} long window')
    st.text(beth_eth_flipside_df['PRICE_DIFF'].min())
    st.text("")
    st.text(f'The most bETH has drifted above ETH in a {time_floor} long window')
    st.text(beth_eth_flipside_df['PRICE_DIFF'].max())
    st.text("")

#--------------------------------------------------------------------------------------------

    beth_eth_graph3 = px.line(
    beth_eth_flipside_df, #this is the dataframe you are trying to plot
    x = "TIME_GROUP",
    y = ['price_ETH_RoR_DIFF', 'price_bETH_RoR_DIFF'],
    #color = columns,
    title = "<b>bETH vs ETH pricing ROW OVER ROW DIFFERENCE</b>",
    orientation = "v",
    template = "plotly_white",
    width = 1000,
    height = 600,
    log_y = t_f
    )
    

    st.plotly_chart(beth_eth_graph3)
    st.caption ("""
    The row over row difference is calculated as the price of the asset in the current time period minus the 
    price of the asset in the previous time period. There are respective columns for these values on the base table.
    """)
    
    st.text("")
    st.text(f'The most bETH has dipped in a {time_floor} long window')
    st.text(beth_eth_flipside_df['price_bETH_RoR_DIFF'].min())
    st.text("")
    st.text(f'The most ETH has dipped in a {time_floor} long window')
    st.text(beth_eth_flipside_df['price_ETH_RoR_DIFF'].min())
    st.text("")
    st.text(f'The most bETH has risen in a {time_floor} long window')
    st.text(beth_eth_flipside_df['price_bETH_RoR_DIFF'].max())
    st.text("")
    st.text(f'The most ETH has risen in a {time_floor} long window')
    st.text(beth_eth_flipside_df['price_ETH_RoR_DIFF'].max())
    st.text("")
    # ------------------------------------------------


