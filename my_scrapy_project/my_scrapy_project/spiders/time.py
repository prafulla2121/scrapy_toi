import scrapy

class TimesOfIndiaSpider(scrapy.Spider):
    name = 'time'
    start_urls = [
        'https://timesofindia.indiatimes.com/',
        'https://timesofindia.indiatimes.com/business',
        'https://timesofindia.indiatimes.com/sports',
        'https://timesofindia.indiatimes.com/entertainment',
        'https://timesofindia.indiatimes.com/world',
        'https://timesofindia.indiatimes.com/corona',
        'https://timesofindia.indiatimes.com/helth',
        'https://timesofindia.indiatimes.com/leptop',
        'https://timesofindia.indiatimes.com/cricket',
        'https://timesofindia.indiatimes.com/movies',
        'https://timesofindia.indiatimes.com/education',
        'https://timesofindia.indiatimes.com/crime',
        # Add more sections as needed
    ]

    custom_settings = {
        'FEED_FORMAT': 'csv',
        'FEED_URI': 'articles.csv',
        'FEED_EXPORT_ENCODING': 'utf-8',
        'LOG_LEVEL': 'INFO',  # Set log level to INFO to see progress
        'CONCURRENT_REQUESTS': 32,  # Increase concurrent requests
        'DOWNLOAD_DELAY': 0.5,  # Reduce delay to speed up scraping
    }

    def __init__(self, *args, **kwargs):
        super(TimesOfIndiaSpider, self).__init__(*args, **kwargs)
        self.link_count = 0  # Initialize link count
        self.seen_links = set()  # Set to track seen links

    def parse(self, response):
        # Extract article links that contain '/articleshow/'
        article_links = response.css('a::attr(href)').getall()
        toi_article_links = [link for link in article_links if '/articleshow/' in link]


        # Yield each article link and increment the count
        for link in toi_article_links:
            if link not in self.seen_links:  # Check for duplicates
                self.seen_links.add(link)  # Add to seen links
                self.link_count += 1  # Increment the count
                yield {
                    'article_link': link
                }

        # Follow pagination links
        next_page = response.css('a[rel="next"]::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)

        # Follow all other links on the page to find more articles
        for link in response.css('a::attr(href)').getall():
            if link.startswith('http') and link not in self.seen_links:
                yield response.follow(link, self.parse)

    def parse_article(self, response):
        # Extract article links from the article page
        article_links = response.css('a::attr(href)').getall()
        toi_article_links = [link for link in article_links if '/articleshow/' in link]

        # Yield each article link and increment the count
        for link in toi_article_links:
            if link not in self.seen_links:  # Check for duplicates
                self.seen_links.add(link)  # Add to seen links
                self.link_count += 1  # Increment the count
                yield {
                    'article_link': link
                }

        # Follow pagination links within the article if any
        next_page = response.css('a[rel="next"]::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse_article)

    def closed(self, reason):
        # This method is called when the spider is closed
        self.log(f'Total article links scraped: {self.link_count}')
        with open('link_count.txt', 'w') as f:
            f.write(f'Total article links scraped: {self.link_count}\n')
# import scrapy
# import pandas as pd

# class ToiArticleDetailsSpider(scrapy.Spider):
#     name = 'time'
    
#     def __init__(self, *args, **kwargs):
#         super(ToiArticleDetailsSpider, self).__init__(*args, **kwargs)
#         self.start_urls = self.get_article_links()

#     def get_article_links(self):
#         try:
#             df = pd.read_csv('articles.csv')  
#             return df['article_link'].dropna().unique().tolist()  
#         except Exception as e:
#             self.logger.error(f'Error reading CSV file: {e}')
#             return []

#     custom_settings = {
#         'FEED_FORMAT': 'json',
#         'FEED_URI': 'article_details.json',
#         'FEED_EXPORT_ENCODING': 'utf-8',
#         'LOG_LEVEL': 'INFO',
#         'CONCURRENT_REQUESTS': 32,  
#         'DOWNLOAD_DELAY': 0.5,
#     }

#     def parse(self, response):
#         title = response.css('h1.HNMDR span::text').get()
#         author = response.css('div.xf8Pm.byline a::text').get()
#         date = response.css('div.xf8Pm.byline span::text').get()

#         yield {
#             'article_link': response.url,
#             'title': title.strip() if title else 'N/A',
#             'author': author.strip() if author else 'N/A',
#             'date': date.strip() if date else 'N/A',
#         }
