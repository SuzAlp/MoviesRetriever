from bs4 import BeautifulSoup
from MoviesRetriever.movie import Movie


class HtmlExtractor:
    def __init__(self, content, filter_pattern, movies_logger):
        self._content = content
        self._filter_pattern = filter_pattern
        self._movies_logger = movies_logger

    def extract(self):
        html = BeautifulSoup(self._content, 'html.parser')
        return html.select(self._filter_pattern)

    @property
    def filter_pattern(self):
        return self._filter_pattern

    @filter_pattern.setter
    def filter_pattern(self, value):
        self._filter_pattern = value

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, value):
        self._content = value

class UrlsExtractor(HtmlExtractor):
    def extract(self):
        data = super().extract()
        if not data:
            self._movies_logger.LogError("Problem occured while trying to retrieve movie urls "
                                        " with filterPattern={0} from:\n {1}".format(self._filter_pattern,
                                                                                     self._content))
            return None
        urls = [a["href"] for a in data if a.has_attr('href')]
        if not urls:
            self._movies_logger.LogError("Problem occured while trying to get a[href] "
                                        " with filterPattern={0} from:\n {1}".format(self._filter_pattern,
                                                                                     self._content))
            return None
        return urls


class MoviesExtractor(HtmlExtractor):
    def extract(self):
        data = super().extract()
        if not data:
            self._movies_logger.LogError("Problem occured while trying to retrieve movie data"
                                        " with filterPattern={0} from:\n {1}".format(self._filter_pattern,
                                                                                     self._content))
            return None

        directorName = self.extractDirector(data[0])
        if directorName is None:
            return None

        movieName = self.extractName(data[0])
        if movieName is None:
            return None

        actors = self.extractActors(data[0])
        if actors is None:
            return None

        movie = Movie(movieName, directorName, actors)
        return movie

    def extractDirector(self, data):
        nodeType = "span"
        itemprop = "director"
        director = data.find(nodeType, {"itemprop": itemprop})
        if director is None:
            self._movies_logger.LogError("Problem occured while parsing director of movie. searching for {0} node"
                                        " with itemprop=director failed".format(nodeType))
            return None
        itemprop = "name"
        directorName = director.find("span", {"itemprop": itemprop})
        if directorName is None:
            self._movies_logger.LogError("Problem occured while parsing director of movie. searching for {0} node"
                                        " with itemprop={1} failed".format(nodeType, itemprop))
            return None
        return directorName.contents[0]

    def extractName(self, data):
        nodeType = "span"
        className = "title_wrapper"
        titleWrapper = data.find("div", {"class": className})
        if titleWrapper is None:
            self._movies_logger.LogError("Problem occured while parsing name of the movie. searching for {0} node"
                                        " with class={1} failed".format(nodeType, className))
            return None
        title = titleWrapper.find("div", {"class": "originalTitle"})
        if title is not None:
            return title.contents[0].strip()
        else:
            nodeType = "h1"
            h1 = titleWrapper.find(nodeType, {"itemprop": "name"})
            if h1 is None:
                self._movies_logger.LogError("Problem occured while parsing name of the movie. searching for {0} node"
                                             " with itemprop=name failed".format(nodeType))
                return None
            movieName = h1.contents[0]
            if movieName is None:
                self._movies_logger.LogError("Problem occured while parsing name of the movie. getting text from {0} node"
                                            " with itemprop=name failed".format(nodeType))
                return None
            return movieName.strip()

    def extractActors(self, data):
        nodeType = "table"
        className = "cast_list"
        castList = data.find(nodeType, {"class": className})
        if castList is None:
            self._movies_logger.LogError("Problem occured while parsing actors of the movie. searching for {0} node"
                                        " with class={1} failed".format(nodeType, className))
            return None
        actorsList = castList.find_all("td", {"itemprop": "actor"})
        actors = [actor.find("span", {"itemprop": "name"}).next for actor in actorsList]
        return actors
