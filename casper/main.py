import requests
import time
import datetime
from colorama import init, Fore, Style

# Initialize colorama for colored terminal output
init(autoreset=True)

# File to load tokens
data_file = "query.txt"

# Function to load tokens from a file
def load_tokens(file_path):
    with open(file_path, 'r') as file:
        tokens = file.read().splitlines()
    return tokens

# Function to get headers with an optional token
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

# Function to login and get user data
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

            # Fetch leaderboard data after login
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

    # Make the request
    response = requests.get(url, headers=headers, params=params)

    # Check if request was successful
    if response.status_code == 200:
        try:
            result = response.json()

            # Extract user rank details
            user_rank = result.get("ranking", {}).get("user_rank", {})

            # Log user points and position
            user_points = user_rank.get("points", 0)
            user_position = user_rank.get("position", "N/A")

            if user_points and user_position:
                print(Fore.GREEN + f"Rank:  [ {user_position} ]")
                print(Fore.GREEN + f"Points: [ {user_points} ]")
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
            
            # Iterate over different task categories
            for category, task_list in tasks.items():
                print(Fore.CYAN + f"\nCategory: {category.capitalize()} Tasks")
                
                # Loop through the tasks in each category
                for task in task_list:
                    task_name = task.get('task_name', 'Unknown Task')
                    task_type = task.get('type', 'Unknown Type')
                    description = task.get('description', 'No description available')
                    priority = task.get('priority', 'No priority info')
                    rewards = task.get('rewards', [])
                    
                    # Extract reward information if available
                    reward_info = ', '.join([f"{reward['unit']}: {reward['value']}" for reward in rewards]) if rewards else 'No rewards'

#                    print(Fore.GREEN + f"Task: {task_name}, Type: {task_type}, Priority: {priority}")
 #                   print(Fore.BLUE + f"Rewards: {reward_info}\n")

        except Exception as e:
            print(Fore.RED + f"Error parsing tasks data: {e}")
    else:
        print(Fore.RED + f"Failed to retrieve tasks, status code: {response.status_code}")

# Function to click a task (action = 0)
def klik_task(token, task_name):
    url = "https://api.cspr.community/api/users/me/tasks"
    headers = get_headers(token)
    payload = {
        "task_name": task_name,
        "action": 0,  # Action 0 to simulate the click
        "data": {
            "date": datetime.datetime.utcnow().isoformat() + "Z"  # ISO 8601 date
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

# Function to claim and clear a task (action = 1)
def clear_task(token, task_name):
    url = "https://api.cspr.community/api/users/me/tasks"
    headers = get_headers(token)
    payload = {
        "task_name": task_name,
        "action": 1,  # Action for clearing the task
        "data": {
            "date": datetime.datetime.utcnow().isoformat() + "Z"  # ISO 8601 date
        }
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        print(Fore.GREEN + f"Sukses Claim Task: [ {task_name} ]")
    else:
        print(Fore.RED + f"Failed to clear task: {task_name}, status code: {response.status_code}")
        print(Fore.RED + f"Response content: {response.content}")

# Example function to automate clicking, claiming, and clearing tasks with a 10-second delay
def auto_clear_tasks(token):
    # Step 1: Get all tasks
    url = "https://api.cspr.community/api/users/me/tasks"
    headers = get_headers(token)
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        try:
            result = response.json()
            tasks = result.get('tasks', {})

            # Step 2: Loop through each task category
            for category, task_list in tasks.items():
                for task in task_list:
                    task_name = task.get('task_name')

                    # Step 3: Click the task (action 0) before attempting to clear
                    if klik_task(token, task_name):
                        # Wait for 10 seconds before clearing the task
                        time.sleep(10)
                        clear_task(token, task_name)

        except Exception as e:
            print(Fore.RED + f"Error during auto task clearing: {e}")
    else:
        print(Fore.RED + f"Failed to retrieve tasks, status code: {response.status_code}")

if __name__ == "__main__":
    tokens = load_tokens(data_file)

    for token in tokens:
        print(Fore.CYAN + "Logging in with token:")
        user_data = login(token)
        
        if user_data:
            print(Fore.CYAN + "Listing tasks for user:")
            list_task(token)

            # Automatically click, claim, and clear tasks with a 10-second delay between each action
            print(Fore.CYAN + "Auto-clearing tasks:")
            auto_clear_tasks(token)

        time.sleep(2)  # Pause between requests to avoid overloading the server

