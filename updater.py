import os
import sys
import shutil
import tempfile
import configparser
import requests

def get_profiles_ini():
    paths = [
        os.path.expanduser('~/Library/Application Support/Firefox/profiles.ini'),
        os.path.expanduser('~/.mozilla/firefox/profiles.ini')
    ]
    for path in paths:
        if os.path.isfile(path):
            return path
    return None

def read_profiles(profiles_ini):
    config = configparser.ConfigParser()
    config.read(profiles_ini)
    profiles = []
    for section in config.sections():
        if section.startswith('Profile'):
            profiles.append((config[section]['Name'], config[section]['Path'], config[section].getboolean('IsRelative', True)))
    return profiles

def choose_profile(profiles):
    print("Profiles found:\n––––––––––––––––––––––––––––––")
    for i, (name, path, _) in enumerate(profiles):
        print(f"{i}: {name} ({path})")
    print('––––––––––––––––––––––––––––––')
    while True:
        try:
            index = int(input('Select the profile number: '))
            if 0 <= index < len(profiles):
                return profiles[index]
            else:
                print("Invalid selection! Please choose a valid profile number.")
        except ValueError:
            print("Invalid input! Please enter a number.")

def download_file(url):
    response = requests.get(url, allow_redirects=True)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Error: Unable to download file from {url}")
        sys.exit(1)

def update_userjs(profile_path):
    userjs_url = 'https://raw.githubusercontent.com/J0ssel1n/Foxy/main/user.js'
    userjs_content = download_file(userjs_url)
    userjs_path = os.path.join(profile_path, 'user.js')

    # Backup existing user.js
    if os.path.exists(userjs_path):
        backup_path = os.path.join(profile_path, f'user.js.backup.{tempfile.mktemp()}')
        shutil.copy(userjs_path, backup_path)
        print(f"Backup of existing user.js created at: {backup_path}")

    # Write new user.js
    with open(userjs_path, 'w') as file:
        file.write(userjs_content)
    print("Updated user.js with the latest version.")

    # Append user-overrides.js if it exists
    overrides_path = os.path.join(profile_path, 'user-overrides.js')
    if os.path.exists(overrides_path):
        with open(overrides_path, 'r') as overrides_file:
            with open(userjs_path, 'a') as userjs_file:
                userjs_file.write('\n')
                userjs_file.write(overrides_file.read())
        print("Appended user-overrides.js to user.js.")
    else:
        print("No user-overrides.js file found.")

def main():
    profiles_ini = get_profiles_ini()
    if not profiles_ini:
        print("Error: Could not find profiles.ini file.")
        sys.exit(1)
    
    profiles = read_profiles(profiles_ini)
    if not profiles:
        print("Error: No profiles found in profiles.ini file.")
        sys.exit(1)

    name, path, is_relative = choose_profile(profiles)
    profile_path = os.path.join(os.path.dirname(profiles_ini), path) if is_relative else path
    print(f"Selected profile: {name} ({profile_path})")
    
    update_userjs(profile_path)

if __name__ == "__main__":
    main()