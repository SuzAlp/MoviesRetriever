import unittest

from MoviesRetriever import retrievers
from MoviesRetriever.moviesConfig import MoviesConfig
from MoviesRetriever.moviesLogger import MoviesLogger


class TestRetrievers(unittest.TestCase):
    def test_retriever_return_data(self):
        result = self._retriever.retrieve()
        self.assertIsNotNone(result)

    def test_retriever_return_None(self):
        self._retriever.url = "http://www.imdb.com/abcd"
        self.assertIsNone(self._retriever.retrieve())

    def setUp(self):
        movies_config = MoviesConfig("config_test.json")
        movies_logger = MoviesLogger(movies_config)
        self._retriever = retrievers.HtmlRetriever("http://www.imdb.com/chart/top/", movies_logger)
