import os
import getpass
import shutil
import win32com.client
import winreg
import subprocess


mylog = open("C:\\Users\Dcocuments\logs.txt", "a")


def disable_user_account(username):
    try:
        # Disable the user account
        subprocess.run(["net", "user", username, "/active:no"], check=True)
        mylog.write(f"Disabled user account: {username}")
    except subprocess.CalledProcessError as e:
        mylog.write(f"Error occurred while disabling user account: {e}")


def delete_user_profiles():
    
    current_user = getpass.getuser()
    exclude_folders = [current_user, "Default", "Public"]

    users_folder = "C:\\Users"
    user_folders = [folder for folder in os.listdir(users_folder) if os.path.isdir(os.path.join(users_folder, folder))]

    for folder in user_folders:
        if folder not in exclude_folders and not folder.startswith(("saf", "sfc")):
            folder_path = os.path.join(users_folder, folder)
            try:
                # Attempt to delete user profile folder
                shutil.rmtree(folder_path)
                
                mylog.write(f"Deleted user profile: {folder_path}")

                # Delete user profile from the registry
                try:
                    subkey = r"SOFTWARE\\Microsoft\Windows NT\\CurrentVersion\\ProfileList"
                    with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, subkey) as key:
                        user_sid = winreg.QueryInfoKey(key)[0]
                        
                        mylog.write(f'User_SID: {user_sid}')
                        
                        while user_sid:
                            sid = winreg.EnumKey(key, user_sid)
                            
                            try:
                                with winreg.OpenKey(key, sid) as user_key:
                                    profile_path = winreg.QueryValueEx(user_key, "ProfileImagePath")[0]
                                    
                                    mylog.write(f'Profile Path: {profile_path}')
                                    mylog.write(f'Key: {key}')
                                    mylog.write(f'SID: {sid}')
                                    
                                    if profile_path == folder_path:
                                        
                                        # Disable user account
                                        username = os.path.split(profile_path)[-1]
                                        
                                        mylog.write(f"Usernames: {username}")
                                        
                                        disable_user_account(username)
                                        winreg.DeleteKey(key, sid)
                                        mylog.write(f"Deleted user profile registry key: {sid}")
                                        break
                            except Exception as e:
                                mylog.write(f"Error occurred while deleting user profile registry key: {e}")
                            user_sid -= 1
                except Exception as e:
                    mylog.write(f"Error occurred while deleting user profile registry key: {e}")
            except Exception as e:
                mylog.write(f"Error occurred while deleting profile {folder_path}: {e}")

if __name__ == "__main__":
    # Check if the script is run with administrative privileges
    if not os.environ.get("ADMIN"):
        # Re-run the script with administrative privileges
        params = f"{os.path.abspath(__file__)}"
        try:
            # Try running the script with elevated privileges
            shell.ShellExecuteEx(lpVerb="runas", lpFile=sys.executable, lpParameters=params)
        except Exception as e:
            mylog.write(f"Error: {e}")
        else:
            os.environ["ADMIN"] = "1"
    else:
        delete_user_profiles()
