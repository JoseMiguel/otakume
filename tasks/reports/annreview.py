from bs4 import BeautifulSoup
import os
import pandas as pd
import numpy as np
from datetime import datetime
import logging
from collections import defaultdict
from  tasks.core.base import SiteTask, OrchestrateTask
import urllib2
from porc import Client

class ANNReviewOrchestrate(OrchestrateTask, SiteTask):

	@property
	def id(self):
		return 2

	def __init__(self):
		self.key = self.site['season'] + self.site['year']
	
		logging.basicConfig(filename=self.conf['logs']['crawler'],
						format='%(asctime)s - %(levelname)s:%(message)s', 
						level=logging.DEBUG,
						datefmt='%m/%d/%Y %I:%M:%S %p')

	def run(self):
		reviews = self.get().json['reviews']
		dfReviews = pd.DataFrame()
		for review in reviews:
			dfReviews = dfReviews.append(review,ignore_index=True)

		dirname = os.path.join(self.conf['output']['reports'], 'reviews', datetime.strftime(datetime.today(), '%Y-%m-%d') )
		os.makedirs(dirname)
		dfReviews.to_csv(os.path.join(dirname,'reviews.csv'))

def main():
#	pass
	print 'y'
	ann = ANNReviewOrchestrate()
	ann.run()

if __name__ == '__main__':
	main()
