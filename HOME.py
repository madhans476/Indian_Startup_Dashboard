import math
import altair as alt
import streamlit as st 
import pandas as pd 
import matplotlib.pyplot as plt 
from io import BytesIO

st.set_page_config(layout='wide',page_title='StartUp Funding Analysis')
df = pd.read_csv('startup_funding.csv')

st.title("Home")
# statiscal measures
t_amt = df['amount'].sum()
avg = df['amount'].mean()
med = df['amount'].median()
max_v = df['amount'].max()
funded_ct = df[df['amount']!=0]['startup'].count()
funded_stups = df[df['amount']!=0]['startup'].unique().size
investor_ct = df['investors'].unique().size
hubs = df['city'].unique().size

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric('Total ₹', str(round(t_amt)) + ' cr')
with col2:
    st.metric('Maximum ₹', str(round(max_v)) + ' cr')
with col3:
    st.metric('Average ₹', str(round(avg)) + ' cr')
with col4:
    st.metric('Median ₹', str(round(med)) + ' cr')

st.write('\# Feature:  Number of Features')

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric('\# Fundings', str(funded_ct))
with col2:
    st.metric('\# Startups', str(funded_stups))
with col3:
    st.metric('\# Investors', str(investor_ct))
with col4:
    st.metric('\# Hubs', str(hubs))
st.markdown("""---""")

color1 = 'Orange'
color2 = '#03B3FD'


# from geopy.geocoders import ArcGIS

# def get_lat_lon(city_name):
#     geolocator = ArcGIS()
#     location = geolocator.geocode(city_name)
#     if location:
#         return location.latitude, location.longitude
#     else:
#         return None, None

# cities = df['city'].unique()
# lat, lon ,citi = [], [],[]
# for i in cities:
#     v = get_lat_lon(i)
#     lat.append(v[0])
#     lon.append(v[1])
#     citi.append(i)

# data = pd.DataFrame({'city': citi,'lat': lat, 'lon':lon})
# data = data[(data['lat'] >= 8.4) & (data['lat'] <= 37.6) & 
#                   (data['lon'] >= 68.7) & (data['lon'] <= 97.25)]
# data.to_csv('cities.csv')
st.subheader("Indian Startup Hubs")
data = pd.read_csv('cities.csv')
data = data[(data['lat'] >= 8.4) & (data['lat'] <= 37.6) & 
                  (data['lon'] >= 68.7) & (data['lon'] <= 97.25)]
data = data.iloc[:,2:4]
st.map(data,  color = '#86FD02')

st.markdown("""---""")
st.header('Year Wise Analysis')
col1, col2 = st.columns(2)


def download_plot(fig, label, name):
    img_buffer = BytesIO()
    fig.savefig(img_buffer, format="png")
    img_buffer.seek(0)
        # Add a download button for the plot
    st.download_button(
            label=f":arrow_down: {label}",
            data=img_buffer,
            file_name=name,
            mime="image/png"
        )

def plot_style(type):
        fig, ax = plt.subplots(figsize=(10, 6))
        fig.patch.set_facecolor('#0E1117') 
        ax.set_facecolor('#262730')
        ax.xaxis.set_tick_params(color='white',)  
        ax.yaxis.set_tick_params(color='white')
        if(type == 'Barplot'):
            ax.tick_params(axis='x', colors='white')  
            ax.tick_params(axis='y', colors='white')
        else:
            ax.tick_params(axis='x', colors='white', labelsize=10)  
            ax.tick_params(axis='y', colors='white', labelsize=10)
        ax.xaxis.label.set_color('white')        
        ax.yaxis.label.set_color('white')        
        ax.title.set_color('white')
        return fig,ax

def line_and_df(data, subtype, year_wise):
    data = data.reset_index()
    s = 'Counts'
    if year_wise == 'Amount Funded':
        s = 'Total ₹ (Cr)'
    data.columns = ['Year', s]
    
    if subtype == 'Barplot':
        # fig, ax = plot_style(subtype)
        # axis = sns.barplot(x=data['Year'], y=data[s],color="Orange", ax=ax)

        # # Add labels to the bars
        # for container in axis.containers:
        #     axis.bar_label(container, fmt='%d', padding=3, color='white')
        # ax.tick_params(axis='x', colors='white')  
        # ax.tick_params(axis='y', colors='white')
        # ax.set_title(f'{s} Over Years', fontsize=16)
        # ax.set_xlabel('Year', fontsize=12)
        # ax.set_ylabel(f'{s}', fontsize=12)
        # st.pyplot(fig)
        # download_plot(fig, year_wise, f"{year_wise}_{subtype}.png")

        bars = alt.Chart(data).mark_bar(size=35).encode(
            x=alt.X('Year:N', title='Year'),
            y=alt.Y(f'{s}:Q', title=s),
            color=alt.value(color1),
            tooltip=[
            alt.Tooltip("Year", title="Year: "),
            alt.Tooltip(s, title=f'{s}: ', format='.0f'),
        ],
        ).properties(
            height = 350,
        ).configure_axis(
            labelAngle= 0,
            labelFontSize=12,
        )

        # Hover interaction
        highlight = alt.selection_single(on='mouseover', empty='none')

        # Chart with hover effect
        bars = bars.encode(
            color=alt.condition(highlight, alt.value(color2), alt.value(color1)),
            size=alt.condition(highlight, alt.value(55), alt.value(35))  # Enlarges on hover
        ).add_selection(
            highlight
        )

        st.altair_chart(bars, use_container_width=True)

    elif subtype == 'Lineplot':
        #! Static plot
        # fig, ax = plot_style(subtype)
        # sns.lineplot(x=data['Year'], y=data[s], marker='o', color=color1, linewidth=2.5)
        # ax.set_title(f'{s} Over Years', fontsize=16)
        # ax.set_xlabel('Year', fontsize=12)
        # ax.set_ylabel(f'{s}', fontsize=12)

        # st.pyplot(fig)
        # download_plot(fig, year_wise, f"{year_wise}_{subtype}.png")
        hover = alt.selection_single(on='mouseover', nearest=True, empty='none', fields=['Year'])

        line_chart = alt.Chart(data).mark_line(color=color1, point=True).encode(
            x=alt.X('Year:O', title='Year', axis=alt.Axis(labelAngle=0)),
            y=alt.Y(f'{s}:Q', title=f'{s}',),
            tooltip=[
            alt.Tooltip("Year", title="Year: "),
            alt.Tooltip(s, title=f'{s}: ', format='.0f'),
        ]
        ).properties(
            width=600,
            height=400
        )

        # Add hover effect for color change
        highlight_points = line_chart.mark_circle(size=100).encode(
            color=alt.condition(hover, alt.value(color2), alt.value(color1)),
            size=alt.condition(hover, alt.value(150), alt.value(100))
        ).add_selection(
            hover
        )

        # Combine line chart and highlighted points
        final_chart = (line_chart + highlight_points).properties(
        ).configure_axis(
            labelColor='white',
            labelAngle=0,
            grid=False
        ).configure_view(
            strokeWidth=0
        ).configure_title(
            color='white',
            fontSize=16
        ).configure()  # Apply background config here

        # Display the chart in Streamlit
        st.altair_chart(final_chart, use_container_width=True)
    else:            
        data['Year'] = data['Year'].astype(str)
        st.write('Data Overview:')
        st.dataframe(data.style.set_properties(**{
            'background-color': '#262730',
            'border': '1px solid black',
            # 'color': 'black',
            'text-align': 'center'
        }))

with col1:
    year_wise = 'Amount Funded'
    st.subheader("Amount Funded Year Wise")
    subtype = st.selectbox("Subtype",['Barplot','Lineplot','DataFrame'])
    data = df.groupby(by='year')['amount'].sum()
    line_and_df(data, subtype, year_wise)

with col2:
    year_wise = '# Fundings'
    st.subheader("Number of Fundings Year Wise")
    subtype = st.selectbox("SubType",['Barplot','Lineplot','DataFrame'])
    data = df['year'].value_counts()
    line_and_df(data, subtype, year_wise)

# fig, ax = plt.subplots(figsize=(10, 6))
# plt.plot(range(len(df['amount'])),df['amount'],marker='o')
# st.pyplot(fig)

st.markdown("""---""")

# download_plot(bars,"State_wise_startup_ct", f"State_wise_starup_ct.png")
