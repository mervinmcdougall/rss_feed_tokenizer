import csv
import feedparser as fp
import requests
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.probability import FreqDist
from os.path import exists as file_exists
from lxml import etree
from bs4 import BeautifulSoup
from urllib.request import urlopen

def read_rss_feeds(rss_feeds_path):
    """
    Reads the RSS feeds from the csv file
    :param rss_feeds_path: 
    :return: 
    """
    rss_feeds = csv.DictReader(open(rss_feeds_path, 'r'))
    return rss_feeds


def get_rss_feeds(rss_feeds):
    """
    Returns the RSS feeds
    :param rss_feeds:
    :return:
    """""
    feeds = {}
    for rss in rss_feeds:
        path = rss['Feed']
        data = fp.parse(path)
        feeds[rss['Name']] = data

    return feeds


def process_entries(feeds):
    """
    Processes the RSS feeds
    :param feeds:
    :return:
    """
    corpus = {}
    for name, feed in feeds.items():
        print("Processing feed: ", name)
        corpus[name] = []
        for items in feed['entries']:
            # html = requests.get(items['link']).text
            html = urlopen(items['link']).read()
            soup = BeautifulSoup(html, 'html.parser')
            data  = soup.get_text()
            # data = items['summary']
            # data = remove_html_tags(html)
            corpus[name].append(data)


    return corpus


def save_to_file(corpus):
    """
    Saves the corpus to a file
    :param corpus:
    :return:
    """
    with open('data/corpus.txt', 'w', encoding='utf-8') as f:
        for name, entries in corpus.items():
            stub = name.replace(' ', '_')
            f.write('data/'+stub + '\n')
            for entry in entries:
                # print(entry)
                f.write(entry + '\n')



def remove_html_tags(text):
    """
    Removes the html tags from the text
    :param text:
    :return:
    """
    parser = etree.HTMLParser()
    tree = etree.fromstring(text, parser)
    return etree.tostring(tree, encoding='unicode', method='text')


def tokenize_corpus(corpus_path):
    """
    Tokenizes the corpus
    :param corpus_path:
    :return:
    """
    sentences = []
    tokens = []

    with open(corpus_path, 'r', encoding='utf-8') as f:
        for line in f:
            sentences.append(line.strip())

    for s in sentences:
        for word in word_tokenize(s):
            tokens.append(word.lower())

    return tokens

def filter_stopwords(tokens):
    """
    Filters the stopwords from the tokens
    :param tokens:
    :return:
    """
    stopWords = set(stopwords.words('english'))
    filtered_tokens = [w for w in tokens if not w in stopWords]

    # filter using custom stopwords
    with open('config/stopwords.txt', 'r') as f:
        custom_stopwords = f.read().splitlines()
        filtered_tokens = [w for w in filtered_tokens if not w in custom_stopwords]

    return filtered_tokens


def filter_regex_patterns(tokens):
    """
    Filters the tokens using regex patterns
    :param tokens:
    :return:
    """
    with open('config/regex_patterns.txt', 'r') as f:
        patterns = f.read().splitlines()
        filtered_tokens = []
        for token in tokens:
            # if not any(re.match(pattern, token) for re in map(re.compile, patterns)):
            #     filtered_tokens.append(token)
            found = 0
            for pattern in patterns:
                if re.search(pattern, token):
                    found =1
                    break
            if not found:
                filtered_tokens.append(token)
    return filtered_tokens


def generate_frequency(tokens, limit=10):
    """
    Generates the frequency distribution of the tokens
    :param tokens:
    :return:
    """
    fdist = FreqDist(tokens)
    return fdist.most_common(limit)

def main():
    corpus_path = 'data/corpus.txt'
    if not file_exists(corpus_path):

        print("Processing rss feeds")
        rss_feeds_path = "config/rss_sources.csv"

        # Read the RSS feeds from the csv file
        rss_feeds = read_rss_feeds(rss_feeds_path)

        # Get the RSS feeds
        feeds = get_rss_feeds(rss_feeds)

        # Process the RSS feeds
        corpus = process_entries(feeds)

        # Save to file
        save_to_file(corpus)

    print('Tokenizing the corpus')
    # Tokenize the corpus
    tokens = tokenize_corpus(corpus_path)
    print(f'Generated {len(tokens)} tokens')

    filtered_tokens =  filter_stopwords(tokens)
    print(f'Filtered {len(filtered_tokens)} tokens')

    filtered_tokens = filter_regex_patterns(filtered_tokens)
    print(f'Filtered {len(filtered_tokens)} tokens')
    # print(filtered_tokens)

    # Perform a frequency distribution
    frequency = generate_frequency(filtered_tokens, limit=100)
    print(frequency)

if __name__ == '__main__':
    main()
