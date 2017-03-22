import json
class MoviesConfig:
    def __init__(self):
        json_data_file = open('MoviesRetriever\config.json')
        self._configData = json.load(json_data_file)

    def configByKey(self,section,key):
        return self._configData[section][key]