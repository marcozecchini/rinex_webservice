import pandas as pd

def extract_bbox_from_NMEA(file_path):
	"""Reads a NMEA file and extracts the bounding box.

	Parameters:
	-----------
	:param file_path: str
		path to the NMEA file.

	:return: list
		the bounding box as a list in the format [left, bottom, right, top], i.e. [min Longitude, min Latitude, max Longitude, max Latitude].
	"""
	df = pd.read_csv(file_path, header=None, skiprows=4, usecols=[1, 2, 3, 4, 5, 6],
					 names=['type', 'time', 'lat', 'N-S', 'lon', 'E-W'])
	df_filtered = df[df.type.str.contains('GGA')]  # takes only $GGA entries

	# converting str to floats (eventual errors are coerced to NaNs)
	df_float = df_filtered.copy()
	df_float[['time', 'lat', 'lon']] = df_filtered[['time', 'lat', 'lon']].apply(pd.to_numeric, errors='coerce')

	# changing lat to -lat if Southern Hemisphere, and lon to -lon if Western Hemisphere
	# AND dividing by 100 (lat-lon in NMEA files are multiplied by 100)
	df_final = df_float.copy()
	df_final['lat'] = df_float.apply(lambda x: -x['lat'] / 100 if x['N-S'] == 'S' else x['lat'] / 100, axis=1)
	df_final['lon'] = df_float.apply(lambda x: -x['lon'] / 100 if x['E-W'] == 'W' else x['lon'] / 100, axis=1)

	min_lat = min(df_final.lat)
	max_lat = max(df_final.lat)
	min_lon = min(df_final.lon)
	max_lon = max(df_final.lon)

	return [min_lon, min_lat, max_lon, max_lat]


## OLD VERSION
def extract_bbox_from_NMEA__OLD(file_path):
	"""Reads a NMEA file and extracts the bounding box.

	Parameters:
	-----------
	:param file_path: str
		path to the NMEA file.

	:return: list
		the bounding box as a list in the format [left, bottom, right, top], i.e. [min Longitude, min Latitude, max Longitude, max Latitude].
	"""
	df = pd.read_csv(file_path, header=None, skiprows=4, usecols=[1, 2, 3, 5], names=['type', 'time', 'lat', 'lon'])
	df_filtered = df[df.type.str.contains('GGA')]  # takes only $GGA entries
	df_filtered = df_filtered.dropna()

	min_lat = min(df_filtered.lat)
	max_lat = max(df_filtered.lat)
	min_lon = min(df_filtered.lon)
	max_lon = max(df_filtered.lon)

	return [min_lon, min_lat, max_lon, max_lat]