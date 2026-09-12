# x7va
# NOTE : Spamming Discord's API is against TOS, You may get your account suspended and I am not responsible. For a further caution, use an alt's token and a higher delay.





import random
import string 
import requests
import os
import time
import json
from colorama import Fore,init
import datetime
from configparser import ConfigParser
import sys
from threading import Thread
from concurrent.futures import ThreadPoolExecutor
import re
init(autoreset=True)
__version__ = "x7va"
__github__= "https://github.com/x7va"
dir_path = os.path.dirname(os.path.realpath(__file__))
configur = ConfigParser()
configur.read(os.path.join(dir_path, f"config.ini"))
tokens_list = os.path.join(dir_path, f"tokens.txt")
integ_0 = 0
sys_url = "https://discord.com/api/v9/users/@me"
URL = "https://discord.com/api/v9/users/@me/pomelo-attempt"
CLAIM_URL = "https://discord.com/api/v9/users/@me"
def s_sys_h():
   if configur.getboolean("sys","MULTI_TOKEN") == True:
      return {
    "Content-Type": "Application/json",
    "Orgin": "https://discord.com/",

    "Authorization":avail_tokens(tokens_list)[integ_0]
    }
   elif configur.getboolean("sys","MULTI_TOKEN") == False:
      return{
    "Content-Type": "Application/json",
    "Orgin": "https://discord.com/",

    "Authorization":configur.get("sys","TOKEN")
    }
   else:
      return {
    "Content-Type": "Application/json",
    "Orgin": "https://discord.com/",

    "Authorization":configur.get("sys","TOKEN")
    }
def sys_c_t():
   if configur.get("sys","TOKEN") != "":
      pass
   elif configur.get("sys","TOKEN") == "" and configur.getboolean("sys","MULTI_TOKEN") == False:
        print(f"{Lb}[!]{Fore.RED} No token found. You must paste your token inside the 'config.ini' file, in front of the value 'TOKEN'.")
        exit()
   elif configur.getboolean("sys","MULTI_TOKEN") == True and not avail_tokens(tokens_list)[0]:
       print(f"{Lb}[!]{Fore.RED} No tokens found. You must paste your tokens inside the 'tokens.txt' file.")
       exit()
   elif configur.getboolean("sys","MULTI_TOKEN") is not True and configur.getboolean("sys","MULTI_TOKEN") is not False and configur.get("sys","TOKEN") == "":
       print(f"{Lb}[!]{Fore.RED} Invalid config detected. Please re-check the config file, `config.ini` and your settings.")
       exit()
available_usernames = []
av_list = os.path.join(dir_path, f"available_usernames.txt")
sample_0 = r"_."
Lb = Fore.LIGHTBLACK_EX
Ly = Fore.LIGHTYELLOW_EX
Delay = configur.getfloat("config","default_delay")

# Proxy management
proxies_list = []
proxy_index = 0
use_proxies = False
def setconf():
   global string_0
   global digits_0
   global punctuation_0
   global webhook_0
   #global multi_token_0
   global sat_string
   global sat_digits
   global sat_multi_token
   global sat_punct
   global sat_webhook
   global use_proxies
   sat_webhook = configur.get("sys","WEBHOOK_URL")
   sat_string = configur.getboolean("config","string")
   sat_digits = configur.getboolean("config","digits")
   sat_punct = configur.getboolean("config","punctuation")
   sat_multi_token = configur.getboolean("sys","MULTI_TOKEN")
   if sat_webhook =="":
      webhook_0 = False
   elif sat_webhook !="":
      webhook_0 = True
   if sat_string == True:
      string_0 = string.ascii_lowercase
   elif sat_string == False:
      string_0 = ""
   else:
      string_0 = string.ascii_lowercase
      sat_string = True
   if sat_digits == True:
      digits_0 = string.digits
   elif sat_digits == False:
      digits_0 = ""
   else:
      digits_0 = string.digits
      sat_digits = True
   if sat_punct == True:
      punctuation_0 = sample_0
   elif sat_punct == False:
      punctuation_0 = ""
   else:
      punctuation_0 = sample_0
      sat_punct = True
   if sat_punct == False and sat_digits == False and sat_string == False:
      punctuation_0 = sample_0
      digits_0 = string.digits
      string_0 = string.ascii_lowercase
   
   # Load proxy settings
   use_proxies = configur.getboolean("sys", "USE_PROXIES")
   if use_proxies:
       load_proxies()

def load_proxies():
   """Load proxies from file or scrape them"""
   global proxies_list
   proxy_file = os.path.join(dir_path, "proxies.txt")
   
   # Try to load from file first
   if os.path.exists(proxy_file):
       with open(proxy_file, 'r') as f:
           proxies_list = [line.strip() for line in f if line.strip()]
       print(f"{Lb}[+]{Fore.LIGHTGREEN_EX} Loaded {len(proxies_list)} proxies from proxies.txt")
       return
   
   # If no file, scrape proxies
   print(f"{Lb}[!]{Ly} No proxies.txt found. Scraping proxies...")
   scrape_proxies()

def scrape_proxies():
   """Scrape free proxies from multiple sources"""
   global proxies_list
   sources = [
       "https://www.proxy-list.download/api/v1/get?type=http",
       "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all",
       "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt"
   ]
   
   for source in sources:
       try:
           response = requests.get(source, timeout=10)
           if response.status_code == 200:
               proxies = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d+', response.text)
               proxies_list.extend(proxies)
       except:
           continue
   
   # Remove duplicates
   proxies_list = list(set(proxies_list))
   
   # Save to file
   proxy_file = os.path.join(dir_path, "proxies.txt")
   with open(proxy_file, 'w') as f:
       for proxy in proxies_list:
           f.write(f"{proxy}\n")
   
   print(f"{Lb}[+]{Fore.LIGHTGREEN_EX} Scraped and saved {len(proxies_list)} proxies to proxies.txt")

def validate_proxy(proxy):
   """Validate if a proxy works"""
   try:
       test_url = "http://httpbin.org/ip"
       proxies_dict = {
           "http": f"http://{proxy}",
           "https": f"http://{proxy}"
       }
       response = requests.get(test_url, proxies=proxies_dict, timeout=5)
       return response.status_code == 200
   except:
       return False

def get_next_proxy():
   """Get next proxy from list with rotation"""
   global proxy_index, proxies_list
   if not proxies_list:
       return None
   
   proxy = proxies_list[proxy_index]
   proxy_index = (proxy_index + 1) % len(proxies_list)
   return proxy

def get_proxies_dict(proxy):
   """Convert proxy string to requests dict format"""
   if not proxy:
       return None
   return {
       "http": f"http://{proxy}",
       "https": f"http://{proxy}"
   }

def main():
    sys_c_t()
    # Skip title command on non-Windows systems (Mac/Linux)
    if os.name == 'nt':
        os.system(f"title {__version__} - Connected as {requests.get(sys_url,headers=s_sys_h()).json()['username']}")
    s_sys_h()
    setconf()    
    print(f"""{Fore.LIGHTYELLOW_EX}
════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
  {__version__} - {__github__}
  Connected as {Fore.LIGHTCYAN_EX}{requests.get(sys_url,headers=s_sys_h()).json()['username']}#{requests.get(sys_url,headers=s_sys_h()).json()['discriminator']}{Fore.LIGHTYELLOW_EX}
                            
  {Fore.LIGHTCYAN_EX}1{Fore.LIGHTBLACK_EX}[{Fore.YELLOW}Generate names and check{Fore.LIGHTBLACK_EX}]             
  {Fore.LIGHTCYAN_EX}2{Fore.LIGHTBLACK_EX}[{Fore.YELLOW}Check a specific list{Fore.LIGHTBLACK_EX}]             
  {Fore.LIGHTCYAN_EX}3{Fore.LIGHTBLACK_EX}[{Fore.YELLOW}Schedule username claim{Fore.LIGHTBLACK_EX}]
  
  Config: Digits:{sat_digits} String:{sat_string} Punctuation:{sat_punct} Multi-Token:{sat_multi_token} Webhook:{webhook_0} Delay:{Delay}s
════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
""")
    proc0()
    
def setdelay():
   global Delay
   print(f"{Lb}[!]{Ly} Default delay is: {Delay}s (config.ini){Lb}")
   d_input = input(f"{Lb}[{Ly}Edit Delay (Press Enter to skip){Lb}]:> ")
   if d_input=="" or d_input.isspace():
      return
   else:   
    try:
      int(d_input)
      Delay = int(d_input)
    except ValueError:
      print(f"{Lb}[!]{Fore.RED}Error: You must enter a valid integer. No strings.")
      setdelay()

def proc0():
    m_input = input(f"{Fore.LIGHTBLACK_EX}[{Fore.LIGHTGREEN_EX}DSV{Fore.LIGHTBLACK_EX}]:> {Fore.LIGHTYELLOW_EX}").lower()
    if m_input=="exit":
        sys.exit(0)
    if m_input=="":
        proc0()
    elif m_input=="2":
        setdelay()
        opt2load()
    elif m_input=="1":
       setdelay()
       opt1load()
    elif m_input=="3":
       opt3load()
    else:
        proc0()
def validate_names(opt,usernames):
   global available_usernames
   global integ_0
   if opt == 2:
    for username in usernames:
       body = {
           "username": username
       }
       time.sleep(Delay)
       
       # Get proxy if enabled
       proxy = get_next_proxy() if use_proxies else None
       proxies = get_proxies_dict(proxy)
       
       endpoint = requests.post(URL, headers=s_sys_h(), json=body, proxies=proxies, timeout=10)
       json_endpoint = endpoint.json()
       if endpoint.status_code == 429 and sat_multi_token == True and len(avail_tokens(tokens_list)) != integ_0:
           integ_0 = (integ_0 +1) % len(avail_tokens(tokens_list))
           print(f"{Lb}[!]{Ly} Token {integ_0} went rate limited. Using token index: {integ_0} connected as: {requests.get(sys_url,headers=s_sys_h()).json()['username']}#{requests.get(sys_url,headers=s_sys_h()).json()['discriminator']}")
       elif endpoint.status_code == 429 and sat_multi_token == False:
         sleep_time = endpoint.json()["retry_after"]
         print(f"{Lb}[!]{Fore.RED} Rate limit hit. Sleeping for {sleep_time}s (Discord rate limit)")
         time.sleep(sleep_time)
       if json_endpoint.get("taken") is not None:
           if json_endpoint["taken"] is False:
            print(f"{Lb}[+]{Fore.LIGHTGREEN_EX} '{username}' available.")
            ch_send_webhook(username)
            save(username)
            available_usernames.append(username)
           elif json_endpoint["taken"] is True:
              print(f"{Lb}[-]{Fore.RED} '{username}' taken.")
       else:
           print(f"{Lb}[?]{Fore.RED} Error validating '{username}': {endpoint.json()['message']} |DSV: Make sure you have a valid token.")
   elif opt == 1:
       body = {
           "username": usernames
       }
       
       # Get proxy if enabled
       proxy = get_next_proxy() if use_proxies else None
       proxies = get_proxies_dict(proxy)
       
       endpoint = requests.post(URL, headers=s_sys_h(), json=body, proxies=proxies, timeout=10)
       json_endpoint = endpoint.json()
       if endpoint.status_code == 429 and len(avail_tokens(tokens_list)) != integ_0 and sat_multi_token == True:
           integ_0 = (integ_0 +1) % len(avail_tokens(tokens_list))
           print(f"{Lb}[!]{Ly} Token {integ_0} went rate limited. Using token index: {integ_0} connected as: {requests.get(sys_url,headers=s_sys_h()).json()['username']}#{requests.get(sys_url,headers=s_sys_h()).json()['discriminator']}")
       elif endpoint.status_code == 429 and sat_multi_token == False:
         sleep_time = endpoint.json()["retry_after"]
         print(f"{Lb}[!]{Fore.RED} Rate limit hit. Sleeping for {sleep_time}s (Discord rate limit)")
         time.sleep(sleep_time)
       if json_endpoint.get("taken") is not None:
           if json_endpoint["taken"] is False:
            print(f"{Lb}[+]{Fore.LIGHTGREEN_EX} '{usernames}' available.")
            ch_send_webhook(usernames)
            save(usernames)
            available_usernames.append(usernames)
           elif json_endpoint["taken"] is True:
              print(f"{Lb}[-]{Fore.RED} '{usernames}' taken.")
       else:
           print(f"{Lb}[?]{Fore.RED} Error validating '{usernames}': {endpoint.json()['message']} |DSV: Make sure you have a valid token.")
def avail_tokens(path):
   with open(path, 'r') as at:
        tokens = at.read().splitlines()
   return tokens
def exit():
   try:
       input(f"{Fore.YELLOW}Press Enter to exit.")
   except EOFError:
       pass
   sys.exit(0)
def checkavail(): 
   if len(available_usernames) < 1:
      print(f"{Lb}[!]{Fore.RED} Error: No available usernames found.")
      exit()
   else:
      return
def opt2load():
    global av_list
    global dir_path
    list_path = os.path.join(dir_path, f"usernames.txt")
    print(f"{Lb}[!]{Ly}Checking 'usernames.txt' for a valid list...")
    try:
     with open(list_path) as file:
      usernames = [line.strip() for line in file]
      validate_names(2,usernames)
     checkavail()
     print(f"\n{Lb}[=]{Fore.LIGHTGREEN_EX} Done. {Ly}{len(available_usernames)}{Fore.LIGHTGREEN_EX} Available usernames, are saved in the following file: '{av_list}' .")
     exit()
    except FileNotFoundError:
       print(f"{Lb}[!]{Fore.RED} Error: Couldn't find the list (usernames.txt). Please make sure to create a valid list file in the same directory: \n({dir_path}\\)")
       exit()
def opt1load():
   opt1_input:int = input(f"{Lb}[{Ly}How many letters in a username{Lb}]:> ")
   try:
    int(opt1_input)
    if int(opt1_input) >32 or int(opt1_input) <2:
       print(f"{Lb}[!]{Fore.RED} Error: The username must contain at least 2 letters, and not more than 32 letters.")
       opt1load()
    opt2_input:int = input(f"{Lb}[{Ly}How many usernames to generate{Lb}]:> ")
    opt1func(int(opt2_input),int(opt1_input))
   except ValueError:
      print(f"{Lb}[!]{Fore.RED} Error: You must enter a valid integer. No strings.")
      opt1load()
def save(content):
   with open(av_list, "a") as file:
        file.write(f"\n{content}")
def ch_send_webhook(val0):
   if webhook_0 == True:
    webhook = Discord(url=sat_webhook)
    try:
     webhook.post(
       username="DSV",
       avatar_url="https://cdn.icon-icons.com/icons2/488/PNG/512/search_47686.png",
       embeds=[
    {
      "title": f"Username: `{val0}` is available :white_check_mark:.",
      "timestamp": str(datetime.datetime.utcnow()),
      "footer": {
        "text": "github.com/suenerve/Discord-Username-Checker"
      },
      "author": {
        "name": "DSV - Username Found",
        "url": "https://github.com/suenerve/Discord-Username-Checker",
        "icon_url": "https://cdn-icons-png.flaticon.com/512/5290/5290982.png"
      },
      "thumbnail": {
        "url": "https://raw.githubusercontent.com/suenerve/Discord-Username-Checker/main/images/ignore.png"
      },
      "fields": [],
      "color": 16768000
    }
  ],

    )
    except Exception as s:
       print(f"{Lb}[!]{Fore.RED} Error: Something went wrong while sending the webhook request. Exception: {s} | DSV: Make sure you have a valid webhook URL")
   else:
      return
def opt1func(v1,v2):
   for i in range(v1):
    name = get_names(int(v2))
    validate_names(1,name)
    time.sleep(Delay)
   checkavail()
   print(f"\n{Lb}[=]{Fore.LIGHTGREEN_EX} Done. {Ly}{len(available_usernames)}{Fore.LIGHTGREEN_EX} Available usernames, are saved in the following file: '{av_list}' .")
   exit()

def opt3load():
   """Option 3: Schedule a username claim for a specific time"""
   print(f"{Lb}[!]{Ly} Schedule Username Claim")
   username_input = input(f"{Lb}[{Ly}Enter username to claim{Lb}]:> ")
   time_input = input(f"{Lb}[{Ly}Enter target time (YYYY-MM-DD HH:MM:SS){Lb}]:> ")
   
   if not username_input or not time_input:
       print(f"{Lb}[!]{Fore.RED} Username and time are required.")
       return
   
   # Check if password is configured
   password = configur.get("sys", "PASSWORD")
   if not password or password == "":
       print(f"{Lb}[!]{Fore.RED} Password not configured in config.ini. Please add your PASSWORD.")
       return
   
   print(f"{Lb}[!]{Ly} Starting scheduled claim thread...")
   # Run in a separate thread so it doesn't block the main menu
   claim_thread = Thread(target=schedule_claim, args=(username_input, time_input))
   claim_thread.daemon = True
   claim_thread.start()
   
   print(f"{Lb}[+]{Fore.LIGHTGREEN_EX} Claim scheduled. Press Enter to return to menu...")
   input()
def get_names(length: int) ->str:
   return ''.join(random.sample(string_0 + digits_0 + punctuation_0, length))

def claim_username(username):
   """Claim a username using the Discord API with password authentication"""
   global integ_0
   password = configur.get("sys", "PASSWORD")
   if not password or password == "":
       print(f"{Lb}[!]{Fore.RED} Password not configured in config.ini")
       return False
   
   body = {
       "username": username,
       "password": password
   }
   
   # Get proxy if enabled
   proxy = get_next_proxy() if use_proxies else None
   proxies = get_proxies_dict(proxy)
   
   try:
       response = requests.patch(CLAIM_URL, headers=s_sys_h(), json=body, proxies=proxies, timeout=10)
       if response.status_code == 200:
           print(f"{Lb}[+]{Fore.LIGHTGREEN_EX} Successfully claimed username: '{username}'")
           ch_send_webhook(username)
           return True
       elif response.status_code == 429:
           if sat_multi_token == True and len(avail_tokens(tokens_list)) > integ_0:
               integ_0 = (integ_0 + 1) % len(avail_tokens(tokens_list))
               print(f"{Lb}[!]{Ly} Token rate limited. Switching to token index: {integ_0}")
               return claim_username(username)
           else:
               sleep_time = response.json().get("retry_after", 1)
               print(f"{Lb}[!]{Fore.RED} Rate limit hit while claiming. Sleeping for {sleep_time}s")
               time.sleep(sleep_time)
               return claim_username(username)
       else:
           print(f"{Lb}[!]{Fore.RED} Failed to claim username: '{username}'. Status: {response.status_code}")
           print(f"{Lb}[!]{Fore.RED} Response: {response.text}")
           return False
   except Exception as e:
       print(f"{Lb}[!]{Fore.RED} Error claiming username: {e}")
       return False

def schedule_claim(username, target_time_str):
   """Schedule a username claim for a specific time (exact to the second)"""
   try:
       # Parse the target time (format: YYYY-MM-DD HH:MM:SS)
       target_time = datetime.datetime.strptime(target_time_str, "%Y-%m-%d %H:%M:%S")
       current_time = datetime.datetime.now()
       
       if target_time <= current_time:
           print(f"{Lb}[!]{Fore.RED} Target time must be in the future!")
           return False
       
       delay_seconds = (target_time - current_time).total_seconds()
       print(f"{Lb}[!]{Ly} Scheduled claim for '{username}' at {target_time_str}")
       print(f"{Lb}[!]{Ly} Waiting {delay_seconds:.2f} seconds...")
       
       # Wait until the exact second
       time.sleep(delay_seconds)
       
       # Claim the username
       return claim_username(username)
   except ValueError:
       print(f"{Lb}[!]{Fore.RED} Invalid time format. Use: YYYY-MM-DD HH:MM:SS")
       return False
# Source of this class: https://github.com/10mohi6/discord-webhook-python/blob/master/discordwebhook/discordwebhook.py
class Discord:
    def __init__(self, *, url):
        self.url = url
    def post(
        self,
        *,
        content=None,
        username=None,
        avatar_url=None,
        tts=False,
        file=None,
        embeds=None,
        allowed_mentions=None
    ):
        if content is None and file is None and embeds is None:
            raise ValueError("required one of content, file, embeds")
        data = {}
        if content is not None:
            data["content"] = content
        if username is not None:
            data["username"] = username
        if avatar_url is not None:
            data["avatar_url"] = avatar_url
        data["tts"] = tts
        if embeds is not None:
            data["embeds"] = embeds
        if allowed_mentions is not None:
            data["allowed_mentions"] = allowed_mentions
        if file is not None:
            return requests.post(
                self.url, {"payload_json": json.dumps(data)}, files=file
            )
        else:
            return requests.post(
                self.url, json.dumps(data), headers={"Content-Type": "application/json"}
            )
if __name__ == "__main__":
    main()
