class Movie:
    def __init__(self,name,director,actors):
        self._name = name
        self._director = director
        self._actors = actors

    @property
    def name(self):
        return self._name

    @property
    def director(self):
        return self._director

    @property
    def actors(self):
        return self._actors