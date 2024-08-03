import requests
from bs4 import BeautifulSoup
from django.http import JsonResponse
from .models import News, Tag

def fetch_rss_feed(request):
    url = 'https://www.zoomit.ir/feed'
    response = requests.get(url)
    response.encoding = 'utf-8' 
    if response.status_code != 200:
        return JsonResponse({'error': 'Failed to fetch RSS feed'}, status=500)

    soup = BeautifulSoup(response.content, 'xml')
    items = soup.find_all('item')

    articles = []
    for item in items:
        title = item.find('title').text if item.find('title') else 'No title'
        source = item.find('link').text if item.find('link') else 'No link'
        description = item.find('description').text if item.find('description') else 'No description'
        tags = [category.text for category in item.find_all('category')]

        # Fetch the full content of the article
        article_content = fetch_article_content(source)
        
        news_article, created = News.objects.get_or_create(
            title=title,
            source=source,
            defaults={'description': article_content}
        )

        if created:
            for tag_name in tags:
                tag, _ = Tag.objects.get_or_create(name=tag_name)
                news_article.tags.add(tag)

        articles.append({
            'title': title,
            'source': source,
            'description': article_content,
            'tags': tags,
        })

    return JsonResponse(articles, safe=False, json_dumps_params={'ensure_ascii': False})

def fetch_article_content(url):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return 'No content'

        soup = BeautifulSoup(response.content, 'html.parser')
        article_content = []
        article = soup.find('article')
        if article:
            paragraphs = article.find_all('p')
            for paragraph in paragraphs:
                article_content.append(paragraph.text)

        return ' '.join(article_content)
    except requests.RequestException as e:
        print(f"Error fetching article content: {e}")
        return 'No content'
