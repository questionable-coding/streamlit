import streamlit as st
import requests
from bs4 import BeautifulSoup

def link_scraper(url):
    text = requests.get(url).text
    soup = BeautifulSoup(text, 'html.parser')
    links = [tag.get('href') for tag in soup.find_all('a') if tag.get('href')]
    return links

st.title('Simple Python Web Scraper')

col1, col2 = st.columns(2)

with col1:
    url = st.text_input('Enter target URL:')
    if st.button('Execute'):
        results = link_scraper(url)
        st.markdown('### Scraped Links:')
        with st.expander("See results here:"):
            for result in results:
                st.code((f'link: {result}').strip())

with col2:
    st.image('https://assets.bishopfox.com/prod-1437/Images/logos/partner-logos/NISOS-logo.png')
