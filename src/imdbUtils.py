##############################
#  Module: imdbUtils.py
##############################

import requests
from bs4 import BeautifulSoup

def getSoup(url):
    """
    Utility function which takes a url and returns a Soup object.
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    return soup

def minMax(a):
    '''Returns the index of negative and positive review.'''

    # get the index of least rated user review
    minpos = a.index(min(a))

    # get the index of highest rated user review
    maxpos = a.index(max(a))

    return minpos, maxpos

def getReviews(soup):
    '''Function returns all individual review links on a page'''

    # get a list of user ratings
    user_review_ratings = [tag.previous_element for tag in
                           soup.find_all('span', attrs={'class': 'point-scale'})]

    #print("There are a total of " + str(len(user_review_ratings)) + " movie user ratings")


    # find the index of negative and positive review
    # n_index, p_index = minMax(list(map(int, user_review_ratings)))

    user_review_list = []
    # get the review tags
    user_review_list_temp = soup.find_all('a', attrs={'class':'title'})

    for user_review_temp in user_review_list_temp:
        user_review = "https://www.imdb.com/" + user_review_temp.get('href')
        user_review_list.append(user_review)

    # print(user_review_list)
    # # get the negative and positive review tags
    # n_review_tag = user_review_list[n_index]
    # p_review_tag = user_review_list[p_index]
    #
    # # return the negative and positive review link
    # n_review_link = "https://www.imdb.com" + n_review_tag['href']
    # p_review_link = "https://www.imdb.com" + p_review_tag['href']

    # return n_review_link, p_review_link
    return user_review_list

def getLoadMoreLink (soup):

#   one example of the load more link
#   https://www.imdb.com/title/tt1392170/reviews/_ajax?paginationKey=g4wp7cjlr45tmzqk7cvx5nrvrpq4shjjtzpwzouokkd2gbzgpnt6ud25o4yvtnrob4drz6ws6s3kkz3sfc6xpgdffjtlc
#   this is part of data-key
    temp_string = ""
    temp_string = str(soup.select(".load-more-data")[0])

    if temp_string.find("data-key") != -1:
        ajax_data_key = soup.select(".load-more-data")[0]['data-key']
        ajax_data_url = soup.select(".load-more-data")[0]['data-ajaxurl']
        # baseurl = "https://www.imdb.com/title/"
        # load_more_link = baseurl + imdb_title_id + "/reviews/_ajax?paginationKey=" + ajax_data_key
        baseurl = "https://www.imdb.com"
        load_more_link = baseurl + ajax_data_url + "?paginationKey=" + ajax_data_key
        return load_more_link
    else:
        return "NNAA"


def getLoadMoreLink2_key (soup):

#   one example of the load more link
#   https://www.imdb.com/title/tt1392170/reviews/_ajax?paginationKey=g4wp7cjlr45tmzqk7cvx5nrvrpq4shjjtzpwzouokkd2gbzgpnt6ud25o4yvtnrob4drz6ws6s3kkz3sfc6xpgdffjtlc
#   this is part of data-key
    #print(soup.find('div', attrs={'class':'load-more-data'}))
    ajax_data_key = ""
    if len(soup.find_all('div', attrs={'class':'load-more-data'})) != 0:
        ajax_data_key = soup.select(".load-more-data")[0]['data-key']
    #ajax_data_url = soup.select(".load-more-data")[0]['data-ajaxurl']
    # baseurl = "https://www.imdb.com/title/"
    # load_more_link = baseurl + imdb_title_id + "/reviews/_ajax?paginationKey=" + ajax_data_key
    #baseurl = "https://www.imdb.com"
    #load_more_link = baseurl + ajax_data_url + "?paginationKey=" + ajax_data_key
    return ajax_data_key

def getReviewDate(soup):
    '''Returns the user review date given the review url.'''

    review_date = ""

    # find div tags with class display-name-date
    #tag = soup.find('div', attrs={'class': 'display-name-date'})
    tag = soup.find('span', attrs={'review-date'})
    if len(tag) != 0:
        review_date = tag.getText()
    return review_date
    #return tag.getText()

def getReviewText(soup):
    '''Returns the user review text given the review url.'''

    # find div tags with class text show-more__control
    tag = soup.find('div', attrs={'class': 'text show-more__control'})

    return tag.getText()

def getMovieTitle(soup):
    '''Returns the movie title from the review url.'''

    movie_title = ""
    # find h1 tag
    tag = soup.find('h1')

    if len(tag) >= 2:
        movie_title = list(tag.children)[1].getText()

    return movie_title

    #return list(tag.children)[1].getText()

def getMovieTitleID(soup):
    '''Returns the movie title from the review url.'''

    # find h1 tag
    movie_title_id = ""
    tag = soup.find('h1')

    if len(tag) >= 2:
        movie_title_id = list(tag.children)[1].get('href')[7:16]

    # return list(tag.children)[1].get('href')[8:16]
    return movie_title_id
