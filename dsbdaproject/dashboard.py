import streamlit as st
import plotly.express as px
import pandas as pd 
import matplotlib.pyplot as plt
import os
import warnings
import seaborn as sns
warnings.filterwarnings('ignore')

st.set_page_config(page_title="Covid-19 Tweet Sentiment Analysis",page_icon=":earth_asia:",layout="wide")

# st.title(":earth_asia: Tweet Analysis Dashboard ")
st.write('<h1 style="color:red; width:100%; border:1px solid black; text-align:center; box-shadow:2px 2px 5px black; background-color:#6E7171; -webkit-text-stroke-width: 1px; -webkit-text-stroke-color: black; text-shadow:0px 2px 5px white;">Tweet Analysis Dashboard</h1>',unsafe_allow_html=True)
st.markdown('<style>div.block-container{ background-color:azure; border:solid black 2px; box-shadow:2px 2px 5px black;}</style>' ,unsafe_allow_html=True)
st.divider()

fl = st.file_uploader(":file_folder: Upload Your file" , type=(["csv"]))
if fl is not None:
    filename = fl.name
    st.write(filename)
    df = pd.read_csv(filename, encoding ="ISO-8859-1")
else:
    os.chdir("E:\\JN")
    df = pd.read_csv("Corona_NLP_train.csv",encoding ="ISO-8859-1")

st.divider()
st.subheader(":desktop_computer: View of Filtered Dataset:")

#sidebar
st.sidebar.header(" :arrow_down: Choose Your Filter:")
#for locattion
country1 = st.sidebar.multiselect("Pick Your Country:" , df["Location"].unique())
#for Date
tweetat = st.sidebar.multiselect("Pick Your Date:", df["TweetAt"].unique())

#filter the data for locaton and date
if not country1 and not tweetat :
    filtered_df =df
elif not tweetat:
    filtered_df = df[df["Location"].isin(country1)]
elif not country1:
    filtered_df = df[df["TweetAt"].isin(tweetat)]
elif country1 and tweetat:
    filtered_df = df[df["Location"].isin(country1) & df["TweetAt"].isin(tweetat)]
else:
    filtered_df = df[df["location"].isin(country1) & df["TweetAt"].isin(tweetat)]
st.write(filtered_df)

#setting date columns
col1, col2 = st.columns((2))
df["TweetAt"] = pd.to_datetime(df["TweetAt"])

#getting the min and max date
startDate = pd.to_datetime(df["TweetAt"]).min()
endDate = pd.to_datetime(df["TweetAt"]).max()

with col1:
    date1 = pd.to_datetime(st.date_input("Start Date", startDate))

with col2:
    date2 = pd.to_datetime(st.date_input("End Date", endDate))

df= df[(df["TweetAt"]>=date1) & (df["TweetAt"]<=date2)].copy()


category_df = filtered_df.groupby(by = ["OriginalTweet"], as_index = False)["Sentiment"].sum()
st.divider()

with col1:
    st.write('<h3 style="color:red; text-decoration:underline solid black; margin:1rem 0rem;"> &bull; Tweet counts by location:</h3>',unsafe_allow_html=True)
    #conting tweet per location
    location_counts = df.groupby('Location').size().reset_index(name='Tweet Count')

    #ploting the bar charts
    fig = px.bar(location_counts, x='Location', y='Tweet Count', title='Tweet Counts by Location')

    #passing fig object to the plotly_chart
    st.plotly_chart(fig)

with col1:
    st.write('<h3 style="color:red; text-decoration:underline solid black; margin:1rem 0rem;"> &bull; Tweet Sentiment Analysis:</h3>',unsafe_allow_html=True)
    #count the total tweets per sentiment
    sentiment_counts = df['Sentiment'].value_counts()

    #plotting the pie chart
    fig, ax = plt.subplots(figsize=(8, 6))
    sentiment_counts.plot(kind='pie', autopct='%1.1f%%', startangle=140, ax=ax)
    plt.title('Sentiment Analysis')
    plt.ylabel('')

    #passing fig to the pyplot()
    st.pyplot(fig)