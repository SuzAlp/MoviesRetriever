from MoviesRetriever.retrievers import HtmlRetriever
from MoviesRetriever import sqlLiteMoviesDb
from MoviesRetriever import neo4jMoviesDb
from MoviesRetriever.extractors import UrlsExtractor, MoviesExtractor
from MoviesRetriever.moviesLogger import MoviesLogger
from MoviesRetriever.moviesConfig import MoviesConfig
import concurrent.futures
import time


def start(movies_conf, movies_logger, db):
    base_url = movies_conf.configByKey("main", "base_url")
    html_ret = HtmlRetriever(base_url + movies_conf.configByKey("main", "chart_url"), movies_logger)
    html = html_ret.retrieve()
    if html is None:
        return False

    urls_extractor = UrlsExtractor(html, movies_conf.configByKey("main", "urls_extractor_pattern"),
                                   movies_logger)
    urls = urls_extractor.extract()
    if urls is None:
        return False
    movies = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=movies_conf.configByKey("main", "num_threads")) as executor:
        future_to_url = {executor.submit(processUrl, url, movies_conf, movies_logger): url for url in urls}
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            try:
                movie = future.result()
            except Exception as exc:
                movies_logger.LogError("Problem occured while processing -{0} .Exception: {1}".format(url, exc))
            else:
                movies.append(movie)

    for movie in movies:
        if movie is not None:
            db.insert(movie)
    db.select()
    return True


def processUrl(url, movies_conf, movies_logger):
    print("start")
    htmlRet = HtmlRetriever(movies_conf.configByKey("main", "base_url") + url, movies_logger)
    html = htmlRet.retrieve()
    movieExtractor = MoviesExtractor(html, movies_conf.configByKey("main", "movie_extractor_pattern"),
                                     movies_logger)
    movie = movieExtractor.extract()
    print("end")
    return movie


def main():
    movies_conf = MoviesConfig()
    movies_logger = MoviesLogger(movies_conf)
    # db = sqlLiteMoviesDb.SqlLiteMoviesDb(moviesConf,moviesLogger)
    db = neo4jMoviesDb.Neo4jMoviesDb(movies_conf, movies_logger)
    timeSleep = movies_conf.configByKey("main", "time_between_retrive")
    while True:
        success = start(movies_conf, movies_logger, db)
        if success is False:
            errorMsg = "Failed to retrieve movies and save to DB.Check the logs"
            movies_logger.LogError(errorMsg)
            print(errorMsg)
        else:
            infoMsg = "Movies Retrieved successfully"
            movies_logger.LogInfo(infoMsg)
            print(infoMsg)

        time.sleep(timeSleep)


if __name__ == '__main__':
    main()
