import requests
import random
from time import sleep
from typing import List

from bs4 import BeautifulSoup

HEADERS = {
    'user - agent': 'Mozilla / 5.0(Windows NT 10.0; Win64; x6'
}


class IncorrectURLError(Exception):
    """
    Custom Error
    """


def create_bs_page(url: str) -> BeautifulSoup:
    # make request to the website
    response = requests.get(url, headers=HEADERS)

    # response encoding
    response.encoding = 'utf-8'

    if not response:
        raise IncorrectURLError(url)

    # create bs instance fot the further parsing
    return BeautifulSoup(response.content, features='html.parser')


class WebPageCrawler:
    def __init__(self, base_url, number_of_pages):
        self.base_url = base_url
        self.number_of_pages = number_of_pages

    def __extract_text_urls(self, page_url: str) -> List[str]:
        """
        Extracts text urls from a page url
        :param page_url: str
        :return: List of full urls
        """

        # get bs instance for the further parsing
        page_bs = create_bs_page(page_url)

        # extract links by tags
        links = page_bs.find_all('a', {'class': 'section-link'})

        # create full links for requests
        full_urls = [f"{self.base_url}{link.attrs['href']}" for link in links]
        return full_urls

    def __get_page_urls(self) -> List:
        """
        Creates a list of page links for later requests.
        :return: list
        """
        return [f'{self.base_url}?page={n}' for n in range(2, self.number_of_pages+1)]

    def get_articles_urls(self) -> List[str]:
        """
        Extracts articles urls from the base url
        :return: List od urls
        """
        page_urls = self.__get_page_urls()

        text_urls = []
        for i, page_url in enumerate(page_urls):
            if i % 5 == 0:
                print('=' * (i//5), '>', sep='')
            text_urls.extend(self.__extract_text_urls(page_url))

            # delay the next request
            sleep(random.randint(1, 3))

        return text_urls


class TextParser:
    @staticmethod
    def __parse_text_page(page_bs: BeautifulSoup) -> List[str]:
        page_content = page_bs.find('div', {'class': 'text'}).contents
        text = [tag.string for tag in page_content if tag.string is not None]
        return text

    def get_texts(self, text_urls: List[str]) -> List[List[str]]:
        """
        Extract textual content from the articles urls
        :param text_urls: list of pages with texts
        :return: List of the extracted contents
        """
        texts = []
        for i, text_url in enumerate(text_urls):
            if i % 10 == 0:
                print('=' * (i//10), '>', i, sep='')
            page_bs = create_bs_page(text_url)
            text = self.__parse_text_page(page_bs)
            texts.append(' '.join(text))
        return texts