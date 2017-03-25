from MoviesRetriever.moviesDb import MoviesDb
import sqlite3

class SqlLiteMoviesDb(MoviesDb):
    def __init__(self, movies_conf, movies_logger):
        self._seqNum = 1
        self._movies_conf = movies_conf
        self._movies_logger = movies_logger
        try:
            self._connection = sqlite3.connect(':memory:')
            self._cursor = self._connection.cursor()
            self._cursor.execute('''CREATE TABLE IF NOT EXISTS movies(movie_id INT,movie_name TEXT, director TEXT)''')
            self._cursor.execute('''CREATE TABLE IF NOT EXISTS actors(movie_id INT,actor TEXT)''')
        except Exception as e:
            self._movies_logger.LogError("Problem occured while connecting to sqlite DB and initializing.Exception:{0}".format(e))

    def getSequence(self):
        current = self._seqNum
        self._seqNum+=1
        return current

    def isExists(self, name):
        self._cursor.execute("SELECT * FROM movies where movie_name=?",(name,))
        rows = self._cursor.fetchall()
        if not rows :
            return False
        return True

    def insert(self,movie):
        if self.isExists(movie.name) is False:
            moviesTable = self._movies_conf.configByKey("sqlite", "table_movies")
            actorsTable = self._movies_conf.configByKey("sqlite", "table_actors")
            seqNum = self.getSequence()
            try:
                self._cursor.execute("INSERT INTO movies (movie_id,movie_name,director) VALUES (?,?,?)",(seqNum, movie.name, movie.director))
            except Exception as e:
                self._movies_logger.LogError("Failed inserting the movie - {0} into movies table.Exception:{1}".format(movie.name, e))
                return False
            try:
                for actor in movie.actors:
                    self._cursor.execute("INSERT INTO actors (movie_id,actor) VALUES(?,?)",(seqNum,actor))
            except Exception as e:
                self._movies_logger.LogError("Failed inserting the movie - {0} into actors table.Exception:{1}".format(movie.name, e))
                return False
        return True


    def select(self):
        self._cursor.execute("SELECT * FROM movies")
        rows = self._cursor.fetchall()
        for row in rows:
            print (row)

