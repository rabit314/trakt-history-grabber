import requests
from bs4 import BeautifulSoup

# Function to extract titles from a single page
def extract_titles_from_page(page_url):
    response = requests.get(page_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    titles = [title.get_text() for title in soup.find_all('h3', class_='ellipsify')]
    
    # Check if there is a "next" button to determine if there's another page
    next_page = soup.find('li', class_='next')
    
    return titles, bool(next_page)

# Base URL for your watch history
base_url = "https://trakt.tv/users/rabit7/history/all/added?page={}"

# List to store all the titles
all_titles = []

# Start from the first page
page_num = 1

while True:
    page_url = base_url.format(page_num)
    titles, has_next_page = extract_titles_from_page(page_url)
    all_titles.extend(titles)
    print(f"Page {page_num} scraped, {len(titles)} titles found.")
    
    if not has_next_page:
        break
    
    page_num += 1

# Save the titles to a plain text file
with open("trakt_watch_history.txt", "w", encoding="utf-8") as file:
    for title in all_titles:
        file.write(title + "\n")

print(f"Scraping complete. {len(all_titles)} titles saved to trakt_watch_history.txt.")
