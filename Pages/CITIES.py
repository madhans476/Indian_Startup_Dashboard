import streamlit as st
import pandas as pd
import geopandas as gpd 
import matplotlib.pyplot as plt
import altair as alt

st.set_page_config(layout='wide',page_title="Cities")

df = pd.read_csv("startup_funding.csv")

color1 = 'Orange'
color2 = 'Blue'

# df1 = df['state'].value_counts().reset_index()
# df1 = df1.drop(index=3)
# india_shape = gpd.read_file('india_st.shp')

# india_shape['States'] = india_shape['STATE'].astype(str)  # Update accordingly

# df1['state'] = df1['state'].str.lower().str.strip()
# india_shape['States'] = india_shape['States'].str.lower().str.strip()

# # Merge the dataframes
# merged = india_shape.set_index('States').join(df1.set_index('state'))

# # # Check the merged data
# # print(merged[['Count']])  # Should show counts now

# fig, ax = plt.subplots(1, 1, figsize=(12, 10))  # Adjust size as needed
# merged.plot(
#     column='count', 
#     cmap='coolwarm',  # Use a more contrasting color map
#     linewidth=0.8, 
#     ax=ax, 
#     edgecolor='0.8',
#     legend=True, 
#     missing_kwds={'color': 'lightgrey', 'label': 'No Data'}
# )

# # Set title and remove axis
# ax.set_title('State-wise Heatmap (Count)', fontsize=16)
# ax.set_axis_off()

# # Display the plot in Streamlit
# st.pyplot(fig)



st.subheader('Statewise Startup Count')



def Barplot(n,data):
    bh = 68
    min_bh = 450
    ch = max(n * bh, min_bh)

    base_bar_size = 60 
    min_bar_size = 10
    bar_size = max(base_bar_size - n * (1.2), min_bar_size)

    bars = alt.Chart(data).mark_bar(size=bar_size).encode(
        x=alt.X('count:Q', title='Count'),
        y=alt.Y('state:N', title='State', sort='-x'),
        color=alt.value(color1),
        tooltip=[alt.Tooltip('count', title="Count: "), alt.Tooltip('state', title="State: ")]
    ).properties(
        height = ch
    ).configure_axis(
        labelFontSize=12,
    )

    # Hover interaction
    highlight = alt.selection_single(on='mouseover', empty='none')

    # Chart with hover effect
    bars = bars.encode(
        color=alt.condition(highlight, alt.value(color2), alt.value(color1)),
        size=alt.condition(highlight, alt.value(bar_size+(bar_size/3)), alt.value(bar_size))  # Enlarges on hover
    ).add_selection(
        highlight
    )

    # Show chart in Streamlit
    st.altair_chart(bars, use_container_width=True)
def DataFrame(n,data):
    data = data.sort_values('count', ascending=False)
    st.write('Data Overview:')
    h = n*41
    st.dataframe(data.style.set_properties(**{
            'background-color': '#262730',
            'border': '1px solid black',
            'text-align': 'center'
        }), height = h, width = 400)


n = st.slider("Select n:",2,18,5)
data = df['state'].value_counts().reset_index()
# data = data.drop(index=3)

data = data[:n]
data = data.sort_values('count', ascending=True)
type = st.selectbox('Type:',['BarPlot', 'DataFrame'])
if type=='BarPlot':
    Barplot(n,data)
else:
    DataFrame(n,data)

st.markdown("""---""")


