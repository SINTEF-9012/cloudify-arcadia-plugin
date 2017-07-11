from plugin.api.responses import ARCADIACompResponse

from requests import get, post, codes
import xml.etree.ElementTree as etree

HOST_NAME = "127.0.0.1"
PORT = 80

URL = "http://{host}:{port}".format(
        host=HOST_NAME,
        port=PORT)

ERROR_CANNOT_POST = "Unable to post service graph at {url}.\n{response}"
ERROR_CANNOT_FETCH_CNID = "Unable to fetch '{cnid}' information.\n{response}"

class ARCADIARestAPIClient(object):

	def __init__(self, *args, **kwargs):
		pass

	def get_component_info(self, cnid):
		response = get(URL + "/components/" + cnid,
						headers = {"Accept": "application/xml"})

		if response.status_code not in [200, 204]:
			message = ERROR_CANNOT_FETCH_CNID.format(
							cnid=cnid,
							response=response.text)
			return { "rc": 1, "message": message}

		node = etree.fromstring(response.text)
		_cepcid = node.find("CEPCID").text if node.find("CEPCID") is not None else None
		_ecepid = node.find("ECEPID").text if node.find("ECEPID") is not None else None
		response = ARCADIACompResponse(cepcid=_cepcid, ecepcid=_ecepid)
		return {'rc' : 0, 'message' : 'SUCCESS', 'response' : response}

	def register_service_graph(self, service_tree):
		payload = service_tree.print_element()
		response = post(URL + "/register",
				headers={"content-type": "application/xml"},
				data=payload)

		if response.status_code not in [200, 204]:
			message = ERROR_CANNOT_POST.format(
								url=URL,
								response=response.text)
			return {'rc' : 1, 'message' : message}

		return {'rc' : 0, 'message' : 'SUCCESS'}
