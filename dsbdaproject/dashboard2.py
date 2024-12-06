import streamlit as st
import plotly.express as px
import pandas as pd 
import matplotlib.pyplot as plt
import os
import warnings
import seaborn as sns
import base64
warnings.filterwarnings('ignore')

# setting the web page title
st.set_page_config(page_title="Covid-19 Vaccination India State-wise Progress",page_icon=":earth_asia:",layout="wide")

#Settin the web page Heading
st.write('<h1 style="text-align:center; color:#4EBAEB; background-color:white; margin-top:-4rem; width:100%; border: 1px solid #333; box-shadow:2px 2px 10px #333; font-family:roboto; text-shadow:2px 2px 4px #4EBAEB; ">Covid-19 Vaccination Navigator</h1>',unsafe_allow_html=True)
st.markdown('<style>div.block-container{ background-color:#D0F2FA;}</style>',unsafe_allow_html=True)

#setting the web file uploader div
container = st.container()

with container:
    st.write('<hr style="background-color:red;">',unsafe_allow_html=True)
    fl = st.file_uploader(":file_folder: Upload Your file" , type=(["csv"]))
    if fl is not None:
        filename = fl.name
        st.write(filename)
        df = pd.read_csv(filename, encoding ="ISO-8859-1")
    else:
        os.chdir("E:\\JN")
        df = pd.read_csv("covid_vaccine_statewise.csv",encoding ="ISO-8859-1")


st.write('<hr style="background-color:red;">',unsafe_allow_html=True)

#sidebar 
st.sidebar.header("Select Your Desired Options :")
st.sidebar.write('<hr style=" margin:1rem 0rem; background-color:red;">',unsafe_allow_html=True)
state = st.sidebar.multiselect("Select Your State :",df["State"].unique())
date = st.sidebar.multiselect("Select Your Date :",df["Updated On"].unique())

if not state and not date:
    filtered_df = df
elif not date:
    filtered_df = df[df["State"].isin(state)]
elif not state:
    filtered_df = df[df["Updated On"].isin(date)]
elif state and date:
    filtered_df = df[(df["State"].isin(state)) & (df["Updated On"].isin(date))]
else:
    filtered_df = df[(df["State"].isin(state)) & (df["Updated On"].isin(date))]

st.write(filtered_df)
st.write('<h5 style="color:blue;">&bull; Download Dataset From Here:</h5>',unsafe_allow_html=True)


#for downloading the filtered dataset:

def download_csv(dataframe, filename):
    csv = dataframe.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}.csv">Download CSV</a>'
    return href
st.markdown(download_csv(filtered_df, 'filtered_data'), unsafe_allow_html=True)

st.sidebar.write('<hr style=" margin:1rem 0rem; background-color:red;">',unsafe_allow_html=True)

st.write('<hr style="background-color:red;">',unsafe_allow_html=True)


#creating two columns:
col1, col2 = st.columns([0.5,0.5])



with col1 :
    st.write('<h4 style="color:red; text-decoration:underline black solid;">&bull; State wise total Vaccination Dose Administered: </h4>',unsafe_allow_html=True)

    fig = px.pie(df, values='Total Doses Administered', names='State', title='Vaccination Counts by State')
    fig.update_layout(template="gridon", height=500)
    st.plotly_chart(fig,use_container_width=True)

with col2 :
    st.write('<h4 style="color:red; text-decoration:underline black solid;">&bull; Total Vaccination Dose Administered Per Day In India: </h4>',unsafe_allow_html=True)

    fig = px.bar(df,x="Updated On",y="Total Doses Administered", title='Total vaccination per day',template="gridon",height=500)

    st.plotly_chart(fig,use_container_width=True)
    
st.divider()

_, col3 = st.columns([0.05,0.95])

with col3:
    st.write('<h4 style="color:red; text-decoration:underline black solid;">&bull; Gender Wise total Vaccination per State:</h4>',unsafe_allow_html=True)

    fig = px.bar(df, x="State",y=["Male(Individuals Vaccinated)","Female(Individuals Vaccinated)","Transgender(Individuals Vaccinated)"],template="gridon",height=400)
    fig.update_layout(yaxis=dict(title='Gender wise Total Dose'), yaxis2=dict(title='Vaccination', overlaying='y', side='right'))
    st.plotly_chart(fig,use_container_width=True)

with col3:
    st.write('<h4 style="color:red; text-decoration:underline black solid;">&bull; Brand Wise Vaccination Per state:</h4>',unsafe_allow_html=True)

    fig = px.bar(df, x="State",y=[" Covaxin (Doses Administered)","CoviShield (Doses Administered)"],template="gridon",height=400)
    fig.update_layout(yaxis=dict(title='Brand wise Total Dose'), yaxis2=dict(title='Vaccination', overlaying='y', side='right'))
    st.plotly_chart(fig,use_container_width=True)

st.write('<hr style="background-color:red;">',unsafe_allow_html=True)

st.divider()