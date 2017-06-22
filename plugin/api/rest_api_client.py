

class ARCADIACompResponse(object):

	@property
	def cepcid(self):
		return self._cepcid

	@property
	def ecepid(self):
		return self._ecepid


class ARCADIARestAPIClient(object):

	def __init__(self, *args, **kwargs):
		pass

	def get_component_info(self, cnid):
		#make a call here
		response = ARCADIACompResponse()
		return {'rc' : 0, 'message' : 'SUCCESS', 'response' : response}


	def register_service_graph(self, service_tree):
		#make a call here
		#service_tree.print_element will print xml, or any other format which is set by ARCADIAClientFacade
		return {'rc' : 0, 'message' : 'SUCCESS'}