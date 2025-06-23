#!/usr/bin/env python3
"""
Scrapy-based URL extractor that crawls a website and extracts all URLs.
Generates two output files: All_URLs.txt and All_Unique_URLs.txt
"""

import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.log import configure_logging
from urllib.parse import urljoin, urlparse
import sys
import os
import logging
from collections import OrderedDict


class URLExtractorSpider(scrapy.Spider):
    name = 'url_extractor'
    
    def __init__(self, start_url=None, *args, **kwargs):
        super(URLExtractorSpider, self).__init__(*args, **kwargs)
        
        if not start_url:
            raise ValueError("start_url is required")
        
        # Normalize the URL - add https if no protocol specified
        self.start_url = self.normalize_url(start_url)
        self.start_urls = [self.start_url]
        
        # Extract domain for filtering
        parsed_url = urlparse(self.start_url)
        self.allowed_domains = [parsed_url.netloc]
        
        # Storage for URLs
        self.all_urls = []
        self.unique_urls = OrderedDict()  # Maintains insertion order while removing duplicates
    
    def normalize_url(self, url):
        """Normalize URL by adding protocol if missing"""
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        return url
    
    def parse(self, response):
        """Parse response and extract all URLs"""
        # Extract all links from the page
        links = response.css('a::attr(href)').getall()
        
        for link in links:
            if link:
                # Convert relative URLs to absolute URLs
                absolute_url = urljoin(response.url, link)
                
                # Store all URLs (including duplicates)
                self.all_urls.append(absolute_url)
                
                # Store unique URLs
                self.unique_urls[absolute_url] = True
                
                # Follow links within the same domain
                parsed_link = urlparse(absolute_url)
                if parsed_link.netloc in self.allowed_domains:
                    yield scrapy.Request(
                        url=absolute_url,
                        callback=self.parse,
                        dont_filter=False  # Allow Scrapy's built-in duplicate filtering
                    )
    
    def closed(self, reason):
        """Called when the spider is closed - write results to files"""
        self.logger.info(f'Spider closed: {reason}')
        self.logger.info(f'Total URLs found: {len(self.all_urls)}')
        self.logger.info(f'Unique URLs found: {len(self.unique_urls)}')
        
        # Write all URLs to file
        with open('All_URLs.txt', 'w', encoding='utf-8') as f:
            for url in self.all_urls:
                f.write(url + '\n')
        
        # Write unique URLs to file
        with open('All_Unique_URLs.txt', 'w', encoding='utf-8') as f:
            for url in self.unique_urls:
                f.write(url + '\n')
        
        print(f"Results saved:")
        print(f"- All_URLs.txt: {len(self.all_urls)} URLs")
        print(f"- All_Unique_URLs.txt: {len(self.unique_urls)} URLs")


def main():
    """Main function to run the spider"""
    if len(sys.argv) != 2:
        print("Usage: python scrapy_url_extractor.py <URL>")
        print("Example: python scrapy_url_extractor.py example.com")
        print("Example: python scrapy_url_extractor.py https://example.com")
        sys.exit(1)
    
    target_url = sys.argv[1]
    
    # Configure Scrapy logging to reduce verbosity
    configure_logging({'LOG_LEVEL': 'INFO'})
    
    # Set up the crawler process
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'ROBOTSTXT_OBEY': True,  # Respect robots.txt
        'DOWNLOAD_DELAY': 1,  # Be respectful - 1 second delay between requests
        'CONCURRENT_REQUESTS': 16,  # Limit concurrent requests
        'CONCURRENT_REQUESTS_PER_DOMAIN': 8,
        'AUTOTHROTTLE_ENABLED': True,  # Enable auto-throttling
        'AUTOTHROTTLE_START_DELAY': 1,
        'AUTOTHROTTLE_MAX_DELAY': 3,
        'AUTOTHROTTLE_TARGET_CONCURRENCY': 2.0,
        'LOG_LEVEL': 'INFO',
    })
    
    print(f"Starting URL extraction for: {target_url}")
    print("This may take a while depending on the size of the website...")
    
    # Start the spider
    process.crawl(URLExtractorSpider, start_url=target_url)
    process.start()


if __name__ == "__main__":
    main()