import requests
import time
import datetime
from colorama import init, Fore, Style

init(autoreset=True)

data_file = "query.txt"

def load_tokens(file_path):
    with open(file_path, 'r') as file:
        tokens = file.read().splitlines()
    return tokens

def print_welcome_banner():
    banner = """
   ▄   ██▄      ▄▄▄▄▄       ▄████  ▄█     ▄   ▄███▄   
    █  █  █    █     ▀▄     █▀   ▀ ██      █  █▀   ▀  
██   █ █   █ ▄  ▀▀▀▀▄       █▀▀    ██ █     █ ██▄▄    
█ █  █ █  █   ▀▄▄▄▄▀        █      ▐█  █    █ █▄   ▄▀ 
█  █ █ ███▀                  █      ▐   █  █  ▀███▀   
█   ██                        ▀          █▐           
                                         ▐            
    """
    print(Fore.BLUE + Style.BRIGHT + banner)
    banner2 = "BOT AUTO CLEAR TASK CASPER"
    print(Fore.YELLOW + Style.BRIGHT + banner2)
    banner3 = "Support surya"
    print(Fore.YELLOW + Style.BRIGHT + banner3)
    banner4 = "0x0FbFC8dBB6e238dFdA2ee70ecee3AC9855777451"
    print(Fore.RED + Style.BRIGHT + banner4)

def get_headers(token=None):
    headers = {
        "Accept": "application/json",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Origin": "https://webapp.cspr.community",
        "Referer": "https://webapp.cspr.community/",
        "Sec-Ch-Ua": "\"Not-A.Brand\";v=\"99\", \"Chromium\";v=\"124\"",
        "Sec-Ch-Ua-Mobile": "?1",
        "Sec-Ch-Ua-Platform": "\"Android\"",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36"
    }
    return headers

def login(token):
    url = "https://api.cspr.community/api/users/me"
    headers = get_headers(token)
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        try:
            result = response.json()
            user_data = result.get('user', {})
            wallet = user_data.get('wallet', {})
            user_name = user_data.get('username', 'Unknown Name')

            print(Fore.YELLOW + Style.BRIGHT + f"Account: [ {user_name} ]")

            fetch_leaderboard(token)

            return user_data
        except Exception as e:
            print(Fore.RED + f"Error parsing user data: {e}")
    else:
        print(Fore.RED + f"Failed to login, status code: {response.status_code}")

def fetch_leaderboard(token):
    url = "https://api.cspr.community/api/airdrop-info?leaderboard_offset=0&leaderboard_limit=3"
    headers = get_headers(token)
    params = {
        "leaderboard_offset": 0,
        "leaderboard_limit": 3
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        try:
            result = response.json()

            user_rank = result.get("ranking", {}).get("user_rank", {})

            user_points = user_rank.get("points", 0)
            user_position = user_rank.get("position", "N/A")

            if user_points and user_position:
                print(Fore.GREEN + f"Point: [ {user_points} ]")
                print(Fore.GREEN + f"Rank:  [ {user_position} ]")
            else:
                print(Fore.RED + "User rank information is missing or incomplete.")

        except Exception as e:
            print(Fore.RED + f"Error parsing leaderboard data: {e}")
    else:
        print(Fore.RED + f"Failed to retrieve leaderboard, status code: {response.status_code}")

def list_task(token):
    url = "https://api.cspr.community/api/users/me/tasks"
    headers = get_headers(token)
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        try:
            result = response.json()
            tasks = result.get('tasks', {})
            
            for category, task_list in tasks.items():
                print(Fore.CYAN + f"\nCategory: {category.capitalize()} Tasks")
                
                for task in task_list:
                    task_name = task.get('task_name', 'Unknown Task')
                    task_type = task.get('type', 'Unknown Type')
                    description = task.get('description', 'No description available')
                    priority = task.get('priority', 'No priority info')
                    rewards = task.get('rewards', [])
                    seconds_to_allow_claim = task.get('seconds_to_allow_claim', 0)

                    reward_info = ', '.join([f"{reward['unit']}: {reward['value']}" for reward in rewards]) if rewards else 'No rewards'

#                    print(Fore.GREEN + f"Task: {task_name}, Type: {task_type}, Priority: {priority}, Allow Claim After: {seconds_to_allow_claim} seconds")
#                    print(Fore.BLUE + f"Rewards: {reward_info}\n")

        except Exception as e:
            print(Fore.RED + f"Error parsing tasks data: {e}")
    else:
        print(Fore.RED + f"Failed to retrieve tasks, status code: {response.status_code}")

def klik_task(token, task_name):
    url = "https://api.cspr.community/api/users/me/tasks"
    headers = get_headers(token)
    payload = {
        "task_name": task_name,
        "action": 0,
        "data": {
            "date": datetime.datetime.utcnow().isoformat() + "Z"
        }
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        print(Fore.YELLOW + f"Submit Task [ {task_name} ]")
        return True
    else:
        print(Fore.RED + f"Failed to click task: {task_name}, status code: {response.status_code}")
        print(Fore.RED + f"Response content: {response.content}")
        return False

def clear_task(token, task_name):
    url = "https://api.cspr.community/api/users/me/tasks"
    headers = get_headers(token)
    payload = {
        "task_name": task_name,
        "action": 1,
        "data": {
            "date": datetime.datetime.utcnow().isoformat() + "Z"
        }
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        print(Fore.GREEN + f"Sukses Claim Task: [ {task_name} ]")
    else:
        print(Fore.RED + f"Failed to clear task: {task_name}, status code: {response.status_code}")
        print(Fore.RED + f"Response content: {response.content}")

def auto_clear_tasks(token):
    url = "https://api.cspr.community/api/users/me/tasks"
    headers = get_headers(token)
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        try:
            result = response.json()
            tasks = result.get('tasks', {})

            for category, task_list in tasks.items():
                for task in task_list:
                    task_name = task.get('task_name')
                    seconds_to_allow_claim = task.get('seconds_to_allow_claim', 0)  # Get seconds_to_allow_claim

                    if klik_task(token, task_name):
#                        print(Fore.CYAN + f"Waiting for {seconds_to_allow_claim} seconds before clearing task: {task_name}...")
                        for remaining in range(seconds_to_allow_claim, 0, -1):
                            print(Fore.YELLOW + f"Time remaining: {remaining} seconds", end='\r')  # Print remaining time
                            time.sleep(1)  # Sleep for 1 second

                        print()  # Move to the next line after countdown
                        clear_task(token, task_name)

        except Exception as e:
            print(Fore.RED + f"Error during auto task clearing: {e}")
    else:
        print(Fore.RED + f"Failed to retrieve tasks, status code: {response.status_code}")

if __name__ == "__main__":
    print_welcome_banner()

    tokens = load_tokens(data_file)

    for token in tokens:
        print(Fore.CYAN + "Berhasil login:")
        user_data = login(token)
        
        if user_data:
            print(Fore.CYAN + "List Task:")
            list_task(token)

            print(Fore.CYAN + "Claim Task tasks:")
            auto_clear_tasks(token)

        time.sleep(2)  # Pause between requests to avoid overloading the server

