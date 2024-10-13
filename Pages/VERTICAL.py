import streamlit as st
import pandas as pd
import seaborn as sns 
import matplotlib.pyplot as plt
import altair as alt

st.set_page_config(layout='wide',page_title="Major Startup Verticals In India")

tab1,tab2 = st.tabs(["Major Verticals","Compare Verticals"])
st.write()

df = pd.read_csv("startup_funding.csv")


def line_plot(df,x,y,n):
    line_chart = alt.Chart(df).mark_line(color='Orange').encode(
        x=x,
        y=y,
        tooltip=[x, y]
    )
    st.altair_chart(line_chart, use_container_width=True)
def bar_plot(df,x,y,n):
    bh = 68
    min_bh = 450
    ch = max(n * bh, min_bh)
    
    bar_chart = alt.Chart(df).mark_bar(color="orange").encode(
       x=x,
       y=alt.Y(y,sort='-x'),
       tooltip=[x,y]
    ).properties(
        width=700,  # Set the width of the chart
        height=ch,  # Set the height of the chart
    )
    
    highlight = alt.selection_single(on='mouseover', empty='none')
    
    bar_chart = bar_chart.encode(
            color=alt.condition(highlight, alt.value('red'), alt.value('orange')),
            size=alt.condition(highlight, alt.value(55), alt.value(35))  # Enlarges on hover
        ).add_selection(
            highlight
        )
    st.altair_chart(bar_chart, use_container_width=True)
    
## TAB 1 Functions
# @st.cache_data
def funding_bar_plot(n):
    gk=df.groupby('vertical')['amount'].sum().sort_values(ascending=False)
    gk=gk.reset_index()
    gk = gk.iloc[0:n]
    bar_plot(gk,'amount','vertical',n)
    
    
# @st.cache_data    
def year_wise(year):
    gk=df.groupby(['vertical','year'])['startup'].count().sort_values(ascending=False)
    gk=gk.reset_index()
    gk = gk[gk['year']==year]
    sorted_df = gk.sort_values(by='startup', ascending=False)
    sorted_df = sorted_df.iloc[0:10]
    bar_plot(sorted_df,"startup","vertical",10)

# @st.cache_data      
def vertical_analysis(choice,selection):
    df_filtered = df[df['vertical']==choice]
    df_filtered = df_filtered.groupby('year')['startup'].count()
    df_filtered = df_filtered.reset_index()
    df_filtered['year'] = df_filtered['year'].astype(str)
    if selection == "DataFrame":
        return df_filtered
    line_plot(df_filtered,'year','startup',n)
    
    
def funding_analysis(choice,selection):
    gk = df.groupby(['vertical','year'])['amount'].sum()
    gk = gk.reset_index()
    gk = gk[gk['vertical']==choice]
    gk['year']=gk['year'].astype(str)
    if selection=="DataFrame":
        return gk
    line_plot(gk,'year','amount',n)

## Tab 1
with tab1:
    ## Barplot based on sum funding
    st.header("Top Verticals In India")
    st.subheader("Most Funded Verticals")
    n = st.slider("Select n:",2,25,5)
    funding_bar_plot(n)
    st.write("\n")
    
    ## Barplot based on no of startups in every vertical per year
    st.subheader("Top verticals during a given year")
    choice=st.selectbox("Select a year:",[x for x in range(2015,2021)])
    st.write("\n")
    year_wise(choice)
    
    
    st.write("\n")
    st.header("Vertical Analysis")
    gk=df.groupby('vertical')['amount'].sum().sort_values(ascending=False)
    gk=gk.reset_index()
    choice = st.selectbox("Choose a vertical:",gk['vertical'].iloc[0:25])
    
    st.subheader(f"Major Hubs Of {choice}")
    df['city'] = df['city'].str.replace(" ","",regex=False)
    
    fk = df[df['vertical']==choice]
    citi = pd.read_csv('cities.csv')
    citi['city'] = citi['city'].str.replace(" ","",regex=False)
    # citi.to_csv('cities.csv')
    merged_data = citi[citi['city'].isin(fk['city'])]
    
    if 'lat' in merged_data.columns and 'lon' in merged_data.columns:
        st.map(merged_data[['lat', 'lon']], color='#86FD02')
    else:
        st.error("The city data is missing 'latitude' and 'longitude' columns.")
    
    
    col1,col2 = st.columns(2)
    with col1:
        ## Vertical Wise Analysis
        st.subheader("Number of Startups vs Year")
        selection = st.selectbox("Options",['Lineplot','DataFrame'],key='selectbox2')
        if(selection=="Lineplot"):
            vertical_analysis(choice,selection)
            
        else:
            
            data_frame = vertical_analysis(choice,selection)
            st.dataframe(data_frame.style.set_properties(**{'background-color': '#262730','text-align': 'center',}))
        st.write("\n")
    
    
    with col2:
        ## Funding analysis
        st.subheader("Funding vs Year")
        selection = st.selectbox("Options",['Lineplot','DataFrame'],key='selectbox1')
        if(selection=="Lineplot"):
            funding_analysis(choice,selection)
            
        else: 
            data_frame = funding_analysis(choice,selection)
            data_frame.drop(columns='vertical',inplace=True)
            data_frame=data_frame.reset_index()
            data_frame.drop(columns='index',inplace=True)
            st.dataframe(data_frame.style.set_properties(**{'background-color': '#262730','text-align': 'center'}))
        st.write("\n")
        
    
    

## Tab2:
with tab2:
    gk=df.groupby('vertical')['amount'].sum().sort_values(ascending=False)
    gk=gk.reset_index()
    gk = gk.iloc[0:n]
    
    st.header("Compare Verticals")
    col1,col2 = st.columns(2)
    
    with col1:
        choice = st.selectbox("Choose a vertical",[gk['vertical']],key= 'selectbox3')
        st.subheader(f"{choice}")
        
        