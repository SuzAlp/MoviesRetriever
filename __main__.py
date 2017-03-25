from MoviesRetriever.crawlers import ImdbCrawler
from MoviesRetriever.sqlLiteMoviesDb import SqlLiteMoviesDb
from MoviesRetriever.neo4jMoviesDb import Neo4jMoviesDb
from MoviesRetriever.moviesLogger import MoviesLogger
from MoviesRetriever.moviesConfig import MoviesConfig

import time


def main():
    try:
        movies_conf = MoviesConfig()
        movies_logger = MoviesLogger(movies_conf)
        timeSleep = movies_conf.configByKey("main", "time_between_retrive")
        #db = SqlLiteMoviesDb(movies_conf,movies_logger)
        db = Neo4jMoviesDb(movies_conf, movies_logger)
        imdb_crawler = ImdbCrawler(movies_conf.configByKey("imdb", "base_url"), movies_conf, movies_logger)
    except Exception as e:
        print("Failed to initialize component.Exception:{0}".format(e))
        return
    else:
        while True:
            movies = imdb_crawler.processMovies()
            # None or empty list of movies
            if not movies:
                errorMsg = "Failed to retrieve movies.Check the logs"
                movies_logger.LogError(errorMsg)
                print(errorMsg)
            else:
                success_counter = 0
                for movie in movies:
                    success = db.insert(movie)
                    if success:
                        success_counter += 1
                if success_counter < len(movies):
                    errorMsg = "Failed to insert movies to Db.Check the logs"
                    movies_logger.LogInfo(errorMsg)
                    print(errorMsg)
                else:
                    infoMsg = "Successfully inserted all the movies to DB"
                    movies_logger.LogInfo(infoMsg)
                    print(infoMsg)

            time.sleep(timeSleep)


if __name__ == '__main__':
    main()
