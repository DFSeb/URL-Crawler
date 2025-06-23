# URL Extractor

## Overview
This Python script uses the Scrapy framework to crawl a website and extract all URLs found within the same domain. It generates two output files containing all discovered URLs, with options for both complete and deduplicated lists.

## Requirements
- Python 3.6 or higher
- Scrapy framework

## Installation
Before running the script, install the required dependency:

```
pip install scrapy
```

## Usage
Run the script from the command line with a target URL:

```
python scrapy_url_extractor.py <URL>
```

### Examples:
```
python scrapy_url_extractor.py example.com
python scrapy_url_extractor.py https://example.com
python scrapy_url_extractor.py www.example.com
```

Note: The script automatically adds "https://" if no protocol is specified, so you can use any of the above formats.

## Output Files
The script generates two text files:

1. **All_URLs.txt**
   - Contains every URL discovered during the crawl
   - Includes duplicate URLs if found on multiple pages
   - One URL per line

2. **All_Unique_URLs.txt**
   - Contains only unique URLs (duplicates removed)
   - Maintains the order of first discovery
   - One URL per line

## Features
- **Automatic URL Normalization**: Handles missing protocols (http/https)
- **Domain Restriction**: Only crawls URLs within the same domain as the starting URL
- **Respectful Crawling**: 
  - Respects robots.txt files
  - Implements delays between requests
  - Uses reasonable concurrency limits
- **Comprehensive Coverage**: Follows all internal links to discover hidden pages
- **Progress Monitoring**: Displays crawl progress and final statistics

## Script Behavior
- The crawler starts from your specified URL
- It extracts all links from each page
- Only follows links that belong to the same domain
- Continues crawling until all discoverable pages are processed
- Saves results to the two output text files

## Configuration Options
The script includes several built-in settings for responsible crawling:
- 1-second delay between requests
- Auto-throttling enabled
- Maximum 16 concurrent requests
- Respects robots.txt directives

## Troubleshooting

### Common Issues:
1. **"No module named 'scrapy'"**
   - Solution: Install Scrapy using `pip install scrapy`

2. **Permission denied when writing files**
   - Solution: Ensure you have write permissions in the current directory

3. **SSL certificate errors**
   - The script uses HTTPS by default; some sites may have certificate issues
   - Try using the HTTP version of the URL if available

4. **Long execution times**
   - Large websites can take considerable time to crawl completely
   - The script shows progress updates in the console

### Expected Output:
```
Starting URL extraction for: https://example.com
This may take a while depending on the size of the website...
[Scrapy log messages...]
Results saved:
- All_URLs.txt: 1250 URLs
- All_Unique_URLs.txt: 1050 URLs
```

## Limitations
- Only crawls pages within the same domain as the starting URL
- Requires JavaScript-free navigation (static HTML links)
- Respects robots.txt, which may limit crawling on some sites
- Does not extract URLs from JavaScript-generated content

## Best Practices
- Test on smaller websites first to understand crawl times
- Be respectful of target websites - don't overwhelm servers
- Check robots.txt files manually if you encounter access issues
- Consider the website's terms of service before crawling

## Technical Details
- Built with Scrapy 2.x framework
- Uses Python's urllib.parse for URL handling
- Implements OrderedDict for efficient duplicate removal
- Includes comprehensive error handling and logging

## Support
This script is designed for educational and legitimate research purposes. Ensure you have permission to crawl target websites and comply with their terms of service and robots.txt directives.
