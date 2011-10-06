#!/usr/bin/env python

import sys
import urllib
import urlparse
from BeautifulSoup import BeautifulSoup
from collections import defaultdict
from operator import itemgetter


def get_businesses_from_search(term, location):

	search_url = "http://www.yelp.com/search?find_desc=%s&ns=1&find_loc=%s" % (
		urllib.quote(term), urllib.quote(location))

	conn = urllib.urlopen(search_url)
	contents = conn.read()

	soup = BeautifulSoup(contents)
	for result in soup("div", {"class": "businessresult clearfix"}):
		business_url = "http://www.yelp.com" + result.find("h4").find("a")["href"]
		business_name = result.find("h4").text

		yield {
			"business_name": business_name,
			"business_url": business_url
		}

def get_reviews_from_biz_page(url):

	conn = urllib.urlopen(url)
	contents = conn.read()

	soup = BeautifulSoup(contents)

	business_name = soup.find("h1").text
	business_url = soup.find(id="review_search_form")["action"]

	for review in soup("li", {"class": "hreview review clearfix  externalReview"}):

		user = review.find("li", {"class": "user-name"}).find("a")
		user_name = user.text
		user_url = user["href"]

		text = review.find("p", {"class": "review_comment description ieSucks"}).text
		rating = int(review.find("div", {"class": "rating"}).find("span", {"class": "value-title"})["title"])

		yield {
			"business_name": business_name,
			"business_url": business_url,
			"user_name": user_name,
			"user_url": user_url,
			"text": text,
			"rating": rating
		}

def get_reviews_from_user_page(url):

	conn = urllib.urlopen(url)
	contents = conn.read()

	soup = BeautifulSoup(contents)
	user_name = soup.find("title").text.split("&#39;s")[0]

	for review in soup("div", {"class": "review clearfix"}):

		business = review.find("h4").find("a")
		business_name = business.text
		business_url = urlparse.urlparse(business["href"]).path
		text = review.find("div", {"class": "review_comment"}).text
		rating = int(float(review.find("div", {"class": "rating"}).find("img")["title"].split()[0]))

		yield {
			"business_name": business_name,
			"business_url": business_url,
			"user_name": user_name,
			"text": text,
			"rating": rating
		}

if __name__ == "__main__":

	assert len(sys.argv) == 3, "Please enter a business and location to search for recommendations"

	businesses = list(get_businesses_from_search(sys.argv[1], sys.argv[2]))
	for business in businesses:
		print business["business_name"]

	business_num = int(raw_input("Enter a busines to view suggestions [1-10]: "))
	business = businesses[business_num-1]

	print "Getting suggestions for:", business["business_name"]


	suggestions = defaultdict(int)

	for review in get_reviews_from_biz_page(business["business_url"]):
		print review["rating"], review["user_name"]

		for subreview in get_reviews_from_user_page(review["user_url"]):

			if subreview["business_name"] != review["business_name"]:
				print "\t", subreview["business_name"], subreview["rating"]

				rating = review["rating"] * subreview["rating"]
				suggestions[subreview["business_name"]] += rating

		print

	print "Here are your suggestions for:", business["business_name"]
	sorted_suggestions = sorted(suggestions.iteritems(), key=itemgetter(1), reverse=True)
	for business, rating in sorted_suggestions:
		print rating, business

