import unittest
from  MoviesRetriever import retrievers
class TestWebRetriever(unittest.TestCase):

    def test_a(self):
        result = self._retriever.retrieve()
        self.assertIsNotNone(result)

    def setUp(self):
        self._retriever = retrievers.HtmlRetriever("http://www.imdb.com/chart/top/?ref_=nv_mv_250_6")

    if __name__ == '__main__':
        unittest.main()