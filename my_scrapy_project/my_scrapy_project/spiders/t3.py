import scrapy
import json
import pandas as pd

class BusinessStandardSpider(scrapy.Spider):
    name = "b3"

    # Load URLs from a CSV file
    def start_requests(self):
        # Load the CSV file
        urls_df = pd.read_csv('scraped_links.csv')  # Ensure the CSV has a column named "url"
        for index, row in urls_df.iterrows():
            yield scrapy.Request(url=row['url'], callback=self.parse)

    # Parse the response
    def parse(self, response):
        # Extract the script content with JSON data
        script_data = response.xpath('//script[@id="__NEXT_DATA__"]/text()').get()

        if script_data:
            try:
                # Load JSON content
                data = json.loads(script_data)

                # Extract the required fields from the JSON
                title = data.get('props', {}).get('pageProps', {}).get('title', 'No Title')
                body = data.get('props', {}).get('pageProps', {}).get('description', 'No Content')
                date = data.get('props', {}).get('pageProps', {}).get('datePublished', 'No Date')
                keywords = data.get('props', {}).get('pageProps', {}).get('keywords', 'No Keywords')

                # Yield the scraped data
                yield {
                    "title": title.strip(),
                    "body": body.strip(),
                    "date": date.strip(),
                    "keywords": keywords.strip()
                }

            except json.JSONDecodeError:
                self.logger.error("Failed to parse JSON data from: %s", response.url)

