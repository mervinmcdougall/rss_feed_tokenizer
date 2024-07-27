# RSS Feeed Tokenizer

## Summary
The RSS feed tokenizer is an NLP experiment. It allows for reading content from a site via its RSS feed and tokenizing the page content. Once tokenized it performs a frequency distribution to determine the gist of the content.

The application allows for reading multiple feeds. For example, you can retrieve data from an Economics feed and a Market feed. It will amalgamate the result of reading the two feeds, tokenize and will perform the frequency distribution. By consolidating the two feeds, it will attempt to find most frequently occurring words across the two or more feeds.

## Configuration
The code makes use of three main files for configuration:

- **regex_patterns.txt** - _Filters tokens using a regular expressions._
- **rss_sources.csv** - _Lists the RSS feeds the application will be reading from._
- **stopwords.txt** - _Filters stop words from the generated tokens._
- **corpus.txt** - _Caches the content read from the RSS feeds to reduce the load on the various endpoints._