import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from datetime import datetime
import re
import pandas as pd
import numpy as np
import itertools
from imdbUtils import *

pd.options.display.max_colwidth=500

file_counter = input("Please enter a file counter:")
filename = 'Movie_List_v7_' + file_counter + '.csv'



##movie_tags[:10]
#movie_list = pd.read_csv('Movie_List_v7.csv')
movie_list = pd.read_csv(filename)
print(movie_list.head())

for index, movie in movie_list.iterrows():
    movie_tags = []
    if movie["Status"] == "x" or movie["Status"] == "err":
    #if movie["Status"] != "try":
        continue

    movie_tags.append(movie["imdb_id"])
    userReview_filename = movie["imdb_id"] + '-userReviews.csv'
    movie_review_links_filename = movie["imdb_id"] + '-movie_review_links.csv'
    movie_ind_review_links_filename = movie["imdb_id"] + '-movie_ind_review_links.csv'


    # movie overall review links
    # Example: https://www.imdb.com/title/tt0385887/reviews
    base_url = "https://www.imdb.com/title/"
    movie_review_links = [base_url + tag + '/reviews' for tag in movie_tags]
    # print(movie_review_links)
    print("====================================")
    print(datetime.now(), "There are a total of " + str(len(movie_review_links)) + " movies in the list")
    # movie_overall_review_links.append("https://www.imdb.com/title/tt1392170/reviews/_ajax?paginationKey=g4wp7cjlr45tmzqk7cvx5nrvrpq4shjjtzpwzouokkd2gbzgpnt6ud25o4yvtnrob4drz6ws6s3kkz3sfc6xpgdffjtlc")
    # next we need to expand the movie_overall_review_links to LOAD MORE pages

    # An example of LOAD MORE page
    # https://www.imdb.com/title/tt1392170/reviews/_ajax?paginationKey=g4wp7cjlr45tmzqk7cvx5nrvrpq4shjjtzpwzouokkd2gbzgpnt6ud25o4yvtnrob4drz6ws6s3kkz3sfc6xpgdffjtlc

    print(datetime.now(), "Now working on the load more links")
    # for each movie overall reivew link,, get a list of soup objects
    movie_soups_init = [getSoup(link) for link in movie_review_links]

    # get movie reivew load more links for each overall review page. There are many load more links for each movie overall review page.
    movie_review_load_more_list = [getLoadMoreLink(movie_soup) for movie_soup in movie_soups_init]
    # print(movie_review_load_more_list, sep = "\n")
    movie_review_load_more_list2 = []

    i = 0

    if movie_review_load_more_list.count('NNAA'):
        movie_review_load_more_list.remove("NNAA")

    for link in movie_review_load_more_list:
        i = i + 1
        # print(link)
        if link == "NNAA":
            continue
        movie_soup2 = getSoup(link)
        movie_review_load_more2_data_key = getLoadMoreLink2_key(movie_soup2)
        if movie_review_load_more2_data_key == "":
            continue
        #load_more_link = baseurl + imdb_title_id + "/reviews/_ajax?paginationKey=" + ajax_data_key
        # https://www.imdb.com/title/tt0385887/reviews/_ajax?paginationKey=
        movie_review_load_more2_link = link[0:65] + movie_review_load_more2_data_key
        # movie_review_load_more_list2.append(movie_review_load_more2_link)
        movie_review_load_more_list.append(movie_review_load_more2_link)
        # if i == 50:
        #     break

    #movie_soups_load_init = [getSoup(link) for link in movie_review_load_more_list]

    #movie_review_load_more_list2 = [getLoadMoreLink2(movie_soup) for movie_soup in movie_soups_load_init]
    #print(movie_review_load_more_list)

    # movie_review_load_more_list = list(itertools.chain(*movie_review_load_more_list))
    # combine initial overall review list with load more review list

    movie_review_links.extend(movie_review_load_more_list)
    #movie_review_links.extend(movie_review_load_more_list2)


    print(datetime.now(), "All Movie Reivew Links, including Load More Links is ready for export")
    #print(*movie_review_links, sep = "\n")

    df_review_links = pd.DataFrame({'movie_review_link': movie_review_links})

    df_review_links.head()


    # save the dataframe to a csv file.
    df_review_links.to_csv(movie_review_links_filename, index=False)

    print(datetime.now(), "All Movie Reivew Links, including Load More Links export to CSV is complete")

    print(datetime.now(), "Now working on the individual review list")
    movie_soups = [getSoup(link) for link in movie_review_links]

    # get all movie review links for per each review and each movie
    movie_ind_review_list = [getReviews(movie_soup) for movie_soup in movie_soups]

    #print(movie_ind_review_list)

    movie_ind_review_list = list(itertools.chain(*movie_ind_review_list))


    print(datetime.now(), "There are total of " + str(len(movie_ind_review_list)) + " individual movie reviews")
    #print(*movie_ind_review_list, sep = "\n")


    print(datetime.now(), "All Individual Reivew Links are ready for export")

    df_ind_review_links = pd.DataFrame({'movie_ind_review_link': movie_ind_review_list})

    df_ind_review_links.head()



    # save the dataframe to a csv file.
    df_ind_review_links.to_csv(movie_ind_review_links_filename, index=False)

    print(datetime.now(), "All Individual Reivew Links export is complete")

    print(datetime.now(), "Now working on individual review extraction for each movie")
    df = pd.DataFrame(columns =['title_id', 'movie', 'user_review_permalink', 'user_review', 'user_review_date'])


    # df = pd.DataFrame({'title_id': movie_title_id, 'movie': movie_titles, 'user_review_permalink': movie_ind_review_list,
    #              'user_review': review_texts, 'user_review_date':review_date})

    for review_url in movie_ind_review_list:
        # get the review_url's soup
        soup = getSoup(review_url)

        movie_title_id = getMovieTitleID(soup)

        review_date = getReviewDate(soup)

        # get review text from the review link
        review_texts = getReviewText(soup)

        # get movie name from the review link
        movie_titles = getMovieTitle(soup)

        new_row = {'title_id': movie_title_id, 'movie': movie_titles, 'user_review_permalink': review_url, 'user_review': review_texts, 'user_review_date':review_date}
        #append row to the dataframe
        df = df.append(new_row, ignore_index=True)

    # df.head()

    print(datetime.now(), "Dataframe is ready, now start exporting individual reviews")

    # save the dataframe to a csv file.

    df.to_csv(userReview_filename, index=False)

    print(datetime.now(), "Individual review extraction is complete " + userReview_filename)

    # pickle the dataframe
    #df.to_pickle('userReviews.pkl')
