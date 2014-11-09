from bs4 import BeautifulSoup
import numpy as np
import logging
from collections import defaultdict
from  tasks.core.base import SiteTask, OrchestrateTask
import urllib2
from porc import Client

class ANNReviewOrchestrate(OrchestrateTask):

	@property
	def id(self):
		return 2

	def __init__(self):
	
		logging.basicConfig(filename=self.conf['logs']['crawler'],
						format='%(asctime)s - %(levelname)s:%(message)s', 
						level=logging.DEBUG,
						datefmt='%m/%d/%Y %I:%M:%S %p')

	def run(self):
		task = ANNReviewTask()
		self.key = task.key

		reviews = self.get()
		updateReviews = task.run()
		# since there are about 20 reviews per season
		for i, updateReview in enumerate(updateReviews['reviews']):
			print updateReview
			for review in reviews['reviews']:
				if review['title'] == updateReview['title']:
					updateReviews['reviews'][i]['id'] = review['id']
					break
			
		self.json = updateReviews
		self.put()


class ANNReviewTask(SiteTask):

	def __init__(self):
		self.key = self.site['season'] + self.site['year']

	@property	
	def id(self):
		return 2

	def request_url(self):
		return self.site['api_url']
		

	def retrieve(self, leafXML, element):
		attrs = {}
		if element['property'] != None:
			attrs = {element['property'] : element['value']} 

		return leafXML.findAll(element['tag'], attrs=attrs)

	def prepare_url(self,url):
		try:
			xml = urllib2.urlopen(url, timeout=30)
		except Exception as e:
			logging.warning('Failed info in % with key %d, raise: ', self.source, self.key, e.message)
			return None

		return xml
		

	def run(self):
		url = self.request_url()
		xml = self.prepare_url(url)
		return self.crawl(xml, self.elements)

	def crawl(self, xml, elements):
		result = defaultdict(list)
		print 'x'
		if xml != None:
			logging.info('Getting anime info from %s with key %s', self.source, self.key)
			soupXML = BeautifulSoup(xml)
			soupTable = self.retrieve(soupXML, self.elements['table'])[0]
		
			for animeSoup in self.retrieve(soupTable, self.elements['animes']):
				ratings = []
				reviewDict = {}
				elementReview = self.elements['review_url']
				reviewUrlSoup = self.retrieve(animeSoup, elementReview)[0]
				name = self.retrieve(animeSoup, self.elements['name'])[0].text
				suffix_url = reviewUrlSoup[elementReview['inplace']]

				separator = ('/' if suffix_url[0] != '/' else '')
				review_url = self.site['base_url'] + separator + suffix_url
				xml_review = self.prepare_url(review_url)
				# in order to crawl reviews for each anime
				# this might change, it's pure adhoc
				reviewSiteSoup = BeautifulSoup(xml_review)
				reviews = self.retrieve(reviewSiteSoup, self.elements['rating'])

				length = self.elements['rating']['length']
				for review in reviews:
					reviewDescription = review.text[:length]
					pos = reviewDescription.rfind(self.elements['rating']['content'])
					text = reviewDescription[pos:length]
					rating_value = -1
					try:
						rating_value = float(text.split()[1])
					except:
						pass

					if rating_value > 0:
						ratings.append(rating_value)

				reviewDict['title'] = str(name.replace('\n', ' '))
				reviewDict['mean'] = np.mean(ratings)
				reviewDict['st-dev'] = 2 * np.std(ratings)
				result['reviews'].append(reviewDict)
				
			result['season'] = self.site['season']
			result['year'] = self.site['year']
		
		return result
	
def main():
#	pass
	print 'y'
	ann = ANNReviewOrchestrate()
	ann.run()

if __name__ == '__main__':
	main()
