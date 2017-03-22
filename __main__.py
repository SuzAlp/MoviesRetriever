from MoviesRetriever import retrievers
from MoviesRetriever import sqlLiteMoviesDb
from MoviesRetriever import extractors
from MoviesRetriever.moviesLogger import  MoviesLogger
from MoviesRetriever.moviesConfig import MoviesConfig
import concurrent.futures
import time
import datetime
import json


def start(moviesConf,moviesLogger,db):
    baseUrl = moviesConf.configByKey("main", "base_url")
    htmlRet = retrievers.HtmlRetriever(baseUrl + moviesConf.configByKey("main","chart_url"), moviesLogger)
    html = htmlRet.retrieve()
    if html is None:
        return False

    urlsExtractor = extractors.UrlsExtractor(html, moviesConf.configByKey("main","urls_extractor_pattern"), moviesLogger)
    urls = urlsExtractor.extract()
    if urls is None:
        return False


    movies =[]
    with concurrent.futures.ThreadPoolExecutor(max_workers=moviesConf.configByKey("main","num_threads")) as executor:
        future_to_url = {executor.submit(processUrl, url, moviesConf, moviesLogger): url for url in urls}
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            try:
                movie = future.result()
            except Exception as exc:
                moviesLogger.LogError("Problem occured while processing -{0} .Exception: {1}".format (url, exc))
            else:
                movies.append(movie)

    for movie in movies:
        if movie is not None:
            db.insert(movie)
    db.select()
    return True

def processUrl(url,moviesConf,moviesLogger):
    print("start")
    htmlRet = retrievers.HtmlRetriever(moviesConf.configByKey("main", "base_url") + url, moviesLogger)
    html = htmlRet.retrieve()
    movieExtractor = extractors.MoviesExtractor(html, moviesConf.configByKey("main","movie_extractor_pattern"),
                                                moviesLogger)
    movie = movieExtractor.extract()
    print("end")
    return movie

def main():
    moviesConf = MoviesConfig()
    moviesLogger = MoviesLogger(moviesConf)
    db = sqlLiteMoviesDb.SqlLiteMoviesDb(moviesConf,moviesLogger)
    timeSleep = moviesConf.configByKey("main","time_between_retrive")
    while True:
        success = start(moviesConf, moviesLogger, db)
        if success is False:
            errorMsg = "Failed to retrieve movies and save to DB.Check the logs"
            moviesLogger.LogError(errorMsg)
            print (errorMsg)
        else:
            infoMsg = "Movies Retrieved successfully"
            moviesLogger.LogInfo(infoMsg)
            print(infoMsg)

        time.sleep(timeSleep)

if __name__ == '__main__':
    main()