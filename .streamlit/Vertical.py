import streamlit as st
import pandas as pd
import seaborn as sns 
import matplotlib.pyplot as plt
import altair as alt

st.title("Major Startup Verticals In India")

tab1,tab2,tab3 = st.tabs(["Major Verticals","Startups","Compare Startups"])
st.write()

df = pd.read_csv("Final.csv")
df.columns = df.columns.str.replace(' ', '')

def line_plot(df,x,y):
    fig, ax = plt.subplots(figsize=(7, 3.5))
    fig.patch.set_facecolor('#0E1117') 
    ax.set_facecolor('#262730')
    sns.lineplot(data=df, x=x, y=y,color="Orange", ax=ax)

    ax.xaxis.set_tick_params(color='white')  
    ax.yaxis.set_tick_params(color='white')  
    ax.tick_params(axis='x', colors='white', labelsize=4)  
    ax.tick_params(axis='y', colors='white', labelsize=4)
    ax.xaxis.label.set_color('white')        
    ax.yaxis.label.set_color('white')        
    ax.title.set_color('white')
    st.pyplot(fig)
    
def bar_plot(df,x,y):
    fig, ax = plt.subplots(figsize=(7, 3.5))
    fig.patch.set_facecolor('#0E1117') 
    ax.set_facecolor('#262730')
    axis = sns.barplot(data=df, x=x, y=y, color="Orange", ax=ax)

    for container in axis.containers:
        axis.bar_label(container, fmt='%d', padding=3, color='white')
    ax.xaxis.set_tick_params(color='white',)  
    ax.yaxis.set_tick_params(color='white')  
    ax.tick_params(axis='x', colors='white',labelsize=5)  
    ax.tick_params(axis='y', colors='white',labelsize=5)
    ax.xaxis.label.set_color('white')        
    ax.yaxis.label.set_color('white')        
    ax.title.set_color('white')
    # ax.set_xscale('log', base=2)
    st.pyplot(fig)
    
## TAB 1 Functions
# @st.cache_data
def funding_bar_plot(n):
    gk=df.groupby('vertical')['amount'].sum().sort_values(ascending=False)
    gk=gk.reset_index()
    gk = gk.iloc[0:n]
    bar_plot(gk,'amount','vertical')
    
    
# @st.cache_data    
def year_wise(year):
    gk=df.groupby(['vertical','year'])['startup'].count().sort_values(ascending=False)
    gk=gk.reset_index()
    gk = gk[gk['year']==year]
    sorted_df = gk.sort_values(by='startup', ascending=False)
    sorted_df = sorted_df.iloc[0:10]
    bar_plot(sorted_df,"startup","vertical")

# @st.cache_data      
def vertical_analysis(choice):
    df_filtered = df[df['vertical']==choice]
    df_filtered = df_filtered.groupby('year')['startup'].count()
    df_filtered = df_filtered.reset_index()
    df_filtered['year'] = df_filtered['year'].astype(str)
    line_plot(df_filtered,'year','startup')
    

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
    
    ## Vertical Wise Analysis
    st.write("\n")
    st.subheader("Vertical Analysis")
    gk=df.groupby('vertical')['amount'].sum().sort_values(ascending=False)
    gk=gk.reset_index()
    choice = st.selectbox("Choose a vertical:",gk['vertical'].iloc[0:25])
    vertical_analysis(choice)
    
    

