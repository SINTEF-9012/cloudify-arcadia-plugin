from plugin.api.responses import ARCADIACompResponse


class ARCADIARestAPIClient(object):

	def __init__(self, *args, **kwargs):
		pass

	def get_component_info(self, cnid):
		#make a call here
		#if request_fals:
		#	return {'rc' : 1, 'message' : reason}

		response = ARCADIACompResponse(cepcid='cepcid', ecepcid='ecepcid')
		return {'rc' : 0, 'message' : 'SUCCESS', 'response' : response}

	def register_service_graph(self, service_tree):
		#make a call here
		#service_tree.print_element will print xml, or any other format which is set by ARCADIAClientFacade
		#if request_fals:
		#	return {'rc' : 1, 'message' : reason}

		return {'rc' : 0, 'message' : 'SUCCESS'}