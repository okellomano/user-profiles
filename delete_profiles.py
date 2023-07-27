import datetime
import os
import subprocess
import winreg

#current_user = os.getlogin()
#log_file = open(f'C:\\Users\\{current_user}\\Documents\\logs.txt', 'a')


def disable_user_account(username):
    pass
    #try:
        # Disable the user account
     #   subprocess.run(["net", "user", username, "/active:no"], check=True)
      #  log_file.write(f"Disabled user account: {username} \n")
    #except subprocess.CalledProcessError as e:
     #   log_file.write(f"Error occurred while disabling user account: {e} \n")


def delete_user_profiles():
    current_user = os.getlogin()
    log_file = open(f'C:\\Users\\{current_user}\\Documents\\logs.txt', 'a')

    exclude_folders = [current_user, 'Default', 'Public']
    users_folder = 'C:\\Users'

    # Folders in the Users folder
    user_folders = [folder for folder in os.listdir(users_folder) if os.path.isdir(os.path.join(users_folder, folder))]

    log_file.write(f'User folders:: {user_folders} \n\n')

    # Folders to delete
    del_folders = [folder for folder in user_folders if folder not in exclude_folders and not folder.startswith(('saf', 'sfc'))]
    log_file.write(f'Folders to delete:: {del_folders} \n\n')

    # Delete the appropriate folders
    for folder in del_folders:
        folder_path = os.path.join(users_folder, folder)

        log_file.write(f'Folder paths to delete:: {folder_path} \n\n')

        try:
            subprocess.run(['rmdir', f'/s', f'/q', folder_path], shell=True)
            log_file.write(f'{datetime.datetime.now()}: Deleted user profiles: {del_folders} \n')

            # TODO:: Implement code to delete the user from the registry
            try:
                subkey = r'SOFTWARE\\Microsoft\Windows NT\\CurrentVersion\\ProfileList'
                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, subkey) as key:  # Open profile list
                    user_sid = winreg.QueryInfoKey(key)[0]  # The total number of subkeys [profiles in the ProfileList]
                    log_file.write(f'Number of profiles:: {user_sid} \n')

                    for i in range(user_sid):
                        sid = winreg.EnumKey(key, i)

                        log_file.write(f'SID:: {sid} \n')  # sid is a subkey of key [a single profile in a profile list]

                        try:
                            with winreg.OpenKey(key, sid) as user_key:  # Open a single profile
                                profile_path = winreg.QueryValueEx(user_key, 'ProfileImagePath')[0]  # user profile path e.g C:/Users/Mano

                                log_file.write(f'Folder path:: {folder_path} Profile path:: {profile_path} \n')

                                if folder_path == profile_path:
                                    log_file.write(f'Folder path {folder_path} equals profile path {profile_path} \n')
                                    # Disable user account
                                    username = os.path.split(profile_path)[-1]
                                    log_file.write(f'Username:: {username} \n')

                                    #disable_user_account(username)
                                    winreg.DeleteKey(key, sid)
                                    log_file.write(f"Deleted user profile registry key: {sid} \n")

                                    break
                        except Exception as e:
                            log_file.write(f'Error occurred while deleting user profile registry key: {e} \n')

            except Exception as e:
                log_file.write(f'Error occurred while deleting user profile registry key: {e} \n')
            # End TODO::
            
        except Exception as e:
            log_file.write(f'Error occurred while deleting profiles: {del_folders}: {e} \n')

if __name__ == '__main__':
    delete_user_profiles()



###########################################################################
# Optimized for modularity, space and time complexity


import datetime
import os
import subprocess
import winreg


def disable_user_account(username):
    try:
        # Disable the user account
        subprocess.run(["net", "user", username, "/active:no"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while disabling user account: {e}")
        

def get_user_folders():
    users_folder = 'C:\\Users'
    return [folder for folder in os.listdir(users_folder) if os.path.isdir(os.path.join(users_folder, folder))]


def delete_user_folders(folders, log_info):
    users_folder = 'C:\\Users'
    try:
        subprocess.run(['rmdir', f'/s', f'/q'] + [os.path.join(users_folder, folder) for folder in folders], shell=True)
        log_info.append(f'{datetime.datetime.now()}: Deleted user profiles: {folders}\n')
    except Exception as e:
        log_info.append(f'Error occurred while deleting profiles: {folders}: {e}\n')
        

def delete_user_registry_keys(folders, log_info):
    try:
        subkey = r'SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\ProfileList'
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, subkey) as key:
            user_sid = winreg.QueryInfoKey(key)[0]
            profiles_to_delete = set()
            for i in range(user_sid):
                sid = winreg.EnumKey(key, i)
                try:
                    with winreg.OpenKey(key, sid) as user_key:
                        profile_path = winreg.QueryValueEx(user_key, 'ProfileImagePath')[0]
                        username = os.path.basename(profile_path)
                        if username in folders:
                            profiles_to_delete.add(sid)
                except Exception as e:
                    log_info.append(f'Error occurred while accessing user profile registry key: {e}\n')

        for sid in profiles_to_delete:
            try:
                with winreg.OpenKey(key, sid) as user_key:
                    profile_path = winreg.QueryValueEx(user_key, 'ProfileImagePath')[0]
                    username = os.path.basename(profile_path)
                    log_info.append(f'Deleting user profile registry key for: {username}\n')
                    winreg.DeleteKey(key, sid)
            except Exception as e:
                log_info.append(f'Error occurred while deleting user profile registry key: {e}\n')

    except Exception as e:
        log_info.append(f'Error occurred while accessing user profile registry key: {e}\n')
        
        
def delete_user_profiles():
    ''' Deletes the user folders from system and from registry. '''
    current_user = os.getlogin()
    log_info = []

    exclude_folders = {current_user, 'Default', 'Public'}

    user_folders = get_user_folders()
    log_info.append(f'User folders: {user_folders}\n\n')

    # folders to delete
    del_folders = {folder for folder in user_folders if folder not in exclude_folders and not folder.startswith(('saf', 'sfc'))}
    log_info.append(f'Folders to delete: {del_folders}\n\n')

    delete_user_folders(del_folders, log_info)
    delete_user_registry_keys(del_folders, log_info)

    # Write log information to the file at once
    with open(f'C:\\Users\\{current_user}\\Documents\\logs.txt', 'a') as log_file:
        log_file.writelines(log_info)


if __name__ == '__main__':
    delete_user_profiles()
