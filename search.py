#!/usr/bin/env python

import urllib
import urlparse
from BeautifulSoup import BeautifulSoup
from collections import defaultdict
from operator import itemgetter


def get_results_from_search(term, location):

	search_url = "http://www.yelp.com/search?find_desc=%s&ns=1&find_loc=%s" % (
		urllib.quote(term), urllib.quote(location))

	conn = urllib.urlopen(search_url)
	contents = conn.read()

	soup = BeautifulSoup(contents)
	for result in soup("div", {"class": "businessresult clearfix"}):
		url = result.find("h4").find("a")["href"]
		title = result.find("h4").text

		yield (title, url)

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
	
suggestions = defaultdict(int)

print "Mole Reviews"
for review in get_reviews_from_biz_page("http://www.yelp.com/biz/mole-new-york-3"):
	print review["rating"], review["user_name"]

	for subreview in get_reviews_from_user_page(review["user_url"]):

		if subreview["business_name"] != review["business_name"]:
			print "\t", subreview["business_name"], subreview["rating"]

			rating = review["rating"] * subreview["rating"]
			suggestions[subreview["business_name"]] += rating

	print

sorted_suggestions = sorted(suggestions.iteritems(), key=itemgetter(1))
for business, rating in sorted_suggestions:
	print rating, business