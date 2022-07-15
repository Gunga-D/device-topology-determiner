import yaml


def read_config(path):
	loaded_data = None
	with open(path, 'r') as stream:
		loaded_data = yaml.safe_load(stream)
	return loaded_data

def write_config(path, data):
	with io.open(path, 'w', encoding='utf8') as stream:
		yaml.dump(data, stream, default_flow_style=False, allow_unicode=True)
