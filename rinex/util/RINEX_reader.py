import georinex as gr

def extract_receiver_info(file_path):
	"""Reads the header of a RINEX file and extracts information about the receiver.

	Parameters:
	-----------
	:param file_path: str
		path to the RINEX file.

	:return: list
		list with info about the receiver in the format ['REC # / TYPE / VERS'].
	"""
	hdr = gr.rinexheader(file_path)
	rec_info = hdr['REC # / TYPE / VERS']  # e.g. 'XXXXXXXX            OnePlus             ONEPLUS A6003       '
	recc = rec_info.replace("            ", " / ")
	rec = " ".join(recc.split()) #.split(" / ")
	return rec

def extract_antenna_info(file_path):
	"""Reads the header of a RINEX file and extracts information about the antenna.

	Parameters:
	-----------
	:param file_path: str
		path to the RINEX file.

	:return: list
		list with info about the antenna in the format ['ANT # / TYPE'].
	"""
	hdr = gr.rinexheader(file_path)
	ant_info = hdr['ANT # / TYPE']  # e.g. 'XXXXXXXX            ONEPLUS A6003                           '
	antt = ant_info.replace("            ", " / ")
	ant = " ".join(antt.split())[:-2] #.split(" / ")[:-1]
	return ant

def extract_bounding_time(file_path):
	"""Reads a RINEX file and extracts information about start and end of the observation.

	Parameters:
	-----------
	:param file_path: str
		path to the RINEX file.

	:return: list
		list with two elements, respectively first and last datetime of the RINEX observations.
	"""
	times = gr.gettime(file_path)
	return [times[0], times[-1]]

def extract_systems_info(file_path):
	"""Reads a RINEX file and extracts information about start and end of the observation.

	Parameters:
	-----------
	:param file_path: str
		path to the RINEX file.

	:return: list
		nested list, where each element is a list containing respectively name of the system, 
        number of frequencies and informations whether "dual-frequency" has been employed.
	"""
	hdr = gr.rinexheader(file_path)
	sys_info = hdr['fields']
	return [[field, len(sys_info[field]), True] if len(sys_info[field]) > 4 else [field, len(sys_info[field]), False] for field in sys_info ]