import pickle

import pandas as pd

from .parsers import WebPageCrawler, TextParser

if __name__ == '__main__':
    base_url = 'https://saharina.ru/metod/ege/text/'
    output_path = 'essays.csv'
    number_of_pages = 48

    crawler = WebPageCrawler(base_url, number_of_pages)
    parser = TextParser()

    text_urls = crawler.get_articles_urls()

    with open('text_urls.pkl', 'wb') as f:
        pickle.dump(text_urls, f)

    # with open('text_urls.pkl', 'rb') as f:
    #     text_urls = pickle.load(f)

    texts = pd.Series(parser.get_texts(text_urls))

    texts.to_csv(output_path)
