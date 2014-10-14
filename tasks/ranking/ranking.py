from bs4 import BeautifulSoup
import logging
from collections import defaultdict
from  tasks.core.base import SiteTask, OrchestrateTask
import urllib2
from porc import Client

class RankingTask(OrchestrateTask, SiteTask):
	
	@property	
	def id(self):
		return 1

	def run(self):
		self.key = 15775 
		features = self.site['features']
		return self.get().json['number_of_episodes']

def main():
	task = RankingTask()
	print task.run()


if __name__ == '__main__':
	main()
