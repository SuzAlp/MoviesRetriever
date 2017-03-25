import concurrent

from MoviesRetriever.extractors import UrlsExtractor, MoviesExtractor
from MoviesRetriever.retrievers import HtmlRetriever


class MoviesCrawler:
    def __init__(self, url, movies_config, movies_logger):
        self._url = url
        self._movies_config = movies_config
        self._movies_logger = movies_logger

    def processMovies(self):
        pass


class ImdbCrawler(MoviesCrawler):
    def processMovies(self):
        html_ret = HtmlRetriever(self._url + self._movies_config.configByKey("imdb", "chart_url"), self._movies_logger)
        html = html_ret.retrieve()
        if html is None:
            return None
        urls_extractor = UrlsExtractor(html, self._movies_config.configByKey("imdb", "urls_extractor_pattern"),
                                       self._movies_logger)

        urls = urls_extractor.extract()
        movies = []
        if urls is None:
            return None
        with concurrent.futures.ThreadPoolExecutor(
                max_workers=self._movies_config.configByKey("imdb", "num_threads")) as executor:
            future_to_url = {executor.submit(self.processUrl, url): url for url in urls}
            for future in concurrent.futures.as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    movie = future.result()
                except Exception as e:
                    self._movies_logger.LogError("Problem occured while processing -{0} .Exception: {1}".format(url, e))
                else:
                    if movie is not None:
                        movies.append(movie)
        return movies

    def processUrl(self, url):
        print("start")
        htmlRet = HtmlRetriever(self._url + url, self._movies_logger)
        html = htmlRet.retrieve()
        movieExtractor = MoviesExtractor(html, self._movies_config.configByKey("imdb", "movie_extractor_pattern"),
                                         self._movies_logger)
        movie = movieExtractor.extract()
        print("end")
        return movie
