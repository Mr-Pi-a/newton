import os


os.system("pip install -r requirements.txt")
file_path = "api_key.txt"
#  API key Config
try:
    with open(file_path, 'r') as file:
        api_key = file.read().strip()
except FileNotFoundError:
    api_key = input("Enter your API key: ")
    with open(file_path, 'w') as file:
        file.write(api_key)

print(f"Using API key: {api_key}")

# E-mail Config
if os.path.isfile('email_config.txt'):
    with open('email_config.txt', 'r') as config_file:
        email, password = config_file.read().strip().split('\n')
else:
    email = input("Enter your email address: ")
    password = input("Enter your email password: ")
    with open('email_config.txt', 'w') as config_file:
        config_file.write(f"{email}\n{password}")


file_path = "api_key_openweathermap.txt"
try:
    with open(file_path, 'r') as file:
        api_key = file.read().strip()
except FileNotFoundError:
    api_key = input("Enter your API key for openweathermap : ")
    with open(file_path, 'w') as file:
        file.write(api_key)

print(f"Using API key: {api_key}")




