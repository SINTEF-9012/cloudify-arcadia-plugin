from abc import ABCMeta
from abc import abstractmethod

class ABCPrettyPrinter(object):

	__metaclass__ = ABCMeta

	@abstractmethod
	def print_pretty(self, node):
		pass