import streamlit as st
from scrape import scrape_site

st.title("AI Web Scraper")
url = st.text_input("Enter a URL:")

if st.button("Scrape Site"):
    st.write("Scraping site...")
    # Scrape the site here
    result = scrape_site(url)
    st.write("Scraping complete!")

    print(result)
