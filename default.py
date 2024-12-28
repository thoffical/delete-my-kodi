import os
import shutil
import xbmc
import xbmcgui

def clear_kodi_data():
    # Get Kodi's userdata path
    from xbmcvfs import translatePath
kodi_data_path = translatePath("special://userdata/")
    # Confirm action with the user
    dialog = xbmcgui.Dialog()
    if dialog.yesno("Clear Kodi Data", f"This will erase all data in:\n{kodi_data_path}\nDo you want to continue?"):
        try:
            # Delete all files and folders in the userdata directory
            for item in os.listdir(kodi_data_path):
                item_path = os.path.join(kodi_data_path, item)
                if os.path.isfile(item_path):
                    os.remove(item_path)
                elif os.path.isdir(item_path):
                    shutil.rmtree(item_path)
            xbmcgui.Dialog().ok("Clear Kodi Data", "Kodi data has been erased. Please restart Kodi.")
        except Exception as e:
            xbmcgui.Dialog().ok("Error", f"An error occurred: {str(e)}")
    else:
        xbmcgui.Dialog().ok("Clear Kodi Data", "Action canceled.")

if __name__ == 
