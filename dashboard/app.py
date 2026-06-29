import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="News Data Platform")

st.title("📰 News Data Platform")

st.write("Article Summary")

response = requests.get(
    "http://news-api:8000/article-summary"
)

if response.status_code == 200:

    data = response.json()

    df = pd.DataFrame(data)

    st.dataframe(df)

    st.bar_chart(
        df.set_index("country")["article_count"]
    )

else:

    st.error("Unable to connect to API")