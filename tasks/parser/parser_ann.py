from bs4 import BeautifulSoup
from collections import defaultdict
from  tasks.core.source import Source
import urllib2
import json

class SourceANN(Source):

	@property	
	def id(self):
		return 1

	def retrieve(self, leafXML, element):
		attrs = {}
		if element['property'] != None:
			attrs = {element['property'] : element['value']} 

		return leafXML.findAll(element['tag'], attrs=attrs)

	def parse(self, animeId):
		xml = urllib2.urlopen(self.site['api_url'] + animeId)
		result = defaultdict(list)
		soupXML = BeautifulSoup(xml)
		for feature, element in self.elements.iteritems():
			if element != None:
				leafXML = soupXML
				leafXML = self.retrieve(leafXML, element)
				for featureXML in leafXML:
					if 'inplace' in element:
						text = featureXML[element['inplace']]
					else:
						text = featureXML.text
					result[feature].append(text)

		return result

	def put(self, animeId):
		dictAnimeInfo = self.parse(animeId)
		dictAnimeInfo['source'] = self.source
		dictAnimeInfo['entity'] = animeId
		return json.dumps(dictAnimeInfo)

	def batch(self):
		for i in range(1,1000):
			print i
			with open('batch.txt','a') as output:
				output.write(self.put(str(i)))

sourceANN = SourceANN()
sourceANN.batch()
