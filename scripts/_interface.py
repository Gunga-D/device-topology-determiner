from tkinter import *


class View(Tk):
	def __init__(self, view_config, simulation_config, controller):
		self.__controller = controller

		super().__init__()

		self.__width = view_config['app']['width']
		self.__height = view_config['app']['height']
		self.geometry(str(self.__width) + 'x' + str(self.__height))

		self.resizable(width=False, height=False)

		header_block = Frame(self, bg = '#8a8a8a')
		header_block.place(relx = 0.5, rely = 0, anchor = "n",
								  height = 6 * self.__height / 20, width = self.__width)

		body_block = Frame(self, bg = '#bababa')
		body_block.place(relx = 0.5, rely = 6 * self.__height / (20 * self.__height), anchor = "n",
								height = 13 * self.__height / 20, width = self.__width)

		footer_block = Frame(self, bg = '#bababa')
		footer_block.place(relx = 0.5, rely = 1, anchor = "s",
								  height = self.__height / 20, width = self.__width)


		self.__create_models_settings(header_block, simulation_config)
		self.__create_simulation_settings(header_block, simulation_config)


		self.__simulation_display = self.__create_simulation_display(body_block)
		self.__update_simulation_display(self.__simulation_display, view_config['simulation_display']['zoom'])


		def zoom_callback(zoom):
			value = zoom.get()
			if value >= 1000:
				zoom.set(999)
			if value <= 0:
				zoom.set(1)
			self.__update_simulation_display(self.__simulation_display, value)
		self.__zoom = self.__create_zoom_instrument(footer_block, view_config['simulation_display']['zoom'], zoom_callback)

		self.__simulation_status = self.__create_simulation_status(footer_block)
		self.__update_simulation_status(self.__simulation_status, self.__controller.current_status)

	def __create_models_settings(self, master, start_values):
		models_settings_block = Frame(master, bg = '#8a8a8a')
		models_settings_block.pack(expand = True, side = 'left', fill = 'both')

		self.update()
		models_settings_block_width = models_settings_block.winfo_width()
		models_settings_block_height = models_settings_block.winfo_height()

		Label(master = models_settings_block, text = "Модели", fg = '#3b3b3b', bg = "#9e9e9e").place(relx = 0.5, rely = 1,
																					 anchor = "s", width = models_settings_block_width, height = 20)


		wave_settings_block = Frame(models_settings_block, bg = '#8a8a8a')
		wave_settings_block.place(relx = 0, rely = 0, width = models_settings_block_width / 2, height = models_settings_block_height - 20)

		wave_distance_string_variable = StringVar()
		wave_distance_string_variable.set(str(start_values['process']['distance']))
		Label(wave_settings_block, text = "Дист. источника, м:", bg = '#8a8a8a').grid(row = 0, column = 0, sticky = 'w', padx = 5, pady = 3)
		Entry(wave_settings_block, textvariable = wave_distance_string_variable, justify = 'left').grid(row = 0, column = 1, padx = 5, pady = 3)

		wave_angle_string_variable = StringVar()
		wave_angle_string_variable.set(str(start_values['process']['angle']))
		Label(wave_settings_block, text = "Угол наклона, °:", bg = '#8a8a8a').grid(row = 1, column = 0, sticky = 'w', padx = 5, pady = 3)
		Entry(wave_settings_block, textvariable = wave_angle_string_variable, justify = 'left').grid(row = 1, column = 1, padx = 5, pady = 3)

		pressure_amplitude_string_variable = StringVar()
		pressure_amplitude_string_variable.set(str(start_values['process']['pressure_amplitude']))
		Label(wave_settings_block, text = "Амплитуда, Па:", bg = '#8a8a8a').grid(row = 2, column = 0, sticky = 'w', padx = 5, pady = 3)
		Entry(wave_settings_block, textvariable = pressure_amplitude_string_variable, justify = 'left').grid(row = 2, column = 1, padx = 5, pady = 3)

		pressure_frequency_string_variable = StringVar()
		pressure_frequency_string_variable.set(str(start_values['process']['pressure_frequency']))
		Label(wave_settings_block, text = "Частота, Гц:", bg = '#8a8a8a').grid(row = 3, column = 0, sticky = 'w', padx = 5, pady = 3)
		Entry(wave_settings_block, textvariable = pressure_frequency_string_variable, justify = 'left').grid(row = 3, column = 1, padx = 5, pady = 2)

		ambient_temperature_string_variable = StringVar()
		ambient_temperature_string_variable.set(str(start_values['process']['ambient_temperature']))
		Label(wave_settings_block, text = "Темп. окр. среды, °C:", bg = '#8a8a8a').grid(row = 4, column = 0, sticky = 'w', padx = 5, pady = 3)
		Entry(wave_settings_block, textvariable = ambient_temperature_string_variable, justify = 'left').grid(row = 4, column = 1, padx = 5, pady = 3)


		device_settings_block = Frame(models_settings_block, bg = '#8a8a8a')
		device_settings_block.place(relx = 0.5, rely = 0, width = models_settings_block_width / 2, height = models_settings_block_height - 20)

		volume_equalizers_number_string_variable = StringVar()
		volume_equalizers_number_string_variable.set(str(start_values['receiver']['device']['volume_equalizers_number']))
		Label(device_settings_block, text = "Кол-во усред. объема:", bg = '#8a8a8a').grid(row = 0, column = 0, sticky = 'w', padx = 5, pady = 3)
		Entry(device_settings_block, textvariable = volume_equalizers_number_string_variable, justify = 'left').grid(row = 0, column = 1, padx = 5, pady = 3)

		volume_equalizers_distance_string_variable = StringVar()
		volume_equalizers_distance_string_variable.set(str(start_values['receiver']['device']['volume_equalizers_distance']))
		Label(device_settings_block, text = "Дист. усред. объема:", bg = '#8a8a8a').grid(row = 1, column = 0, sticky = 'w', padx = 5, pady = 3)
		Entry(device_settings_block, textvariable = volume_equalizers_distance_string_variable, justify = 'left').grid(row = 1, column = 1, padx = 5, pady = 3)

		ports_number_string_variable = StringVar()
		ports_number_string_variable.set(str(start_values['receiver']['volume_equalizer']['ports_number']))
		Label(device_settings_block, text = "Кол-во портов:", bg = '#8a8a8a').grid(row = 2, column = 0, sticky = 'w', padx = 5, pady = 3)
		Entry(device_settings_block, textvariable = ports_number_string_variable, justify = 'left').grid(row = 2, column = 1, padx = 5, pady = 3)

		ports_distance_string_variable = StringVar()
		ports_distance_string_variable.set(str(start_values['receiver']['volume_equalizer']['ports_distance']))
		Label(device_settings_block, text = "Дист. портов:", bg = '#8a8a8a').grid(row = 3, column = 0, sticky = 'w', padx = 5, pady = 3)
		Entry(device_settings_block, textvariable = ports_distance_string_variable, justify = 'left').grid(row = 3, column = 1, padx = 5, pady = 3)


		def deep_update_simulation():
			self.__controller.update_device(int(volume_equalizers_number_string_variable.get()), float(volume_equalizers_distance_string_variable.get()), 
											int(ports_number_string_variable.get()), float(ports_distance_string_variable.get()))
			self.__controller.update_process(float(wave_distance_string_variable.get()), float(wave_angle_string_variable.get()),
											 float(pressure_amplitude_string_variable.get()), float(pressure_frequency_string_variable.get()), 
											 float(ambient_temperature_string_variable.get()))

			self.__update_simulation_display(self.__simulation_display, self.__get_zoom_value(self.__zoom))

		Button(models_settings_block, text = 'Применить', bg = '#25b8f7',
		 	   command = deep_update_simulation).place(relx = 0.5, y = models_settings_block_height - 23, anchor = "s",
													   width = models_settings_block_width, height = 22)


		Frame(models_settings_block, bg = '#787777').place(relx = 1, rely = 0, anchor = "e", width = 0.5,
														   height = models_settings_block_height * 2)

	def __create_simulation_settings(self, master, start_values):
		simulation_settings_block = Frame(master, bg = '#8a8a8a')
		simulation_settings_block.pack(expand = True, side = 'left', fill = 'both')

		self.update()
		simulation_settings_block_width = simulation_settings_block.winfo_width()
		simulation_settings_block_height = simulation_settings_block.winfo_height()

		Label(master = simulation_settings_block, text = "Симуляция", fg = '#3b3b3b', bg = "#9e9e9e").place(relx = 0.5, rely = 1,
																							anchor = "s", width = simulation_settings_block_width, height = 20)


		simulation_result = Frame(simulation_settings_block, bg = '#8a8a8a')
		simulation_result.place(relx = 0, rely = 0,
		 						width = simulation_settings_block_width, height = 7 * (simulation_settings_block_height - 20) / 10)

		Label(simulation_result, text = "Результат", bg = '#8a8a8a').grid(row = 0, column = 0, columnspan = 2, padx = 5, pady = 3)

		teoretical_value_string_variable = StringVar()
		teoretical_value_string_variable.set(str(self.__controller.teoretical_value))
		Label(simulation_result, text = "Теор. значение:", bg = '#8a8a8a').grid(row = 1, column = 0, sticky = 'w', padx = 5, pady = 3)
		Entry(simulation_result, textvariable = teoretical_value_string_variable, justify = 'left').grid(row = 1, column = 1, padx = 5, pady = 3)

		experimental_value_string_variable = StringVar()
		Label(simulation_result, text = "Эксп. значение:", bg = '#8a8a8a').grid(row = 2, column = 0, sticky = 'w', padx = 5, pady = 3)
		Entry(simulation_result, textvariable = experimental_value_string_variable, justify = 'left').grid(row = 2, column = 1, padx = 5, pady = 3)


		simulation_start_block = Frame(simulation_settings_block, bg = '#9e9e9e')
		simulation_start_block.place(relx = 0, y = 7 * (simulation_settings_block_height - 20) / 10,
		 							 width = simulation_settings_block_width, height = 3 * (simulation_settings_block_height - 20) / 10)

		stop_time_variable = IntVar()
		stop_time_variable.set(start_values['stop_time'])
		Label(simulation_start_block, text = "Время моделирования, с:", bg = '#9e9e9e').grid(row = 0, column = 0, sticky = 'w', padx = 5)
		Entry(simulation_start_block, textvariable = stop_time_variable, justify = 'left').grid(row = 0, column = 1, padx = 18)

		def start_simulation():
			self.__update_simulation_status(self.__simulation_status, self.__controller.current_status)
		def end_simulation():
			self.__update_simulation_status(self.__simulation_status, self.__controller.current_status)
			teoretical_value_string_variable.set(str(self.__controller.teoretical_value))
			experimental_value_string_variable.set(str(self.__controller.experimental_value))
		Button(simulation_start_block, text = 'Запустить', bg = '#18f571',
		 	   command = lambda: self.__controller.start_simulation(stop_time_variable.get(),
		 	    													start_simulation,
		 	    													end_simulation)).place(relx = 0.5, 
		 	   																			   y = 3 * (simulation_settings_block_height - 20) / 10 - 3,
		 	    																		   anchor = "s", 
		 	    																		   width = simulation_settings_block_width,
		 	    																		   height = 22)

	def __create_simulation_display(self, master):
		canvas = Canvas(master, bg = 'white', highlightthickness = 1, highlightbackground = "black")
		canvas.pack(expand = True, fill = 'both', padx = 8, pady = 10)
		return canvas

	def __update_simulation_display(self, simulation_display, zoom):
		normalized_zoom = (100 / zoom)


		simulation_display.delete("all")

		self.update()
		simulation_display_center_pos_x = simulation_display.winfo_width() / 2
		simulation_display_center_pos_y = simulation_display.winfo_height() / 2


		for process_determinant in self.__controller.process_determinants:
			element_pos_x = simulation_display_center_pos_x + process_determinant.position[0] * 10 * normalized_zoom
			element_pos_y = simulation_display_center_pos_y + process_determinant.position[1] * 10 * normalized_zoom
			self.__simulation_display.create_oval(element_pos_x - 5 * normalized_zoom, element_pos_y - 5 * normalized_zoom,
			 									  element_pos_x + 5 * normalized_zoom, element_pos_y + 5 * normalized_zoom, width = 1)


		source_position_x = simulation_display_center_pos_x + self.__controller.process_info['source_position'][0] * 10 * normalized_zoom
		source_position_y = simulation_display_center_pos_y + self.__controller.process_info['source_position'][1] * 10 * normalized_zoom

		direction_x = self.__controller.process_info['direction'][0] * 40 * normalized_zoom
		direction_y = self.__controller.process_info['direction'][1] * 40 * normalized_zoom
		self.__simulation_display.create_line(source_position_x, source_position_y, source_position_x + direction_x, source_position_y + direction_y,
											  fill = '#f5a142', width = 3, arrow = LAST, arrowshape = "8 15 8")

		first_point_front_x = source_position_x + 65 * normalized_zoom
		first_point_front_y = (direction_y * source_position_y + direction_x * source_position_x - direction_x * first_point_front_x) / direction_y
		second_point_front_x = source_position_x - 65 * normalized_zoom
		second_point_front_y = (direction_y * source_position_y + direction_x * source_position_x - direction_x * second_point_front_x) / direction_y
		self.__simulation_display.create_line(first_point_front_x, first_point_front_y, second_point_front_x, second_point_front_y,
											  fill = '#f5a142', width = 3)

	def __create_zoom_instrument(self, master, start_zoom_value, callback):
		zoom_variable = IntVar()
		zoom_variable.set(start_zoom_value)
		zoom_variable.trace("w", lambda name, index, mode, zoom = zoom_variable: callback(zoom))

		Entry(master, textvariable = zoom_variable, justify = 'center', bg = '#bababa').place(relx = 0.5, rely = 0.5, width = 25, anchor = 'c')
		Label(master, text = '%', justify = 'left', bg = '#bababa').place(x = self.__width / 2 + 25, rely = 0.5, width = 10, anchor = 'c')
		return zoom_variable

	def __get_zoom_value(self, zoom):
		return zoom.get()

	def __create_simulation_status(self, master):
		status = Label(master = master, fg = 'black', bg = "#bababa")
		status.place(x = 8, rely = 0.5, anchor = 'w')
		return status

	def __update_simulation_status(self, status_object, to):
		status_object.config(text = to)

	def show(self):
		self.mainloop()