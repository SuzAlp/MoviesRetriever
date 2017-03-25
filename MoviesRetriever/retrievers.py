import urllib.request
from urllib.error import URLError, HTTPError

class HtmlRetriever:
    def __init__(self,url, moviesLogger):
        self._url = url
        self._moviesLogger = moviesLogger

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, value):
        self._url = value

    def retrieve(self):
        try:
            response = urllib.request.urlopen(self._url)
        except HTTPError as e:
            self._moviesLogger.LogError(
                "Problem with response from url - {0},errorCode:{1}.Exception:{2}".format(self._url, e.code, e.reason))
            return None
        except URLError as e:
            self._moviesLogger.LogError("Problem with url - {0}.Exception:{1}".format(self._url,e.reason))
            return None
        except Exception as e:
            self._moviesLogger.LogError("There was a problem retrieving html from url - {0}.Exception:{1}".format(self._url, e))
            return None
        else:
            try:
                content = response.read()
                response.close()
                return content
            except Exception as e:
                self._moviesLogger.LogError(
                    "There was a problem reading the html from url - {0}.Exception:{1}".format(self._url, e))
                return None


