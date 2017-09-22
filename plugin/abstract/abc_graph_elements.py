from abc import ABCMeta
from abc import abstractmethod


class Visitee(object):

	__metaclass__ = ABCMeta

	@abstractmethod
	def accept(self, visitor):
		pass

class ABCGraphElement(Visitee):

	__metaclass__= ABCMeta

	@abstractmethod
	def print_element(self, printer):
		pass

	@abstractmethod
	def get_instance(self):
		pass