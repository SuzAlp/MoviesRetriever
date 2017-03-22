import urllib.request
from urllib.error import URLError, HTTPError

class HtmlRetriever:
    def __init__(self,url, moviesLogger):
        self._url = url
        self._moviesLogger = moviesLogger

    def retrieve(self):
        try:
            response = urllib.request.urlopen(self._url)
            content = response.read()
        except HTTPError as e:
            self._moviesLogger.LogError(
                "Problem with response from url - {0},errorCode:{1}.Exception:{2}".format(self._url, e.code, e.reason))
        except URLError as e:
            self._moviesLogger.LogError("Problem with url - {0}.Exception:{1}".format(self._url,e.reason))
        except Exception as e:
            self._moviesLogger.LogError("There was a problem retrieving html from url - {0}.Exception:{1}".format(self._url, e))
        finally:
            try:
                response.close()
            except NameError:
                return None
        return content

