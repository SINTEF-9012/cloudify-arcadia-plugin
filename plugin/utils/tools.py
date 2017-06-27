
class Tools(object):

	@classmethod
	def generate_unique_id(self, instance):
		return id(instance)
