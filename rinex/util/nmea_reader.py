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
	df = pd.read_csv(file_path, header=None, skiprows=4, usecols=[1, 2, 3, 5], names=['type', 'time', 'lat', 'lon'])
	df_filtered = df[df.type.str.contains('GGA')]  # takes only $GGA entries

	min_lat = min(df_filtered.lat)
	max_lat = max(df_filtered.lat)
	min_lon = min(df_filtered.lon)
	max_lon = max(df_filtered.lon)

	return [min_lon, min_lat, max_lon, max_lat]