import os
from xbmcvfs import translatePath

kodi_data_path = translatePath("special://userdata/")
print(f"Testing access to: {kodi_data_path}")
print(f"Contents: {os.listdir(kodi_data_path)}")
