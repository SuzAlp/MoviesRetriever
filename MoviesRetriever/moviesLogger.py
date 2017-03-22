import logging
import datetime
class MoviesLogger:

    def __init__(self,moviesConf):
        filename = moviesConf.configByKey("logger", "file_name")
        handler = logging.FileHandler(filename)
        self._logger = logging.getLogger(__name__)
        self._logger.addHandler(handler)

    def LogError(self,msg):
        self._logger.error("{0}:{1}".format(datetime.datetime.now(),msg))

    def LogInfo(self,msg):
        self._logger.info("{0}:{1}".format(datetime.datetime.now(),msg))