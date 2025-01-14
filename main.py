import streamlit as st
from scrape import scrape_site

st.title("AI Web Scraper")
url = st.text_input("Enter a URL:")
