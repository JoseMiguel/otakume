import os, abc
import configparser
import yaml

class Source(object):
	__metaclass__ = abc.ABCMeta

	@abc.abstractproperty
	def id(self):
		pass
	
	def put(self):
		pass

	@property
	def conf(self):
		baseDir = os.path.dirname(os.path.abspath(__file__))
		configFileDir = os.path.join(baseDir, '..','..','client.cfg')
		config = configparser.ConfigParser()
		config.read(configFileDir)
		return config


	@property
	def site(self):
		sitesDir = self.conf['config'].get('sites')
		with open(sitesDir,'r') as sitesFile:
		 	sites = yaml.safe_load(sitesFile)

		foundSite = {}
		for name , site in sites.iteritems():
			if site['id'] == self.id:
				foundSite = site

		if not foundSite:
			raise('Didn\'t found a site with id = %d ' % self.id)

		return foundSite

	@property
	def elements(self):
		return self.site['xml_element']

	@property
	def source(self):
		return self.site['name']


