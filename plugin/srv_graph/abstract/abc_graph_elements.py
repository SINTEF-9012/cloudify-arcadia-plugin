from abc import ABCMeta
from abc import abstractmethod

class ABCGraphElement(object):

	__metaclass__= ABCMeta

	@abstractmethod
	def print_element(self):
		pass

	@abstractmethod
	def get_instance(self):
		pass