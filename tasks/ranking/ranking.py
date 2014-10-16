from bs4 import BeautifulSoup
import logging
from collections import defaultdict
from  tasks.core.base import SiteTask, OrchestrateTask
import urllib2
from porc import Client
import operator

class AnimeInfoTask(OrchestrateTask, SiteTask):
	@property	
	def id(self):
		return 1

	def getFeatures(self):
		return self.site['features']

	def run(self, title):
		if not isinstance(title, str):
			str(title)
		return self.search('title', title);


class RankingTask(OrchestrateTask, SiteTask):
	@property	
	def id(self):
		self. animeInfo = AnimeInfoTask()
		self.features = self.animeInfo.getFeatures()
		self.histogram = {}
		for feat in self.features:
			self.histogram[feat] = dict()
		return 2

	def updateHistogram(self, info, review):
		hist = self.histogram
		for feat in self.features:
			if info.has_key(feat):
				values = info[feat]
				if isinstance(values, str):
					hist[feat][values] = hist[feat].get(values, 0) + review['mean']
				elif isinstance(values, list):
					for value in values:
						hist[feat][value] = hist[feat].get(value, 0) + review['mean']

	def run(self):
		self.key = 'fall2014'
		reviews = self.get().json['reviews']
		for review in reviews:
			info = self.animeInfo.run(review['item']).all()
			if len(info) == 1:
				info = info[0]
				self.updateHistogram(info['value'], review)
		for feat in self.features:
			sorted_x = sorted(self.histogram[feat].items(), key=operator.itemgetter(1), reverse=True)
			self.histogram[feat] = sorted_x
	
	def __repr__(self):
		result = ""
		for feat in self.features:
			result += feat + ":\n"
			for val, score in self.histogram[feat]:
				result += repr(val) +" : "+ repr(score)+"\n"
		return result

def main():
	task = RankingTask()
	task.run()
	print task


if __name__ == '__main__':
	main()
