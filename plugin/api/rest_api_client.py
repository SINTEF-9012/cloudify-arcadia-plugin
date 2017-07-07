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
                        message = ERROR.CANNOT_FETCH_CNID.format(
                                cnid=cnid,
                                response=response.text)
                        return { "rc": 1, "message": message}
                node = etree.fromstring(response.text)
                nid = node.find("NID").text
                cnid = node.find("CNID").text
		response = ARCADIACompResponse(cepcid=nid, ecepcid=cnid)
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
		if response.status_code not in [200, 204]:
                        message = ERROR_CANNOT_POST.format(
                                url=URL,
                                response=response.text)
		        return {'rc' : 1, 'message' : message}

		return {'rc' : 0, 'message' : 'SUCCESS'}
