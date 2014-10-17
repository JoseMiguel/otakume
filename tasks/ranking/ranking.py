from bs4 import BeautifulSoup
import logging
from collections import defaultdict
from  tasks.core.base import SiteTask, OrchestrateTask
import urllib2
from porc import Client
import operator, json, re

MAX = 10

class AnimeInfoTaskReal(OrchestrateTask, SiteTask):
	@property	
	def id(self):
		return 1

	def getFeatures(self):
		return self.site['cathegorical']

	def runDebug(self):
		pages = self.list()
		#page = pages.next()
		for page in pages:
			for item in page['results']:
				val = json.dumps(item['value'])
				if val != "{}":
					print item['path']['key'], ":", val

class Collections(OrchestrateTask, SiteTask):#file	
	@property	
	def id(self):
		return 1

	def __init__(self):
		self.animes = self.getCollection("allAnime.txt")
		self.ratings = self.getCollection("allRatings.txt")

	def getFeatures(self):
		return self.site['cathegorical']

	def getCollection(self, fileName):
		with open(fileName, 'r') as input:
			lines = input.read().split('\n')
		results = {}
		for line in lines:
			ptr = line.find(":")
			key, val = line[:ptr-1], line[ptr+2:]
			if val == "{}" or val == "":
				continue
			results[key] = json.loads(val)
		return results

		
class RankingTask(OrchestrateTask, SiteTask):
	def __init__(self):
		self.collections = Collections()
		self.features = self.collections.getFeatures()
		self.numVotes = 0
		#self.animeInfo = AnimeInfoTask()
		#self.features = self.animeInfo.getFeatures()
		self.histogram = {}
		for feat in self.features:
			self.histogram[feat] = dict()
	
	@property	
	def id(self):
		return 3

	def getLastRating(self, data):
		ratings = data['rating']
		last = {}
		lastTime = 0
		for rating in ratings:
			time = int(rating['timestamp'])
			if time > lastTime:
				last = rating
				lastTime = time
		return last

	def getNumVotes(self):
		ratings = self.collections.ratings
		total = 0
		for key in ratings.keys():
			total += self.getLastRating(ratings[key])['votes']
		return total

	def updateHistogram(self, info, review):
		hist = self.histogram
		for feat in self.features:
			if info.has_key(feat):
				values = info[feat]
				if isinstance(values, str):
					values = [values]
				for value in values:
					hist[feat][value] = hist[feat].get(value, 0) + \
					float(review['score']) * \
					int(review['votes']) / self.numVotes

	def run(self):
		ratings = self.collections.ratings
		animes = self.collections.animes
		self.numVotes = self.getNumVotes()
		for key in ratings.keys():
			if animes.has_key(key):
				self.updateHistogram(animes[key], \
				self.getLastRating(ratings[key]))
		for feat in self.features:
			sorted_x = sorted(self.histogram[feat].items(), \
			key=operator.itemgetter(1), reverse=True)
			maxVal = sorted_x[0][1] if len(sorted_x) > 0 else 1
			sorted_x = map(lambda x: (x[0],x[1]/maxVal * MAX), \
			sorted_x)
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
