from bs4 import BeautifulSoup
import logging
from collections import defaultdict
from  tasks.core.base import SiteTask, OrchestrateTask
import urllib2
from porc import Client

class ANNOrchestrate(OrchestrateTask):

	@property
	def id(self):
		return 1

	def __init__(self, begin, end):
		self.begin, self.end = begin, end
		logging.basicConfig(filename=self.conf['logs']['crawler'],
						format='%(asctime)s - %(levelname)s:%(message)s', 
						level=logging.DEBUG,
						datefmt='%m/%d/%Y %I:%M:%S %p')

	def run(self):
		for self.key in range(self.begin,self.end + 1):
			task = ANNTask(self.key)
			self.json = task.crawl()
			self.put()


class ANNTask(SiteTask):

	def __init__(self, key):
		self.key = key

	@property	
	def id(self):
		return 1

	def request_url(self, param):
		return self.site['format'] % (self.site['api_url'] , param)
		

	def retrieve(self, leafXML, element):
		attrs = {}
		if element['property'] != None:
			attrs = {element['property'] : element['value']} 

		return leafXML.findAll(element['tag'], attrs=attrs)

	def crawl(self):
		result = defaultdict(list)
		try:
			url = self.request_url(self.key)
			xml = urllib2.urlopen(url)
		except Exception as e:
			logging.warning('Failed info in % with key %d, raise: ', self.source, self.key, e.message)
			return result
			
		logging.info('Getting anime info from %s with key %d', self.source, self.key)
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
	
def main():
	orchestrate = ANNOrchestrate(539,13900)
	orchestrate.run()

if __name__ == '__main__':
	main()
