import unittest
from MoviesRetriever.extractors import UrlsExtractor, MoviesExtractor
from MoviesRetriever.moviesConfig import MoviesConfig
from MoviesRetriever.moviesLogger import MoviesLogger


class TestExtractors(unittest.TestCase):
    def test_urls_retriever_return_None(self):
        self._urls_extractor.content = "abc"
        result = self._urls_extractor.extract()
        self.assertIsNone(result)

    def test_movie_retriever_return_None(self):
        self._movies_extractor.content = "abc"
        result = self._movies_extractor.extract()
        self.assertIsNone(result)

    def get_movie_html(self, name, director, actors):
        return '<html><head></head><body><div class="pagecontent"><div class="title_wrapper">{0}</div>' \
               '<div class="credit_summary_item"><h4 class ="inline" > Director:</h4><span itemprop="director" itemtype="http://schema.org/Person" >' \
               '<a href = "/name/nm0001104?ref_=tt_ov_dr" itemprop="url">{1}</a></span></div>' \
               '<table class="cast_list"><tr class="odd"><td class="primary_photo" ><a href="/name/nm0000209/?ref_=tt_cl_i1" > ' \
               '<img height="44" width="32" alt="Tim Robbins" title="Tim Robbins" src="" /></a></td >' \
               '<td class="itemprop" itemprop="actor" itemtype="http://schema.org/Person" > ' \
               '<a href="/name/nm0000209/?ref_=tt_cl_t1" itemprop="url" > <span class="itemprop" itemprop="name" >{2}</span></a>' \
               '</td></tr><tr class="even" ><td class="primary_photo" > <a href="/name/nm0000151/?ref_=tt_cl_i2" >' \
               '<img height="44" width="32" alt="Morgan Freeman" title="Morgan Freeman" src=""/></a> ' \
               '</td><td class="itemprop" itemprop="actor" itemtype="http://schema.org/Person" >' \
               '<a href="/name/nm0000151/?ref_=tt_cl_t2" itemprop="url" ><span class="itemprop" itemprop="name" >{3}</span></a>' \
               '</td></tr><tr class="odd" ><td class="primary_photo" >' \
               '<a href="/name/nm0348409/?ref_=tt_cl_i3" > <img height="44" width="32" alt="Bob Gunton" title="Bob Gunton" src=""/></a>' \
               '</td><td class="itemprop" itemprop="actor" itemtype="http://schema.org/Person" >' \
               '<a href="/name/nm0348409/?ref_=tt_cl_t3" itemprop="url"><span class ="itemprop" itemprop="name">{4}</span></a>' \
               '</td></tr></table></div></body></html>'.format(name, director, actors[0], actors[1], actors[2])

    def test_movie_extractor_return_movie_with_all_fields(self):
        name = "The Shawshank Redemption"
        director = "Frank Darabont"
        actors = ["Tim Robbins", "Morgan Freeman", "Bob Gunton"]
        self._movies_extractor.content = self.get_movie_html(
            '<h1 itemprop="name" class="">The Shawshank Redemption<span id="titleYear">(<a href="/year/1994/?ref_=tt_ov_inf">1994</a>)</span></h1>',
                                                             '<span class="itemprop" itemprop="name">Frank Darabont</span>', actors)
        result = self._movies_extractor.extract()
        self.assertIsNotNone(result)
        self.assertEqual(result.name, name)
        self.assertEqual(result.director, director)
        self.assertEqual(len(result.actors), len(actors))
        for i in range(len(actors)):
            self.assertEqual(actors[i], result.actors[i])

    def test_movie_extractor_return_None_no_movie_name1(self):
        actors = ["Tim Robbins", "Morgan Freeman", "Bob Gunton"]
        self._movies_extractor.content = self.get_movie_html(
            '<h1 itemprop="blabla" class="">blabla<span id="titleYear">(<a href="/year/1994/?ref_=tt_ov_inf">1994</a>)</span></h1>',
                                                             '<span class="itemprop" itemprop="name">Frank Darabont</span>', actors)
        result = self._movies_extractor.extract()
        self.assertIsNone(result)

    def test_movie_extractor_return_None_no_director(self):
        actors = ["Tim Robbins", "Morgan Freeman", "Bob Gunton"]
        self._movies_extractor.content = self.get_movie_html(
            '<h1 itemprop="name" class="">The Shawshank Redemption<span id="titleYear">(<a href="/year/1994/?ref_=tt_ov_inf">1994</a>)</span></h1>',
            '<span class="itemprop" itemprop="bla">bla</span>', actors)
        result = self._movies_extractor.extract()
        self.assertIsNone(result)

    def test_movie_extractor_return_None_no_actors(self):
        pass

    def test_urls_extractor_return_list_of_one_url(self):
        self._urls_extractor.content = '<html><head></head><body><tbody class="lister-list"><tr>' \
                                       '<td class="ratingColumnimdbRating"><strong title="9.2basedon1,789,588userratings">9.2</strong></td>' \
                                       '<td class="titleColumn">1.<a href="/title/tt0111161/?pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=2398042102&pf_rd_r=16YQ2N1MJT56G7M80MPY&pf_rd_s=center-1&pf_rd_t=15506&pf_rd_i=top&ref_=chttp_tt_1" title="FrankDarabont(dir.),TimRobbins,MorganFreeman">TheShawshankRedemption</a><spanclass="secondaryInfo">(1994)</span></td>' \
                                       '</tr></tbody></body></html>'
        url = "/title/tt0111161/?pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=2398042102&pf_rd_r=16YQ2N1MJT56G7M80MPY&pf_rd_s=center-1&pf_rd_t=15506&pf_rd_i=top&ref_=chttp_tt_1"
        result = self._urls_extractor.extract()
        self.assertIsNotNone(result)
        self.assertEqual(result[0], url)

    def test_urls_extractor_return_list_of_urls(self):
        self._urls_extractor.content = '<html><head></head><body><tbody class="lister-list"><tr>' \
                                       '<td class="ratingColumnimdbRating"><strong title="9.2basedon1,789,588userratings">9.2</strong></td>' \
                                       '<td class="titleColumn">1.<a href="url1" title="abc">def</a><spanclass="secondaryInfo">(1994)</span></td></tr>' \
                                       '<tr><td class="ratingColumnimdbRating"><strong title="9.2basedon1,789,588userratings">9.2</strong></td>' \
                                       '<td class="titleColumn">1.<a href="url2" title="abc">def</a><spanclass="secondaryInfo">(1994)</span></td></tr>' \
                                       '<tr><td class="ratingColumnimdbRating"><strong title="9.2basedon1,789,588userratings">9.2</strong></td>' \
                                       '<td class="titleColumn">1.<a href="url3" title="abc">def</a><spanclass="secondaryInfo">(1994)</span></td></tr>' \
                                       '</tbody></body></html>'
        expectedUrls = ["url1", "url2", "url3"]
        results = self._urls_extractor.extract()
        self.assertIsNotNone(results)
        self.assertEqual(len(expectedUrls), len(results))
        for index in range(len(expectedUrls)):
            self.assertEqual(expectedUrls[index], results[index])

    def setUp(self):
        movies_config = MoviesConfig("config_test.json")
        movies_logger = MoviesLogger(movies_config)
        self._urls_extractor = UrlsExtractor("", movies_config.configByKey("imdb", "urls_extractor_pattern"),
                                             movies_logger)
        self._movies_extractor = MoviesExtractor("", movies_config.configByKey("imdb", "movie_extractor_pattern"),
                                                 movies_logger)
