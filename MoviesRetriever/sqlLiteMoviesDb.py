from MoviesRetriever.moviesDb import MoviesDb
import sqlite3

class SqlLiteMoviesDb(MoviesDb):
    def __init__(self, moviesConf, moviesLogger):
        self._seqNum = 1
        self._connection = sqlite3.connect(':memory:')
        self._cursor = self._connection.cursor()
        self._cursor.execute('''CREATE TABLE IF NOT EXISTS movies(movie_id INT,movie_name TEXT, director TEXT)''')
        self._cursor.execute('''CREATE TABLE IF NOT EXISTS actors(movie_id INT,actor TEXT)''')
        self._moviesConf = moviesConf
        self._moviesLogger = moviesLogger

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
            moviesTable = self._moviesConf.configByKey("sqlite","table_movies")
            actorsTable = self._moviesConf.configByKey("sqlite", "table_actors")
            seqNum = self.getSequence()
            try:
                self._cursor.execute("INSERT INTO movies (movie_id,movie_name,director) VALUES (?,?,?)",(seqNum, movie.name, movie.director))
            except Exception as e:
                self._moviesLogger.LogError("Failed inserting the movie - {0} into movies table.Exception:{1}".format(movie.name,e))
            try:
                for actor in movie.actors:
                    self._cursor.execute("INSERT INTO actors (movie_id,actor) VALUES(?,?)",(seqNum,actor))
            except Exception as e:
                self._moviesLogger.LogError("Failed inserting the movie - {0} into actors table.Exception:{1}".format(movie.name, e))


    def select(self):
        self._cursor.execute("SELECT * FROM movies")
        rows = self._cursor.fetchall()
        for row in rows:
            print (row)

