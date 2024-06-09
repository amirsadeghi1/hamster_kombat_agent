import requests
import json
import time
from datetime import datetime
from itertools import cycle
from colorama import init, Fore, Style
import logging

# Initialize colorama
init(autoreset=True)

def load_tokens(filename):
    with open(filename, 'r') as file:
        return [line.strip() for line in file]

def get_headers(token):
    return {
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Authorization': f'Bearer {token}',
        'Connection': 'keep-alive',
        'Origin': 'https://hamsterkombat.io',
        'Referer': 'https://hamsterkombat.io/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
        'Content-Type': 'application/json'
    }

def get_token(init_data_raw):
    url = 'https://api.hamsterkombat.io/auth/auth-by-telegram-webapp'
    headers = {
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'authorization' : 'authToken is empty, store token null',
        'Origin': 'https://hamsterkombat.io',
        'Referer': 'https://hamsterkombat.io/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Mobile Safari/537.36',
        'accept': 'application/json',
        'content-type': 'application/json'
    }
    data = json.dumps({"initDataRaw": init_data_raw})
    try:
        response = requests.post(url, headers=headers, data=data)
        if response.status_code == 200:
            return response.json()['authToken']
        elif response.status_code == 403:
            print(Fore.RED + Style.BRIGHT + "\rAccess denied. Status 403", flush=True)
        elif response.status_code == 500:
            print(Fore.RED + Style.BRIGHT + "\rInternal Server Error", flush=True)
        else:
            error_data = response.json()
            if "invalid" in error_data.get("error_code", "").lower():
                print(Fore.RED + Style.BRIGHT + "\rFailed to Get Token. Invalid init data", flush=True)
            else:
                print(Fore.RED + Style.BRIGHT + f"\rFailed to Get Token. {error_data}", flush=True)
    except requests.exceptions.Timeout:
        print(Fore.RED + Style.BRIGHT + "\rFailed to Get Token. Request Timeout", flush=True)
    except requests.exceptions.ConnectionError:
        print(Fore.RED + Style.BRIGHT + "\rFailed to Get Token. Connection Error", flush=True)
    except Exception as e:
        print(Fore.RED + Style.BRIGHT + f"\rFailed to Get Token. Error: {str(e)}", flush=True)
    return None
def authenticate(token):
    url = 'https://api.hamsterkombat.io/auth/me-telegram'
    headers = get_headers(token)
    response = requests.post(url, headers=headers)
    return response

def sync_clicker(token):
    url = 'https://api.hamsterkombat.io/clicker/sync'
    headers = get_headers(token)
    response = requests.post(url, headers=headers)
    return response

def claim_daily(token):
    url = 'https://api.hamsterkombat.io/clicker/check-task'
    headers = get_headers(token)
    headers['accept'] = 'application/json'
    headers['content-type'] = 'application/json'
    data = json.dumps({"taskId": "streak_days"})
    response = requests.post(url, headers=headers, data=data)
    return response
def upgrade(token, upgrade_type):
    url = 'https://api.hamsterkombat.io/clicker/buy-boost'
    headers = get_headers(token)
    headers['accept'] = 'application/json'
    headers['content-type'] = 'application/json'
    data = json.dumps({"boostId": upgrade_type, "timestamp": int(time.time())})
    response = requests.post(url, headers=headers, data=data)
    return response

def tap(token, max_taps, available_taps):
    url = 'https://api.hamsterkombat.io/clicker/tap'
    headers = get_headers(token)
    headers['accept'] = 'application/json'
    headers['content-type'] = 'application/json'
    data = json.dumps({"count": max_taps, "availableTaps": available_taps, "timestamp": int(time.time())})
    response = requests.post(url, headers=headers, data=data)
    return response

def list_tasks(token):
    url = 'https://api.hamsterkombat.io/clicker/list-tasks'
    headers = get_headers(token)
    response = requests.post(url, headers=headers)
    return response

def exchange(token):
    url = 'https://api.hamsterkombat.io/clicker/select-exchange'
    headers = get_headers(token)
    headers['accept'] = 'application/json'
    headers['content-type'] = 'application/json'
    data = json.dumps({"exchangeId": 'okx'})
    response = requests.post(url, headers=headers, data=data)
    return response

def claim_cipher(token, cipher_text):
    url = 'https://api.hamsterkombat.io/clicker/claim-daily-cipher'
    headers = get_headers(token)
    headers['accept'] = 'application/json'
    headers['content-type'] = 'application/json'
    data = json.dumps({"cipher": cipher_text})
    response = requests.post(url, headers=headers, data=data)
    
    # Add status code and response content checking
    if response.status_code == 200:
        try:
            # Try parsing JSON and continue the process
            return response
        except json.JSONDecodeError:
            print(Fore.RED + Style.BRIGHT + "Failed to parse JSON from response.", flush=True)
            return None
    elif response.status_code == 400:
        return response
    elif response.status_code == 500:
        print(Fore.RED + Style.BRIGHT + f"Failed to claim cipher, Internal Server Error", flush=True)
        return response
    else:
        print(Fore.RED + Style.BRIGHT + f"Failed to claim cipher, status code: {response.status_code}", flush=True)
        return None

def check_task(token, task_id):
    url = 'https://api.hamsterkombat.io/clicker/check-task'
    headers = get_headers(token)
    headers['accept'] = 'application/json'
    headers['content-type'] = 'application/json'
    data = json.dumps({"taskId": task_id})
    response = requests.post(url, headers=headers, data=data)
    return response

def use_booster(token):
    url = 'https://api.hamsterkombat.io/clicker/check-task'
    headers = get_headers(token)
    headers['accept'] = 'application/json'
    headers['content-type'] = 'application/json'
    data = json.dumps({"boostId": "BoostFullAvailableTaps", "timestamp": int(time.time())})
    response = requests.post(url, headers=headers, data=data)
    return response



def get_available_upgrades(token):
    url = 'https://api.hamsterkombat.io/clicker/upgrades-for-buy'
    headers = get_headers(token)
    response = requests.post(url, headers=headers)
    if response.status_code == 200:
        try:
            upgrades = response.json()['upgradesForBuy']
            print(Fore.GREEN + Style.BRIGHT + f"\r[ Upgrade Minning ] : Successfully get upgrade list.", flush=True)
            return upgrades
        except json.JSONDecodeError:
            print(Fore.RED + Style.BRIGHT + "\r[ Upgrade Minning ] : Failed to get JSON response.", flush=True)
            return []
    else:
        print(Fore.RED + Style.BRIGHT + f"\r[ Upgrade Minning ] : Failed to get upgrade list: Status {response.status_code}", flush=True)
        return []


def buy_upgrade(token, upgrade_id, upgrade_name):
    url = 'https://api.hamsterkombat.io/clicker/buy-upgrade'
    headers = get_headers(token)
    data = json.dumps({"upgradeId": upgrade_id, "timestamp": int(time.time())})
    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        try:
            print(Fore.GREEN + Style.BRIGHT + f"\r[ Upgrade Minning ] : Upgrade {upgrade_name} successfully purchased.", flush=True)
        except json.JSONDecodeError:
            print(Fore.RED + Style.BRIGHT + "\r[ Upgrade Minning ] : Failed to parse JSON during upgrade.", flush=True)
    else:
        try:
            error_response = response.json()
            if error_response.get('error_code') == 'INSUFFICIENT_FUNDS':
                print(Fore.RED + Style.BRIGHT + f"\r[ Upgrade Minning ] : Not enough coins wkwkw :V", flush=True)
                return 'insufficient_funds'
            else:
                print(Fore.RED + Style.BRIGHT + f"\r[ Upgrade Minning ] : Failed upgrade {upgrade_name}: {error_response}", flush=True)
                return []
        except json.JSONDecodeError:
            print(Fore.RED + Style.BRIGHT + f"\r[ Upgrade Minning ] : Failed to get JSON response. Status: {response.status_code}", flush=True)
            return []


def auto_upgrade_passive_earn(token):
    MAX_ATTEMPTS = 3
    ATTEMPT_DELAY = 1  # Delay in seconds between attempts

    for attempt in range(MAX_ATTEMPTS):
        upgrades = get_available_upgrades(token)
        
        if not upgrades:
            print(Fore.RED + Style.BRIGHT + "\r[ Upgrade Mining ] : No upgrades available or failed to get upgrade list.", flush=True)
            time.sleep(ATTEMPT_DELAY)
            continue
        
        for upgrade in upgrades:
            if upgrade['isAvailable'] and not upgrade['isExpired']:
                print(Fore.YELLOW + Style.BRIGHT + f"[ Upgrade Mining ] : {upgrade['name']} | Price: {upgrade['price']} | Profit: {upgrade['profitPerHour']} / Hour ")
                print(Fore.CYAN + Style.BRIGHT + f"\r[ Upgrade Mining ] : Upgrading {upgrade['name']}", end="", flush=True)
                
                result = buy_upgrade(token, upgrade['id'], upgrade['name'])
                
                if result == 'insufficient_funds':
                    print(Fore.RED + Style.BRIGHT + "\r[ Upgrade Mining ] : Insufficient funds. Switching to the next account.\n", flush=True)
                    return
                
                # If upgrade is successful, exit the function
                return
        
    print(Fore.RED + Style.BRIGHT + "\rFailed to upgrade after 3 attempts.", flush=True)

 
# [Main Code]
cek_task_dict = {}
claimed_ciphers = set()
def main():
    global cek_task_dict
    print_welcome_message()
    print(Fore.GREEN + Style.BRIGHT + "Starting Hamster Kombat....\n\n")
    init_data = load_tokens('initdata.txt')
    token_cycle = cycle(init_data)

    token_dict = {}  # Dictionary to store successful tokens
    while True:
        init_data_raw = next(token_cycle)
        token = token_dict.get(init_data_raw)
        
        if token:
            print(Fore.GREEN + Style.BRIGHT + f"\rUsing existing tokens...", end="", flush=True)
        else:
            print(Fore.GREEN + Style.BRIGHT + f"\rGet token...              ", end="", flush=True)

            token = get_token(init_data_raw)

            if token:
                token_dict[init_data_raw] = token
                print(Fore.GREEN + Style.BRIGHT + f"\rSuccessfully get token    ", flush=True)
            else:
                print(Fore.RED + Style.BRIGHT + f"\rSwitch to the next account\n\n", flush=True)
                continue  # Proceed to the next iteration if failed to get token


        response = authenticate(token)
   
        ## SAFE TOKEN
        if response.status_code == 200:

            user_data = response.json()
            username = user_data.get('telegramUser', {}).get('username', 'Empty Username')
            firstname = user_data.get('telegramUser', {}).get('firstName', 'Empty')
            lastname = user_data.get('telegramUser', {}).get('lastName', 'Empty')
            
            print(Fore.GREEN + Style.BRIGHT + f"\r\n======[{Fore.WHITE + Style.BRIGHT} {username} | {firstname} {lastname} {Fore.GREEN + Style.BRIGHT}]======")

            # Sync Clicker
            print(Fore.GREEN + f"\rGetting info user...", end="", flush=True)
            response = sync_clicker(token)


            # Initialize logging
            logging.basicConfig(level=logging.INFO, format='%(message)s')

            def log_colored(message, color, style=Style.BRIGHT, end='\n', flush=True):
                logging.info(color + style + message, extra={'end': end, 'flush': flush})

            def check_and_log(response, message):
                if response.status_code == 200:
                    log_colored(message, Fore.GREEN)
                else:
                    log_colored(f"{message} failed", Fore.RED)

            def handle_exchange(clicker_data, token):
                if clicker_data['exchangeId'] is None:
                    log_colored('Setting exchange to OKX..', Fore.GREEN, end="", flush=True)
                    exchange_set = exchange(token)
                    check_and_log(exchange_set, 'Successfully set exchange to OKEx')

            def claim_cipher_if_needed(token, cipher_text, claimed_ciphers):
                if token not in claimed_ciphers:
                    log_colored('Claiming cipher...', Fore.GREEN, end="", flush=True)
                    response = claim_cipher(token, cipher_text)
                    if response.status_code == 200:
                        bonuscoins = response.json()['dailyCipher']['bonusCoins']
                        log_colored(f'Successfully claimed cipher | {bonuscoins} bonus coins', Fore.GREEN)
                        claimed_ciphers.add(token)
                    else:
                        error_info = response.json() if response else {}
                        if error_info.get('error_code') == 'DAILY_CIPHER_DOUBLE_CLAIMED':
                            log_colored('Cipher already claimed', Fore.RED)
                        else:
                            log_colored('Failed to claim cipher', Fore.RED)

            def upgrade_feature_if_needed(token, feature, feature_name):
                log_colored(f'Upgrading {feature_name}...', Fore.GREEN, end="", flush=True)
                upgrade_response = upgrade(token, feature)
                if upgrade_response.status_code == 200:
                    level = upgrade_response.json()['clickerUser']['boosts'][feature]['level']
                    log_colored(f'{feature_name} upgraded to level {level}', Fore.GREEN)
                else:
                    log_colored(f'Failed to upgrade {feature_name}', Fore.RED)

            def list_tasks_if_needed(token, cek_task_dict):
                if token not in cek_task_dict:
                    cek_task_dict[token] = False
                if not cek_task_dict[token]:
                    response = list_tasks(token)
                    cek_task_dict[token] = True
                    if response.status_code == 200:
                        tasks = response.json()['tasks']
                        all_completed = all(task['isCompleted'] or task['id'] == 'invite_friends' for task in tasks)
                        if all_completed:
                            log_colored('All tasks unclaimed', Fore.GREEN)
                        else:
                            for task in tasks:
                                if not task['isCompleted']:
                                    log_colored(f'Claiming {task["id"]}...', Fore.YELLOW, end="", flush=True)
                                    response = check_task(token, task['id'])
                                    if response.status_code == 200 and response.json()['task']['isCompleted']:
                                        log_colored(f'Claimed {task["id"]}', Fore.GREEN)
                                    else:
                                        log_colored(f'Failed to claim {task["id"]}', Fore.RED)
                    else:
                        log_colored('Failed to get task list', Fore.RED)
                else:
                    log_colored('Skipped task list check', Fore.GREEN)

            def process_clicker_data(clicker_data, token, claimed_ciphers, cipher_text, auto_upgrade_energy, auto_upgrade_multitap, cek_task_list, cek_task_dict, auto_upgrade_passive):
                log_colored(f"[ Level ] : {clicker_data['level']}", Fore.YELLOW)
                log_colored(f"[ Total Earned ] : {int(clicker_data['totalCoins'])}", Fore.YELLOW)
                log_colored(f"[ Coin ] : {int(clicker_data['balanceCoins'])}", Fore.YELLOW)
                log_colored(f"[ Energy ] : {clicker_data['availableTaps']}", Fore.YELLOW)
                
                boosts = clicker_data['boosts']
                log_colored(f"[ Level Energy ] : {boosts.get('BoostMaxTaps', {}).get('level', 0)}", Fore.CYAN)
                log_colored(f"[ Level Tap ] : {boosts.get('BoostEarnPerTap', {}).get('level', 0)}", Fore.CYAN)
                log_colored(f"[ Exchange ] : {clicker_data['exchangeId']}", Fore.CYAN)
                log_colored(f"[ Passive Earn ] : {clicker_data['earnPassivePerHour']}\n", Fore.CYAN)
                log_colored("[ Tap Status ] : Tapping ...", Fore.GREEN, end="", flush=True)

                handle_exchange(clicker_data, token)

                response = tap(token, clicker_data['maxTaps'], clicker_data['availableTaps'])
                check_and_log(response, "[ Tap Status ] : Tapped")

                log_colored("[ Checkin Daily ] : Checking...", Fore.GREEN, end="", flush=True)
                time.sleep(1)
                response = claim_daily(token)
                if response.status_code == 200:
                    daily_response = response.json()['task']
                    if daily_response['isCompleted']:
                        log_colored(f"[ Checking Daily ] Days {daily_response['days']} | Completed", Fore.GREEN)
                    else:
                        log_colored(f"[ Checking Daily ] Days {daily_response['days']} | It's not time to claim daily yet", Fore.RED)
                else:
                    log_colored(f"[ Checkin Daily ] Failed daily check {response.status_code}", Fore.RED)

                if ask_cipher == 'y':
                    claim_cipher_if_needed(token, cipher_text, claimed_ciphers)

                if auto_upgrade_energy == 'y':
                    upgrade_feature_if_needed(token, "BoostMaxTaps", "Energy")

                if auto_upgrade_multitap == 'y':
                    upgrade_feature_if_needed(token, "BoostEarnPerTap", "MultiTap")

                if cek_task_list == 'y':
                    list_tasks_if_needed(token, cek_task_dict)

                if auto_upgrade_passive == 'y':
                    log_colored("[ Upgrade Minning ] : Checking...", Fore.GREEN, end="", flush=True)
                    auto_upgrade_passive_earn(token)

            if response.status_code == 200:
                clicker_data = response.json()['clickerUser']
                process_clicker_data(clicker_data, token, claimed_ciphers, cipher_text, auto_upgrade_energy, auto_upgrade_multitap, cek_task_list, cek_task_dict, auto_upgrade_passive)
            else:
                log_colored(f"Failed to get user info {response.status_code}", Fore.RED)



        ## DEAD TOKEN
        elif response.status_code == 401:
            error_data = response.json()
            if error_data.get("error_code") == "NotFound_Session":
                print(Fore.RED + Style.BRIGHT + f"=== [ Token Invalid {token} ] ===")
                token_dict.pop(init_data_raw, None)  # Remove invalid token
                token = None  # Set token to None to get a new token in the next iteration.
            else:
                print(Fore.RED + Style.BRIGHT + "Authentication failed with unknown error")
        else:
            print(Fore.RED + Style.BRIGHT + f"Error with status code: {response.status_code}")
            token = None  #Set token to None if another error occurs
            
        time.sleep(1)

while True:
    auto_upgrade_energy = input("Upgrade Energy (default n) ? (y/n): ").strip().lower()
    if auto_upgrade_energy in ['y', 'n', '']:
        auto_upgrade_energy = auto_upgrade_energy or 'n'
        break
    else:
        print("Enter 'y' or 'n'.")

while True:
    auto_upgrade_multitap = input("Upgrade Multitap (default n) ? (y/n): ").strip().lower()
    if auto_upgrade_multitap in ['y', 'n', '']:
        auto_upgrade_multitap = auto_upgrade_multitap or 'n'
        break
    else:
        print("Enter 'y' or 'n'.")
while True:
    auto_upgrade_passive = input("Auto Upgrade Mining (Passive Earn)? (default n) (y/n): ").strip().lower()
    if auto_upgrade_passive in ['y', 'n', '']:
        auto_upgrade_passive = auto_upgrade_passive or 'n'
        break
    else:
        print("Enter 'y' or 'n'.")

if auto_upgrade_passive == 'y':
    while True:
        lanjut_upgrade = input("Other upgrades if coins are not enough? (default n) (y/n): ").strip().lower()
        if lanjut_upgrade in ['y', 'n', '']:
            lanjut_upgrade = lanjut_upgrade or 'n'
            break
        else:
            print("Enter 'y' or 'n'.")

while True:
    cek_task_list = input("Enable Check Task? (default n) (y/n): ").strip().lower()
    if cek_task_list in ['y', 'n', '']:
        cek_task_list = cek_task_list or 'n'
        break
    else:
        print("Enter 'y' or 'n'.")

while True:
    ask_cipher = input("Auto Claim Cipher Daily / Daily Password? (default n) (y/n): ").strip().lower()
    if ask_cipher in ['y', 'n', '']:
        ask_cipher = ask_cipher or 'n'
        break
    else:
        print("Enter 'y' or 'n'.")

if ask_cipher == 'y':
    while True:
        cipher_text = input("Enter the cipher / daily password : ")
        if cipher_text:
            break
        else:
            print("Enter daily block password!.")

def print_welcome_message():
    print(r"""
          
    _   _      _         
   /_\ | |_ __| |_  __ _ 
  / _ \| | '_ \ ' \/ _` |
 /_/ \_\_| .__/_||_\__,_|
         |_|  
                     
          """)
    print(Fore.GREEN + Style.BRIGHT + "Hamster Kombat Agent!")
    print(Fore.GREEN + Style.BRIGHT + "Update Link: https://github.com/amirsadeghi1/hamster_kombat_agent")
    print(Fore.GREEN + Style.BRIGHT + "Telegram Contact: https://t.me/Amir_017\n")

if __name__ == "__main__":
    main()
