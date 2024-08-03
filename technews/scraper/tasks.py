from celery import shared_task
import requests
from bs4 import BeautifulSoup

@shared_task

def fetch_rss_feed(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch RSS feed. Status code: {response.status_code}")
        return []

    soup = BeautifulSoup(response.content, 'xml')
    items = soup.find_all('item')

    articles = []
    for item in items:
        title = item.find('title').text if item.find('title') else 'No title'
        link = item.find('link').text if item.find('link') else 'No link'
        description = item.find('description').text if item.find('description') else 'No description'
        tags = [category.text for category in item.find_all('category')]

        # Fetch the full content of the article
        article_content = fetch_article_content(link)
        
        articles.append({
            'title': title,
            'link': link,
            'description': description,
            'tags': tags,
            'full_content': article_content
        })

    return articles
@shared_task(name="fetch_article_content")
def fetch_article_content(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch article content from {url}. Status code: {response.status_code}")
        return 'No content'

    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract full content from <article> and <p> tags
    article_content = []
    article = soup.find('article')
    if article:
        paragraphs = article.find_all('p')
        for paragraph in paragraphs:
            article_content.append(paragraph.text)
    
    return ' '.join(article_content)

# Example
if __name__ == "__main__":
    rss_url = 'https://www.zoomit.ir/feed'
    articles = fetch_rss_feed(rss_url)
    for article in articles:
        print("Title:", article['title'])
        print("Link:", article['link'])
        print("Description:", article['description'])
        print("Tags:", article['tags'])
        print("Full Content:", article['full_content'])
