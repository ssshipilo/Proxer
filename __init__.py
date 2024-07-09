import os
import requests
import threading
import linecache
from colorama import Fore
import random
from concurrent.futures import ThreadPoolExecutor, as_completed
from json import loads
from requests import get
from bs4 import BeautifulSoup
from os import system
from sys import platform
import json
import concurrent.futures
import time

cls = lambda: system("cls") if platform in ["win32", "cygwin"] else system("clear")
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'} # Be sure to add a browser header to bypass protection
_blacklisted = ['IP address', 'Port', 'Country, City', '<td class="speed_col">Speed</td>', 'Type', 'Anonymity', 'Latest update']
_connection_protocol = ["HTTP", "HTTPS", "SOCKS4", "SOCKS5"]
_anonymity_type = ["High", "Average", "Low", "no"]
_protocol_addons = {"HTTP": "h", "HTTPS": "s", "SOCKS4": "4", "SOCKS5": "5"} 
_anonymity_addons = {"High": "4", "Average": "3", "Low": "2", "no": "1"}

class proxy_scraper:

    class proxyscrape:
        def request():
            url = f"https://api.proxyscrape.com/v3/free-proxy-list/get?request=displayproxies&proxy_format=protocolipport&format=text&timeout=2000"
            request = get(url, headers=headers)
            return request 
        def sort(request) -> dict:
            api_data = request.text
            result = []
            for i in api_data.split("\r\n"):
                if str(i.split(":")).strip() != "":
                    try: result.append({"address": str(i.split(":")[1]).replace("//", ""), "port": i.split(":")[2], "protocol": i.split(":")[0]})
                    except IndexError:...
            return result
    
    class free_proxy_list:
        def request():
            """This function doing request to free proxy list"""
            url = "https://free-proxy-list.net/"
            request = get(url, headers=headers)
            return request
        def sort(request) -> dict:
            """This function using request and converts it to dict"""
            soup = BeautifulSoup(request.text, 'html.parser')
            all = soup.find_all('td')
            result_item = {}
            result = []
            for i in all:
                i = str(i)
                if "<td>" in i:
                    i = i.replace("<td>", "").replace("</td>", "") # Remove the opening and closing HTML tags <td> and </td>.
                if i.replace(".", "").isdigit() and len(i) > 5:
                    result_item["address"] = i
                elif i.isdigit():
                    result_item["port"] = i
                else:
                    if result_item != {}:
                        result_item["protocol"] = "HTTP"
                        result.append(result_item)
                    result_item = {}
            return result
        
    class hidemyname:
        def request(page: int=1):
            """This function makes a request and returns a response from the resource"""
            url_prefix = "" # Used for content filtering and other results. In essence, it is an expanded capability to produce results
            d = 64 # Progression difference
            if page > 2: # NOTE: Change this > to this >=
                a = d*(page-1) # Calculate the required term of the progression using the formula
                url_prefix = f"?start={str(a)}#list" # Adding the result to the link prefix
            elif page == 2: # NOTE: I know that this is the same as above, it is important to remove in the future
                url_prefix = f"?start={str(d)}#list" # Add at once the difference of the progression

            url = "https://hidemy.name/en/proxy-list/" + url_prefix
            
            request = get(url, headers=headers)
            return request
        def sort(request) -> dict:
            """This function converts the query result into a conveniently readable dictionary"""
            soup = BeautifulSoup(request.text, 'html.parser')
            all = soup.find_all('td')
            result = [] # This list will be returned by this function
            result_item = {} # One specific item will be stored here
            for i in all:
                i = str(i)
                if "<td>" in i:
                    i = i.replace("<td>", "").replace("</td>", "") # Remove the opening and closing HTML tags <td> and </td>.
                if i not in _blacklisted and "div" not in i: # Remove blocked words (watch src/config.py)
                    if "." in i: # This is the IP address
                        result_item["address"] = i
                    if i.isdigit(): # It's a port.
                        result_item["port"] = i
                    if i in _anonymity_type: # This is the anonymity of the connection
                        result_item["anonymity"] = i
                    elif "protocol" not in result_item:
                        if i in _connection_protocol: # It's protocol.
                            result_item["protocol"] = i
                    else:
                        if result_item != {}:
                            result.append(result_item)
                        result_item = {}
            return result

    class geonode():

        def request():
            request = proxy_scraper.proxyscrape.request()
            all_data = proxy_scraper.proxyscrape.sort(request)
            try:
                response = requests.get(f"https://proxylist.geonode.com/api/proxy-list?limit=500&page=1&sort_by=lastChecked&sort_type=desc", headers=headers)
                response.raise_for_status()
            except Exception as e:
                print(f"Failed to get initial data: {e}")
                return
            api_data = response.json()
            proxies = all_data
            page = 1
            limit = 500
            total = api_data['total']
            collected_data = []
            result = []
            while len(collected_data) < total:
                try:
                    response = requests.get(
                        f"https://proxylist.geonode.com/api/proxy-list?limit={limit}&page={page}&sort_by=lastChecked&sort_type=desc",
                        # proxies=proxies_dict,
                        headers=headers,
                        timeout=5
                    )
                    response.raise_for_status()
                    data = response.json()
                    collected_data.extend(data['data'])
                    for i in data['data']:
                        result.append({"address": i["ip"], "port": i["port"], "protocol": i["protocols"], "city": i["city"], "last_update": i["updated_at"]})
                    if len(collected_data) >= total:
                        break
                    time.sleep(1)
                    page += 1
                except Exception as e:
                    print(f"Proxy failed: {e}")
                    continue

            return result

def update_proxy_list(mode="all"):
    """
    Mode:
        hidemyname - scrape https://hidemy.name/en/proxy-list/
        free_proxy_list - scrape https://free-proxy-list.net/
        proxyscrape - scrape https://proxyscrape.com/
    """

    output = []

    if mode == "hidemyname" or mode == "all":
        try:
            output_arr = []
            for d in range(1, 15):
                request = proxy_scraper.hidemyname.request(page=d)
                result = proxy_scraper.hidemyname.sort(request=request)
                for i in result:
                    output_arr.append(i)
            output.extend(output_arr)
        except:...
        
    if mode == "free_proxy_list" or mode == "all":
        try:
            request = proxy_scraper.free_proxy_list.request()
            result = proxy_scraper.free_proxy_list.sort(request)
            
            output.extend(result)
        except:...

    if mode == "proxyscrape" or mode == "all":
        try:
            request = proxy_scraper.proxyscrape.request()
            result = proxy_scraper.proxyscrape.sort(request)

            output.extend(result)
        except:...

    if mode == "geonode" or mode == "all":
        try:
            result = proxy_scraper.geonode.request()

            output.extend(result)
        except:...
    
    return output
    
#! code section END

class Proxer():
    def __init__(self, file_path_output=os.path.join(os.getcwd(), 'output.txt'), file_path_save=os.path.join(os.getcwd(), 'save.txt'), check_services=["https://www.google.com/", "https://www.microsoft.com/", "https://www.apple.com/", "https://www.amazon.com/", "https://www.facebook.com/", "https://www.twitter.com/","https://www.yahoo.com/","https://www.netflix.com/","https://www.linkedin.com/","https://www.bing.com/","https://www.adobe.com/","https://www.samsung.com/"]) -> None:
        self.file_path_save = file_path_save
        self.file_path_output = file_path_output
        self.check_services = check_services
        self.update_proxies = []
        
    def __save_proxies(self, proxy, path):
        """
        Saving the proxy to a file
        `path` (optional) - path to the file where to save the list of working proxies
        """
        with open(path, "a") as file:
            file.write(proxy + "\n")
        
    def __count_lines(self, filename):
        with open(filename, 'r') as f:
            return sum(1 for _ in f)
    
    def __check_proxy_bool(self, proxy):
        try:
            url_index = random.randint(0, len(self.check_services)-1)
            response = requests.get(self.check_services[url_index], proxies={"http": proxy, "https": proxy}, timeout=3)
            if response.status_code == 200:
                return proxy
        except:
            pass
        return None
    
    def parse(self, path="", returned_array=False):
        """
        `params`: path -  Path to the file where the proxy list will be written. Important!\n
        This is just a list, in order to check this list for operability, use the update_db_proxy() function.\n
        
        ### Make parsing of popular providers:\n
        hidemyname - scrape https://hidemy.name/en/proxy-list/\n
        free_proxy_list - scrape https://free-proxy-list.net/\n
        proxyscrape - scrape https://proxyscrape.com/\n

        """
        counter = 0
        existing_proxies = set()

        if path == "":
            path = self.file_path_output

        if os.path.exists(path):
            with open(path, 'r') as f:
                existing_proxies = set(line.strip() for line in f)

        def add_proxies(proxy_list):
            nonlocal counter 
            for item in proxy_list:
                try:
                    if item["protocol"]:
                        if isinstance(item["protocol"], list):
                            proxy = str(item["protocol"][0]).lower() + "://" + item["address"] + ":" + item["port"]
                        else:
                            proxy = str(item["protocol"]).lower() + "://" + item["address"] + ":" + item["port"]
                    else:
                        proxy = item["address"] + ":" + item["port"]
                    if proxy and proxy not in existing_proxies:
                        with open(path, 'a') as f:
                            f.write(proxy + "\n")
                        existing_proxies.add(proxy)
                        counter += 1
                except:
                    continue
        
        #! --- PROVIDERS ---
        add_proxies(update_proxy_list(mode="hidemyname"))
        add_proxies(update_proxy_list(mode="free_proxy_list"))
        add_proxies(update_proxy_list(mode="proxyscrape"))
        add_proxies(update_proxy_list(mode="geonode"))

        if counter == 0:
            print(Fore.GREEN + "[FREE PROXY]" + Fore.WHITE + " You have the latest up-to-date proxies")
        else:
            print(Fore.GREEN + "[FREE PROXY]" + Fore.WHITE + " New proxy servers have been found:", counter)
        
        if returned_array == True:
            return list(existing_proxies)
        else:
            return True

    def check_proxy(self, proxy):
        """
        Checking proxy performance
        """
        pr = proxy
        proxy = proxy.replace("https://", "")
        proxy = proxy.replace("http://", "")
        proxy = proxy.strip()
        try:
            url_index = random.randint(0, len(self.check_services) - 1)
            start_time = time.time()
            response = requests.get(self.check_services[url_index], proxies={"http": proxy, "https": proxy}, timeout=3)
            end_time = time.time()
            response_time = end_time - start_time
            
            if response.status_code == 200:
                print(Fore.GREEN + "[Working]  " + Fore.WHITE + f"{proxy} - Response time: {response_time:.2f} seconds")
                self.update_proxies.append(f"{pr},{response_time:.2f} sec.")
                return True
            else:
                print(Fore.RED + "[Not Working]  " + Fore.WHITE + f"{proxy} - Response time: {response_time:.2f} seconds")
                return False
        except requests.RequestException as e:
            end_time = time.time()
            response_time = end_time - start_time
            print(Fore.RED + "[Failed]  " + Fore.WHITE + f"{proxy} - Response time: {response_time:.2f} seconds - Error: {e}")
            return False
    
    def update_db_proxy(self, path="", file=False):
        """
        Updating the database of working proxy addresses\n
        `path` (optional) - path to the list of sparser proxies\n
        `file`: 
            True - from your file\n
            False - (default) - make parsing of known services with proxy
        """

        if path == "":
            path = self.file_path_output

        if file:
            if not os.path.exists(path):
                raise FileNotFoundError("[ERROR] There is no file at this path")
        else:
            self.parse()

        with open(path, "r") as file:
            proxies = [line.strip() for line in file.readlines()]
        
        start_time = time.time()
        with concurrent.futures.ThreadPoolExecutor(max_workers=9000) as executor:
            future_to_proxy = {executor.submit(self.check_proxy, proxy): proxy for proxy in proxies}
            working_proxies = []
            for future in concurrent.futures.as_completed(future_to_proxy):
                proxy = future_to_proxy[future]
                try:
                    result = future.result()
                    if result:
                        working_proxies.append(result)
                except Exception as exc:
                    print(f"Proxy {proxy} generated an exception: {exc}")

        end_time = time.time()
        print(f"Checked {len(proxies)} proxies in {end_time - start_time:.2f} seconds.")

        if len(self.update_proxies) > 0:
            for proxy in self.update_proxies:
                with open(self.file_path_save, 'a') as f:
                    f.write(proxy + "\n")
        
    def get(self, count=1) -> []:
        """
        Get a free working proxy
        """
        if not os.path.exists(self.file_path_save):
            raise FileNotFoundError(Fore.RED + "[ERROR] There is no file at this path" + Fore.RESET)

        total_lines = self.__count_lines(self.file_path_save)
        if total_lines == 0:
            print(Fore.RED + "[FREE PROXY][ERROR] Your proxy database is empty.")
            print(Fore.GREEN + "[FREE PROXY]" + Fore.WHITE + " But I made sure you got a proxy anyway. Trying to find a proxy ...")
            proxys = self.parse(returned_array=True)
            if not proxys:
                try:
                    raise Exception(Fore.RED + "[FREE PROXY][ERROR] Your file does not contain proxy addresses, please use the Proxer.update_db_proxy() function.")
                except Exception as e:
                    print(e)
                    return None
                
            print(Fore.GREEN + "[FREE PROXY]" + Fore.WHITE + " Check the found proxies for their ability to work")

            proxy_list = set()
            with ThreadPoolExecutor(max_workers=min(10, len(proxys))) as executor:
                proxies_to_check = random.sample(proxys, min(10, len(proxys)))
                while len(proxy_list) < count:
                    futures = {executor.submit(self.__check_proxy_bool, proxy) for proxy in proxies_to_check}
                    for future in as_completed(futures):
                        proxy = future.result()
                        if proxy:
                            proxy_list.add(proxy)
                        if len(proxy_list) >= count:
                            break
                    if len(proxy_list) < count:
                        proxies_to_check = random.sample(proxys, min(10, len(proxys)))
            if len(proxy_list) > 0:
                print(Fore.GREEN + "[FREE PROXY]" + Fore.WHITE + " But I will remind you that you should use the " + Fore.YELLOW + "update_db_proxy()" + Fore.WHITE + " function to replenish the database of proxy servers", proxy_list)
                return list(proxy_list)
            else:
                try:
                    raise Exception(Fore.RED + "[FREE PROXY][ERROR] Your file does not contain proxy addresses, please use the Proxer.update_db_proxy() function.")
                except Exception as e:
                    print(e)
                    return None

        proxy_list = set()
        print(Fore.GREEN + "[FREE PROXY]" + Fore.WHITE + " We look for a working proxy that Google will let through, this takes up to 5 seconds on average")
        with ThreadPoolExecutor(max_workers=10) as executor:
            while len(proxy_list) < count:
                futures = {executor.submit(self.__check_proxy_bool, linecache.getline(self.file_path_save, random.randint(0, total_lines - 1)).strip()) for _ in range(10)}
                for future in as_completed(futures):
                    proxy = future.result()
                    if proxy:
                        proxy_list.add(proxy)
                    if len(proxy_list) >= count:
                        break

        return list(proxy_list)
    
    def clear_db(self, mode=None, path_output=None, path_save=None):
        """
        Cleaning of databases, verified and unverified proxies
        
        mode: 
            `output` - You want to clean the database of only unverified proxies\n
            `save` - You want to clear the database of only verified proxies\n
        """

        if path_output == None:
            path_output = self.file_path_output
        if path_save == None:
            path_save = self.file_path_save

        if mode == None:
            if os.path.exists(path_output):
                os.remove(path_output)
                print(Fore.GREEN + "[FREE PROXY]" + Fore.WHITE + " Successfully deleted unverified proxy database")

            if os.path.exists(path_save):
                os.remove(path_save)
                print(Fore.GREEN + "[FREE PROXY]" + Fore.WHITE + " Successfully deleted the database of verified proxies")
        else:
            if mode == "output":
                if os.path.exists(path_output):
                    os.remove(path_output)
                    print(Fore.GREEN + "[FREE PROXY]" + Fore.WHITE + " Successfully deleted unverified proxy database")
            elif mode == "save":
                if os.path.exists(path_save):
                    os.remove(path_save)
                    print(Fore.GREEN + "[FREE PROXY]" + Fore.WHITE + " Successfully deleted the database of verified proxies")
            else:
                try:
                    raise Exception(Fore.RED + "[FREE PROXY][ERROR] You have entered the mode parameter incorrectly, read the documentation")
                except Exception as e:
                    print(e)
                    return None

if __name__ == "__main__":
    proxy = Proxer(check_services=["https://www.google.com/"])
    
    # Parsing of new proxies, with uniqueization, if you already have this proxy, it will not add it to the file again
    print(proxy.parse("./test.txt"))

    # Update the proxy list
    proxy.update_db_proxy("./test.txt", True)

    # Get a working proxy
    # print(proxy.get(100))

    # Check proxy
    # print(proxy.check_proxy("216.80.39.89:3129"))

    # Clear DB
    # proxy.clear_db()


# const screenProxy = new Proxy(screen, {
#     get(target, prop) {
#         if (prop === 'width') return 666;
#         if (prop === 'availWidth') return 666;
#         if (prop === 'height') return "Zalupa";
#         if (prop === 'availHeight') return "Zalupa";
#         return target[prop];
#     }
# });

# window.screen = screenProxy;