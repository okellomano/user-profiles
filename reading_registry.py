import winreg


# Location of Systme Files
# location = winreg.HKEY_LOCAL_MACHINE

# subkey contining user profiles
subkey = r"SOFTWARE\\Microsoft\Windows NT\\CurrentVersion\\ProfileList"

# Open the subkey as key [key is a list of profiles present]
# When the subkey is opened, I expect to see a list of specific user folders
with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, subkey) as key:  # Open ProfileList
    # get the security id of the user
    user_sid =  winreg.QueryInfoKey(key)[0]  # use 0 to get the number of subkeys this key has [i.e the total number of profiles]
    print(f'Number of profiles::: {user_sid}')  # Ex 6
    
    # For every user profile [key], Enumerate sunkeys of the open key to return the string
    
    while user_sid:
        sid = winreg.EnumKey(key, user_sid)  # key is the profile; user_sid is the index
        print(f'SID::: {sid}')  # sid is a subkey of key
        
        # Now open a single user key/profile
        with winreg.OpenKey(key, sid) as user_key:  # Open a single profile {soft}
            profile_path = winreg.QueryValueEx(user_key, "ProfileImagePath")[0]  # {value1} This should give e.g 'C\Users\Nomi
            print(f'Profile Path::: {profile_path}')
            
            # If the profile path is equal to the folder to be deleted; proceed and delete it
            # To delete it; you should delete the key associated with it
            
            # if profile_path == folder_path:
            #     winreg.DeleteKey(key, sid)
            
        user_sid -= 1
    
    