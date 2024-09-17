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

## TAB 1 Functions
@st.cache_data
def funding_bar_plot(n,gk):
    gk = gk.iloc[0:n]
    st.bar_chart(gk,x='vertical',y='amount',color="#3182bd",horizontal=True,height=600,width=900)

@st.cache_data    
def year_wise(year):
    gk=df.groupby(['vertical','year'])['startup'].count().sort_values(ascending=False)
    gk=gk.reset_index()
    gk = gk[gk['year']==year]
    sorted_df = gk.sort_values(by='startup', ascending=False)
    gk = gk.iloc[0:10]
    st.bar_chart(gk,x ='vertical',y='startup',color ="#F5B041",height=550,width=900)
    
    

## Tab 1
with tab1:
    ## Barplot based on sum funding
    st.header("Top Verticals In India")
    st.subheader("Most Funded Verticals")
    n = st.slider("Select n:",2,25,5)
    gk=df.groupby('vertical')['amount'].sum().sort_values(ascending=False)
    gk=gk.reset_index()
    funding_bar_plot(n,gk)
    
    
    st.subheader("Top verticals during a given year")
    choice=st.selectbox("Select a year:",[x for x in range(2015,2021)])
    st.write("\n")
    year_wise(choice)
    
    

