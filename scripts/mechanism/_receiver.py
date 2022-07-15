import numpy as np
import _receiver_topology


class Device(_receiver_topology.Ring):
	def __init__(self, config):
		self.__average_pressures = []
		self.__standard_deviations= []

		self.__position = np.array((config['device_position_x'], config['device_position_y']))
		self.__volume_equalizers = super().produce(center_position = self.__position, element_distance = config['volume_equalizers_distance'],
													element = VolumeEqualizer, elements_number = config['volume_equalizers_number'])

	def init_volume_equalizers(self, config):
		for volume_equalizer in self.__volume_equalizers:
			volume_equalizer.init_internal_structure(config['ports_number'], config['ports_distance'])

	def calculate_average_pressure(self):
		sum_pressure = 0
		active_ports_number = 0
		for port in self.ports:
			if port.is_port_active():
				sum_pressure += port.pressure
				active_ports_number += 1

		average_pressure = sum_pressure / active_ports_number
		self.__average_pressures.append(average_pressure)
		return average_pressure

	@property
	def pressure_amplitude(self):
		return max(self.__average_pressures)
		
	@property
	def position(self):
		return self.__position

	@property
	def ports(self):
		ports = []
		for volume_equalizer in self.__volume_equalizers:
			ports.extend(volume_equalizer.ports)
		return ports
	
class VolumeEqualizer(_receiver_topology.Ring):
	def init_internal_structure(self, ports_number, ports_distance,):
		self.__ports = super().produce(center_position = self.__position, element_distance = ports_distance,
										element = Port, elements_number = ports_number)

	@property
	def ports(self):
		return self.__ports

	@property
	def position(self):
		return self.__position

	@position.setter
	def position(self, value):
		self.__position = value

class Port():
	def __init__(self):
		self.__pressure = None

	def is_port_active(self):
		if self.__pressure:
			return True
		return False

	@property
	def position(self):
		return self.__position

	@position.setter
	def position(self, value):
		self.__position = value

	@property
	def pressure(self):
		return self.__pressure

	@pressure.setter
	def pressure(self, value):
		self.__pressure = value