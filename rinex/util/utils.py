from zipfile import ZipFile 
import re
import os
from .nmea_reader import extract_bbox_from_NMEA
from .RINEX_reader import extract_antenna_info, extract_receiver_info, extract_systems_info, extract_bounding_time

def handle_uploaded_file(zipfile):
    result = {}
    with ZipFile(zipfile, 'r') as zip:
        for info in zip.infolist():
            print(info.filename)
            if "nmea" in info.filename:
                res = extract_bbox_from_NMEA(zip.open(info.filename))
                result['min_lat'] = res[1]
                result['min_lon'] = res[0]
                result['max_lat'] = res[3]
                result['max_lon'] = res[2]
            if (re.search("\.[0-9][0-9]o", info.filename)):
                zip.extract(info.filename)
                result['receiver_info'] = extract_receiver_info(info.filename) # trova il modo di passare il file senza salvarlo
                result['antenna_info'] = extract_antenna_info(info.filename)
               
                result['system_info'] = []
                result['number_sys_info'] = []
                result['dual_frequency'] = []

                temp = extract_systems_info(info.filename)
                for item in temp:
                    result['system_info'].append(item[0])
                    result['number_sys_info'].append(item[1])
                    result['dual_frequency'].append(item[2])

                temp = extract_bounding_time(info.filename)
                result['start_time'] = temp[0]
                result['finish_time'] = temp[1]
                os.remove(info.filename)
        print(result)
    return result