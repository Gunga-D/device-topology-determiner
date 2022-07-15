import numpy as np
import mechanism._receiver
import _config_determinant
import _process
import _simulation
import _interface


simulation_config = _config_determinant.read_config('../configs/.simulation.yaml')

wave = _process.Wave(simulation_config['process'])

device = mechanism._receiver.Device(simulation_config['receiver']['device'])
device.init_volume_equalizers(simulation_config['receiver']['volume_equalizer'])

back_end = _simulation.Controller(device, wave)


front_end = _interface.View(_config_determinant.read_config('../configs/.application_interface.yaml'), simulation_config, back_end)
front_end.show()