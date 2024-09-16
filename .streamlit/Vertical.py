import streamlit as st
import pandas as pd
import seaborn as sns 
import matplotlib.pyplot as plt
st.title("Major Startup Verticals In India")

tab1,tab2,tab3 = st.tabs(["Major Verticals","Startups","Compare Startups"])
st.write()

df = pd.read_csv("Final.csv")
df.columns = df.columns.str.replace(' ', '')

## Tab 1
with tab1:
    st.header("Top Verticals In India")
    st.subheader("Most Funded Verticals")
    n = st.slider("Select n:",2,25,5)
    gk=df.groupby('vertical')['amount'].sum().sort_values(ascending=False)
    gk=gk.reset_index()
    # st.bar_chart(gk)
    fig, ax=plt.subplots()
    sns.barplot(x=gk.iloc[0:n,1], y=gk.iloc[0:n,0])
    st.pyplot(fig)

