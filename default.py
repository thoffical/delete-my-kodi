import os
import shutil
import xbmc
import xbmcgui
from xbmcvfs import translatePath


def uninstall_all_addons():
    """
    Uninstalls all third-party addons except for built-in addons like skins and script modules.
    """
    try:
        addons_path = translatePath("special://home/addons/")
        xbmc.log(f"Addons path resolved: {addons_path}", level=xbmc.LOGDEBUG)

        # Collect installed addons excluding built-in ones
        installed_addons = [
            addon for addon in os.listdir(addons_path)
            if os.path.isdir(os.path.join(addons_path, addon)) 
            and not addon.startswith(("skin.", "script."))
        ]

        if not installed_addons:
            xbmcgui.Dialog().ok("No Addons Found", "No third-party addons found to uninstall.")
            return

        dialog = xbmcgui.Dialog()
        if dialog.yesno(
            "Uninstall All Addons",
            f"Detected {len(installed_addons)} third-party addons. Do you want to uninstall them?"
        ):
            for addon_id in installed_addons:
                addon_path = os.path.join(addons_path, addon_id)
                try:
                    xbmc.log(f"Uninstalling addon: {addon_id}", level=xbmc.LOGINFO)
                    shutil.rmtree(addon_path)
                except Exception as e:
                    xbmc.log(f"Failed to uninstall addon {addon_id}: {str(e)}", level=xbmc.LOGERROR)

            xbmcgui.Dialog().ok("Success", "All third-party addons have been uninstalled.")
        else:
            xbmcgui.Dialog().ok("Canceled", "No addons were uninstalled.")

    except Exception as e:
        xbmcgui.Dialog().ok("Error", f"An error occurred while uninstalling addons: {str(e)}")
        xbmc.log(f"Critical Error in addon uninstallation: {str(e)}", level=xbmc.LOGERROR)


def clear_kodi_data():
    """
    Clears all userdata in the special://userdata/ directory.
    """
    try:
        userdata_path = translatePath("special://userdata/")
        xbmc.log(f"Resolved userdata path: {userdata_path}", level=xbmc.LOGDEBUG)

        # Verify path existence
        if not os.path.exists(userdata_path):
            xbmcgui.Dialog().ok("Error", f"Userdata path not found: {userdata_path}")
            return

        # Confirm action with the user
        dialog = xbmcgui.Dialog()
        if dialog.yesno(
            "Clear Kodi Data",
            f"This will erase all userdata in:\n{userdata_path}\nDo you want to proceed?"
        ):
            for item in os.listdir(userdata_path):
                item_path = os.path.join(userdata_path, item)
                try:
                    if os.path.isfile(item_path):
                        os.remove(item_path)
                    elif os.path.isdir(item_path):
                        shutil.rmtree(item_path)
                    xbmc.log(f"Deleted: {item_path}", level=xbmc.LOGINFO)
                except Exception as e:
                    xbmc.log(f"Failed to delete {item_path}: {str(e)}", level=xbmc.LOGERROR)

            xbmcgui.Dialog().ok("Success", "Kodi userdata has been cleared. Kodi will now restart.")
            xbmc.executebuiltin('Restart')
        else:
            xbmcgui.Dialog().ok("Canceled", "No changes were made.")

    except Exception as e:
        xbmcgui.Dialog().ok("Error", f"An error occurred while clearing userdata: {str(e)}")
        xbmc.log(f"Critical Error in userdata clearing: {str(e)}", level=xbmc.LOGERROR)


if __name__ == "__main__":
    try:
        uninstall_all_addons()  # Step 1: Uninstall all addons
        clear_kodi_data()       # Step 2: Clear userdata
    except Exception as main_error:
        xbmc.log(f"Critical Error in script: {str(main_error)}", level=xbmc.LOGERROR)
