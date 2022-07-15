import numpy as np
from abc import ABC, abstractmethod


class Topology(ABC):
	@abstractmethod
	def produce(self):
		pass

class Ring(Topology):
	def produce(self, center_position, element_distance, element, elements_number):
		elements = []

		delta_angle = np.radians(360 / elements_number)
		for index_element in range(elements_number):
			new_element = element()

			pos_x = center_position[0] + np.cos(delta_angle * index_element) * element_distance
			pos_y = center_position[1] + np.sin(delta_angle * index_element) * element_distance
			new_element.position = np.array((pos_x, pos_y))

			elements.append(new_element)

		return elements