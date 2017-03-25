import json


class MoviesConfig:
    def __init__(self,filename=None):
        if filename is None:
            json_data_file = open('MoviesRetriever\config.json')
        else:
            json_data_file = open(filename)
        self._configData = json.load(json_data_file)

    def configByKey(self, section, key):
        return self._configData[section][key]
