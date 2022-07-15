import numpy as np


class Wave():
	def __init__(self, config):
		self.__speed = 332 + 0.6 * config['ambient_temperature']
		self.__source_position = np.array((config['distance'] * np.cos(np.radians(config['angle'])), config['distance'] * np.sin(np.radians(config['angle']))))

		self.__direction = np.array((config['end_point_x'] - self.__source_position[0], config['end_point_y'] - self.__source_position[1])) 
		self.__direction = self.__direction / np.linalg.norm(self.__direction)


		self.__pressure_amplitude = config['pressure_amplitude']
		self.__pressure_angular_frequency = 2 * np.pi * config['pressure_frequency']

	def get_front_position(self, time):
		return self.__source_position + self.__speed * time * self.__direction

	def has_front_arrived(self, time, position):
		angle = np.dot(position - self.get_front_position(time), self.__direction)
		if angle <= 0:
			return True
		return False 

	def get_source_pressure(self, time, start_phase):
		return (self.__pressure_amplitude) * np.sin(self.__pressure_angular_frequency * time + start_phase)

	def get_pressure(self, time, position):
		distance_between_points = np.linalg.norm(self.__source_position - position)
		shift_phase = self.__pressure_angular_frequency * distance_between_points / self.__speed
		return self.get_source_pressure(time, 0) * np.cos(shift_phase) - self.get_source_pressure(time, 90) * np.sin(shift_phase)

	@property
	def pressure_amplitude(self):
		return self.__pressure_amplitude
	
	@property
	def source_position(self):
		return self.__source_position

	@property
	def direction(self):
		return self.__direction
	