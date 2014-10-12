import os, abc
import logging
import configparser
import yaml
from porc import Client

class BaseTask(object):
	__metaclass__ = abc.ABCMeta

	@abc.abstractproperty
	def id(self):
		pass

	@property
	def conf(self):
		config_path = self.fileConfigPath('client.cfg')
		config = configparser.ConfigParser()
		config.read(config_path)
		return config

	def fileConfigPath(self,name):
		baseDir = os.path.dirname(os.path.abspath(__file__))
		return os.path.join(baseDir, '..','..',name)

	def getYAML(self, header, yaml_name):
		yaml_path = self.conf[header].get(yaml_name)
		with open(yaml_path,'r') as yaml_file:
		 	parts = yaml.safe_load(yaml_file)
		return parts
	
	def getYAMLPart(self, parts):
		foundPart = {}
		for part in parts:
			if part['id'] == self.id:
				foundPart = part
				break

		if not foundPart:
			print ('Didn\'t found a dict with id = %d ' % self.id)
		
		return foundPart
	

class OrchestrateTask(BaseTask):
	__metaclass__ = abc.ABCMeta

	def id(self):
		pass

	def get(self):
		pass
	
	def put(self):
		client = Client(self.api_key)
		result = client.put(self.collection,
								self.key,
								self.json)
		try:
			result.raise_for_status()
			if result != None:
				response = result.response
				logging.info('Orchestrate response: %s', result.reason)
				if response.reason == 'Created':
					logging.info('Orchestrate Finished Transaction OK')
				else:
					logging.warning('Orchestrate Failed Transaction: %s', result.reason)
		except Exception as e:
			logging.critical('Orchestrate failed with an exception: %s' % (e.message))
			raise

	def delete(self):
		pass

	@property
	def orchestrate_conf(self):
		return self.getYAML('persistance','orchestrate')

	@property
	def collection(self):
		part = self.getYAMLPart(self.orchestrate_conf['collections'])
		return part['name']

	@property
	def api_key(self):
		return self.orchestrate_conf['config']['api_key']


class SiteTask(BaseTask):
	__metaclass__ = abc.ABCMeta
	
	def id(self):
		pass

	@property
	def site(self):
		parts = self.getYAML('sources','sites')
		part = self.getYAMLPart(parts['sites'])
		return part

	@property
	def elements(self):
		return self.site['xml_element']

	@property
	def source(self):
		return self.site['name']


