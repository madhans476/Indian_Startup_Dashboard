import streamlit as st
import pandas as pd
import seaborn as sns 
import matplotlib.pyplot as plt
import altair as alt

st.set_page_config(layout='wide',page_title="Cities")

df = pd.read_csv("startup_funding.csv")


st.subheader('Statewise Startup Count')

type = st.selectbox('Type:',['BarPlot', 'DataFrame'])

n = st.slider("Select n:",2,18,5)
data = df['state'].value_counts().reset_index()
# data = data.drop(index=3)

data = data[:n]
data = data.sort_values('count', ascending=True)

if type == 'BarPlot':
    bh = 68
    min_bh = 450
    ch = max(n * bh, min_bh)

    base_bar_size = 60 
    min_bar_size = 10
    bar_size = max(base_bar_size - n * (1.2), min_bar_size)

    bars = alt.Chart(data).mark_bar(size=bar_size).encode(
        x=alt.X('count:Q', title='Count'),
        y=alt.Y('state:N', title='State', sort='-x'),
        color=alt.value('orange')
    ).properties(
        # title='Statewise Startup Count',
        height = ch
    ).configure_axis(
        labelFontSize=12,
        titleFontSize=14
    ).configure_title(
        fontSize=16
    )

    # Hover interaction
    highlight = alt.selection_single(on='mouseover', empty='none')

    # Chart with hover effect
    bars = bars.encode(
        color=alt.condition(highlight, alt.value('blue'), alt.value('orange')),
        size=alt.condition(highlight, alt.value(bar_size+(bar_size/3)), alt.value(bar_size))  # Enlarges on hover
    ).add_selection(
        highlight
    )

    # Show chart in Streamlit
    st.altair_chart(bars, use_container_width=True)
else:
    data = data.sort_values('count', ascending=False)
    st.write('Data Overview:')
    h = n*41
    st.dataframe(data.style.set_properties(**{
            'background-color': '#262730',
            'border': '1px solid black',
            'text-align': 'center'
        }), height = h, width = 400)