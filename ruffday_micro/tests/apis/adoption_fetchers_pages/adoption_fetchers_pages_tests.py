import unittest

from apis.adoption_fetchers_pages.adoption_fetchers_pages import HtmlAdoptionFetcher
from apis.adoption_fetchers_pages.adoption_fetchers_pages import TorontoHumaneSocietyFetcher


class HtmlAdoptionFetcherTest(unittest.TestCase):

    __TEST_HTML_DOC = """
    <html><head><title>The Dormouse's story</title></head>
    <body>
    <p class="title"><b>The Dormouse's story</b></p>

    <p class="story">Once upon a time there were three little sisters; and their names were
    <a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
    <a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
    <a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
    and they lived at the bottom of a well.</p>

    <p class="story">...</p>
    """

    def test_parsing_links(self):
        adoption_fetcher = HtmlAdoptionFetcher(self.__TEST_HTML_DOC)        
        self.assertIsNotNone(HtmlAdoptionFetcher(self.__TEST_HTML_DOC))

        actual_links = [link.get('href') for link in adoption_fetcher.find_all('a')]
        expected_links = [
            'http://example.com/elsie',
            'http://example.com/lacie',
            'http://example.com/tillie'
        ]
        self.assertListEqual(expected_links, actual_links)


class TorontoHumaneSocietyFetcherTest(unittest.TestCase):

    __TEST_HTML_FILENAME = 'tests\\apis\\adoption_fetchers_pages\\TorontoHumaneSocietyExample.html'

    def test_find_adoptions(self):
        with open(self.__TEST_HTML_FILENAME, encoding='utf8') as test_doc:
            text = test_doc.read()
            adoption_fetcher = TorontoHumaneSocietyFetcher(text)

if __name__ == '__main__':
    unittest.main()
