import streamlit as st 
import pandas as pd 
from io import BytesIO
from functions import bar_line_and_df

st.set_page_config(layout='wide',page_title='StartUp Funding Analysis')
df = pd.read_csv('startup_funding.csv')

st.title("Home")

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


col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric('\# Fundings', str(funded_ct))
with col2:
    st.metric('\# Startups', str(funded_stups))
with col3:
    st.metric('\# Investors', str(investor_ct))
with col4:
    st.metric('\# Hubs', str(hubs))
st.caption('\# Features:  Number of Features')
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

st.header("Indian Startup Hubs")
data = pd.read_csv('cities.csv')
data = data[(data['lat'] >= 8.4) & (data['lat'] <= 37.6) & 
                  (data['lon'] >= 68.7) & (data['lon'] <= 97.25)]
data = data.iloc[:,2:4]
st.map(data,  color = '#86FD02')

st.markdown("""---""")


# def plot_style(type):
#         fig, ax = plt.subplots(figsize=(10, 6))
#         fig.patch.set_facecolor('#0E1117') 
#         ax.set_facecolor('#262730')
#         ax.xaxis.set_tick_params(color='white',)  
#         ax.yaxis.set_tick_params(color='white')
#         if(type == 'Barplot'):
#             ax.tick_params(axis='x', colors='white')  
#             ax.tick_params(axis='y', colors='white')
#         else:
#             ax.tick_params(axis='x', colors='white', labelsize=10)  
#             ax.tick_params(axis='y', colors='white', labelsize=10)
#         ax.xaxis.label.set_color('white')        
#         ax.yaxis.label.set_color('white')        
#         ax.title.set_color('white')
#         return fig,ax


st.header('Year Wise Analysis')
col1, col2 = st.columns(2)

with col1:
    year_wise = 'Amount Funded'
    st.subheader("Amount Funded Year Wise")
    subtype = st.selectbox("Subtype",['Barplot','Lineplot','DataFrame'])
    data = df.groupby(by='year')['amount'].sum()
    bar_line_and_df(data, subtype, year_wise)

with col2:
    year_wise = '# Fundings'
    st.subheader("Number of Fundings Year Wise")
    subtype = st.selectbox("SubType",['Barplot','Lineplot','DataFrame'])
    data = df[df['amount'] > 0]
    data = data['year'].value_counts()
    bar_line_and_df(data, subtype, year_wise)

# fig, ax = plt.subplots(figsize=(10, 6))
# plt.plot(range(len(df['amount'])),df['amount'],marker='o')
# st.pyplot(fig)

st.markdown("""---""")

# download_plot(bars,"State_wise_startup_ct", f"State_wise_starup_ct.png")
