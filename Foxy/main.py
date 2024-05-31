import os
import sys
import shutil
import tempfile
import configparser
import requests

def get_profiles_ini():
    paths = [
        os.path.expanduser('~/Library/Application Support/Firefox/profiles.ini'),  # macOS
        os.path.expanduser('~/.mozilla/firefox/profiles.ini'),  # Linux
        os.path.join(os.environ['APPDATA'], 'Mozilla', 'Firefox', 'profiles.ini')  # Windows
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
    print("Profiles found:\n")
    for i, (name, path, _) in enumerate(profiles):
        print(f"{i}: {name} ({path})")
    while True:
        try:
            index = int(input('\nSelect the profile number: '))
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

def compare_files(file1_content, file2_path):
    if not os.path.exists(file2_path):
        return False

    with open(file2_path, 'r') as file:
        file2_content = file.read()
    
    return file1_content == file2_content

def update_userjs(profile_path):
    userjs_url = 'https://raw.githubusercontent.com/J0ssel1n/Foxy/main/user.js'
    userjs_content = download_file(userjs_url)
    userjs_path = os.path.join(profile_path, 'user.js')

    if os.path.exists(userjs_path):
        if compare_files(userjs_content, userjs_path):
            print("The downloaded user.js is identical to the existing one. No changes needed.")
            return
        else:
            while True:
                choice = input("An existing user.js file is found. Do you want to overwrite it? (yes/no): ").strip().lower()
                if choice == 'yes':
                    with tempfile.NamedTemporaryFile(delete=False, dir=profile_path, prefix='user.js.backup.', suffix='') as temp_file:
                        backup_path = temp_file.name
                    shutil.copy(userjs_path, backup_path)
                    print(f"Backup of existing user.js created at: {backup_path}")
                    break
                elif choice == 'no':
                    print("Operation cancelled.")
                    return
                else:
                    print("Invalid choice. Please enter 'yes' or 'no'.")

    with open(userjs_path, 'w') as file:
        file.write(userjs_content)
    print("Updated user.js with the latest version.")

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