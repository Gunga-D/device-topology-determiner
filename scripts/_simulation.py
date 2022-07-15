from enum import Enum


class Controller():
	def __init__(self, device, process):
		self.__simulation_status = Status.ready

		self.__device = device
		self.__process = process

	def update_device(self, volume_equalizers_number, volume_equalizers_distance, ports_number, ports_distance):
		new_device_config = {'device_position_x': self.__device.position[0], 'device_position_y': self.__device.position[1],
							 'volume_equalizers_number': volume_equalizers_number, 'volume_equalizers_distance': volume_equalizers_distance}
		self.__device.__init__(new_device_config)

		new_volume_equalizer_config = {'ports_number': ports_number, 'ports_distance': ports_distance}
		self.__device.init_volume_equalizers(new_volume_equalizer_config)

	def update_process(self, wave_distance, wave_angle, pressure_amplitude, pressure_frequency, ambient_temperature):
		new_process_config = {'end_point_x': self.__device.position[0], 'end_point_y': self.__device.position[1], 'distance': wave_distance, 'angle': wave_angle,
		 					  'pressure_amplitude': pressure_amplitude, 'pressure_frequency': pressure_frequency,
		 					  'ambient_temperature': ambient_temperature}
		self.__process.__init__(new_process_config)

	def start_simulation(self, stop_time, interface_start_callback, interface_end_callback):
		self.__simulation_status = Status.in_progress
		interface_start_callback()

		time = 0
		delta_time = 0.001
		while time < stop_time:
			for port in self.__device.ports:
				self.__process.has_front_arrived(time, port.position)
				port.pressure = self.__process.get_pressure(time, port.position)

			self.__device.calculate_average_pressure()

			time += delta_time

		self.__simulation_status = Status.ready
		interface_end_callback()

	@property
	def teoretical_value(self):
		return self.__process.pressure_amplitude

	@property
	def experimental_value(self):
		return self.__device.pressure_amplitude
	
	@property
	def current_status(self):
		return self.__simulation_status.value
		
	@property
	def process_determinants(self):
		return self.__device.ports

	@property
	def process_info(self):
		wave_info = {'source_position': self.__process.source_position, 'direction': self.__process.direction}
		return wave_info
	


class Status(Enum):
	ready = 'Готов'
	in_progress = 'В процессе'
	failed = 'Ошибка'