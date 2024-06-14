import re
import os
import requests
import streamlit as st

# Function to build the payload for Google Custom Search API
def build_payload(query, start=1, num=10, **params):
    payload = {
        'key': API_KEY,
        'q': query,
        'cx': SEARCH_ENGINE_ID,
        'start': start,
        'num': num
    }
    payload.update(params)
    return payload

# Function to make requests to the Google Custom Search API
def make_requests(payload):
    response = requests.get('https://www.googleapis.com/customsearch/v1', params=payload)
    if response.status_code != 200:
        raise Exception(f'Request failed with status code: {response.status_code}')
    return response.json().get('items', [])

# Function to extract URLs from the search results
def extract_urls(search_results):
    return [item['link'] for item in search_results]

# Main function to manage multiple pages of search results
def main(query, result_total=10):
    urls = []
    pages = (result_total // 10) + (1 if result_total % 10 else 0)
    for i in range(pages):
        num_results = result_total - len(urls) if pages == i + 1 else 10
        payload = build_payload(query, start=i * 10 + 1, num=num_results)
        response_items = make_requests(payload)
        urls.extend(extract_urls(response_items))
    return urls

# Function to fetch text content from a URL
def get_text_from_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f'Error fetching URL: {url}. Error: {e}')
        return None

# Function to search for keywords in text
def search_keywords_in_text(text, keywords):
    if text is None:
        return {keyword: [] for keyword in keywords}
    return {keyword: re.findall(r'\b' + re.escape(keyword) + r'\b', text, re.IGNORECASE) for keyword in keywords}

# Function to write results to a file
def write_results_to_file(results, filename):
    with open(filename, 'w') as file:
        for url, matches in results.items():
            file.write(f'URL: {url}\n')
            keywords_found = [keyword for keyword, matches_list in matches.items() if matches_list]
            if keywords_found:
                file.write('Keywords found: ' + ', '.join(keywords_found) + '\n')
            else:
                file.write('No keywords found\n')
            file.write('\n')

# Main Execution Code
if __name__ == '__main__':
    # Prompt for API key and Search Engine ID if not set as environment variables
    API_KEY = os.getenv('GOOGLE_API_KEY', input('Enter Google API Key: ').strip())
    SEARCH_ENGINE_ID = os.getenv('GOOGLE_SEARCH_ENGINE_ID', input('Enter Google Search Engine ID: ').strip())

    if not API_KEY or not SEARCH_ENGINE_ID:
        print("API_KEY and SEARCH_ENGINE_ID must be provided.")
    else:
        query = input('Enter search query: ')
        result_total = int(input('Enter total number of results: '))
        search_keywords = ['youtube.com', 'vk.com', 'twitter.com', 'instagram.com', 'facebook.com',
                           'wordpress.com', 'rumble.com', 'odysse.com', 'bitchute.com', 'truthsocial.com', 'telegram.com']

        urls = main(query, result_total)
        results = {}
        for url in urls:
            print(f'Searching keywords in {url}...')
            text = get_text_from_url(url)
            matches = search_keywords_in_text(text, search_keywords)
            results[url] = matches

        write_results_to_file(results, 'results.txt')
        print("Results have been written to 'results.txt'")

# Streamlit App Code
st.title('Simple Python Web Scraper')

col1, col2 = st.columns(2)

with col1:
    query = st.text_input('Enter search query:')
    result_total = st.number_input('Enter total number of results:', min_value=1, max_value=100, value=10, step=1)
    search_keywords = st.text_area('Enter keywords to search (comma separated):',
                                   value='youtube.com, vk.com, twitter.com, instagram.com, facebook.com, '
                                         'wordpress.com, rumble.com, odysse.com, bitchute.com, truthsocial.com, telegram.com').split(',')

    if st.button('Execute'):
        urls = main(query, result_total)
        results = {}
        for url in urls:
            st.write(f'Searching keywords in {url}...')
            text = get_text_from_url(url)
            matches = search_keywords_in_text(text, search_keywords)
            results[url] = matches

        write_results_to_file(results, 'results.txt')
        st.markdown('### Results:')
        st.download_button(label="Download results", file_name="results.txt", data=open('results.txt').read())

with col2:
    st.image('https://res.cloudinary.com/upwork-cloud/image/upload/c_scale,w_1000/v1692294214/catalog/1692228747201867776/kwjevm8b3trftznernot.jpg')
