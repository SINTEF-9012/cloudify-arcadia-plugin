from plugin.api.responses import ARCADIACompResponse

from requests import post, codes


HOST_NAME = "34.250.221.100"
PORT = 80

URL = "http://{host}:{port}".format(
        host=HOST_NAME,
        port=PORT)


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
		#service_tree.print_element() will print xml, or any other format which is set by ARCADIAClientFacade
		#if request_fals:
		#	return {'rc' : 1, 'message' : reason}
		payload = service_tree.print_element()
		response = post(URL + "/register",
						headers={"content-type": "application/xml"},
						data=payload)
		if response.status_code != codes.ok:
			return {'rc' : 1, 'message' : "Unable to post service graph at {url}".format(url=URL)}

		return {'rc' : 0, 'message' : 'SUCCESS'}
