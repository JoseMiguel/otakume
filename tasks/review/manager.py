import os
import tasks.core.OrchestrateTask

class Manager(OrchestrateTask,SiteTask):
	@property
	def id(sef):
		return 2

	def associate(self):
		self.key = self.site['season'] + self.site['year'] 
		item = self.getItems()
		for item in items:
			entity = self.nearby(item.json['title'])
			self.put_relation(entity.collection, entity.key, 'review', item.collection ,item.key)
		
