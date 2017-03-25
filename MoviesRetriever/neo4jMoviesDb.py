from MoviesRetriever.moviesDb import MoviesDb
from py2neo import Graph, authenticate


class Neo4jMoviesDb(MoviesDb):
    def __init__(self, movies_config, movies_logger):
        self._movies_logger = movies_logger
        address = movies_config.configByKey("neo4j", "db_address")
        user = movies_config.configByKey("neo4j", "user")
        password = movies_config.configByKey("neo4j", "password")
        # set up authentication parameters
        try:
            authenticate(address, user, password)
            # connect to authenticated graph database
            self._graph = Graph("http://localhost:7474/db/data/")
        except Exception as e:
            self._movies_logger.LogError(
                "Problem occured while connecting to neo4j DB and initializing.Exception:{0}".format(e))
            raise e

    def insert(self, movie):
        if self.isExists(movie) is False:
            # creating node movie
            try:
                self._graph.run('CREATE(:Movie{{name: "{0}"}})'.format(movie.name))
            except Exception as e:
                self._movies_logger.LogError("Failed creating node Movie for -{0}.Exception:{1}".format(movie.name, e))
                return False
            # creating node Person for director
            try:
                self._graph.run('CREATE(:Person{{name: "{0}"}})'.format(movie.director))
            except Exception as e:
                self._movies_logger.LogError(
                    "Failed creating node Person for -{0}.Exception:{1}".format(movie.director, e))
                return False
            # creating relationship Person directed Movie
            try:
                self._graph.run('MATCH (director:Person),(movie:Movie) '
                                'WHERE director.name = "{0}" AND movie.name = "{1}" '
                                'CREATE (director)-[:directed]->(movie)'.format(movie.director, movie.name))
            except Exception as e:
                self._movies_logger.LogError(
                    "Failed creating relationship between director -{0} and Movie - {1}.Exception:{2}".format(
                        movie.director, movie.name, e))
                return False
            # creating node Person for each actor,and relationship Person acted in movie
            for actor in movie.actors:
                try:
                    self._graph.run('CREATE(:Person{{name: "{0}"}})'.format(actor))
                except Exception as e:
                    self._movies_logger.LogError(
                        "Failed creating node Person for -{0}.Exception:{1}".format(actor, e))
                    return False
                try:
                    self._graph.run('MATCH (actor:Person),(movie:Movie) '
                                    'WHERE actor.name = "{0}" AND movie.name = "{1}" '
                                    'CREATE (actor)-[:acted_in]->(movie)'.format(actor, movie.name))
                except Exception as e:
                    self._movies_logger.LogError(
                        "Failed creating relationship between actor -{0} and Movie - {1}.Exception:{2}".format(actor,
                                                                                                               movie.name,
                                                                                                               e))
                    return False
        return True

    def select(self):
        results = self._graph.run("MATCH (movie:Movie) RETURN movie.name").data()
        for result in results:
            print(result)

    def isExists(self, movie):
        results = self._graph.run('MATCH (m:Movie {{ name:"{0}" }})RETURN m'.format(movie.name)).data()
        if not results:
            return False
        return True
