import os
import requests
import threading
import linecache
from colorama import Fore
import random
from proxy_grab.main import update_proxy_list # Author code: https://github.com/rodukov/proxyGrab/tree/main
from concurrent.futures import ThreadPoolExecutor, as_completed

class Proxer():

    def __init__(self, file_path_output=os.path.join(os.getcwd(), 'output.txt'), file_path_save=os.path.join(os.getcwd(), 'save.txt')) -> None:
        self.file_path_save = file_path_save
        self.file_path_output = file_path_output
        self.check_services = ["https://www.google.com/", "https://www.microsoft.com/", "https://www.apple.com/", "https://www.amazon.com/", "https://www.facebook.com/", "https://www.twitter.com/","https://www.yahoo.com/","https://www.netflix.com/","https://www.linkedin.com/","https://www.bing.com/","https://www.adobe.com/","https://www.samsung.com/"]
        
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
                    proxy = item["address"] + ":" + item["port"]
                    if proxy and proxy not in existing_proxies:
                        with open(path, 'a') as f:
                            f.write(proxy + "\n")
                        existing_proxies.add(proxy)
                        counter += 1
                except:
                    continue

        add_proxies(update_proxy_list(mode="hidemyname"))
        add_proxies(update_proxy_list(mode="free_proxy_list"))
        add_proxies(update_proxy_list(mode="proxyscrape"))

        if counter == 0:
            print(Fore.GREEN + "[PROXER]" + Fore.WHITE + " You have the latest up-to-date proxies")
        else:
            print(Fore.GREEN + "[PROXER]" + Fore.WHITE + " New proxy servers have been found:", counter)
        
        if returned_array == True:
            return list(existing_proxies)
        else:
            return True

    def check_proxy(self, proxy, _class=False):
        """
        Checking proxy performance
        """
        
        proxy = proxy.replace("https://", "")
        proxy = proxy.replace("http://", "")
        proxy = proxy.strip()
        try:
            url_index = random.randint(0, len(self.check_services)-1)
            response = requests.get(self.check_services[url_index], proxies={"http": proxy, "https": proxy}, timeout=10)
            if response.status_code == 200:
                print( Fore.GREEN + "[Working]  " + Fore.WHITE + f"{proxy}")
                if _class == True:
                    self.__save_proxies(proxy, self.file_path_save)
                return True
            else:
                return False
        except:
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

        if file == True:
            if not os.path.exists(path):
                raise FileNotFoundError(Fore.RED + "[ERROR] There is no file at this path")
        else:
            self.parse()

        with open(path, "r") as file:
            proxies = file.readlines()

        threads = []
        for proxy in proxies:
            thread = threading.Thread(target=self.check_proxy, args=[proxy, True])
            thread.start()
            threads.append(thread)
        for thread in threads:
            thread.join()

    def get(self, count=1) -> []:
        """
        Get a free working proxy
        """
        if not os.path.exists(self.file_path_save):
            raise FileNotFoundError(Fore.RED + "[ERROR] There is no file at this path")

        total_lines = self.__count_lines(self.file_path_save)
        if total_lines == 0:
            print(Fore.RED + "[PROXER][ERROR] Your proxy database is empty.")
            print(Fore.GREEN + "[PROXER]" + Fore.WHITE + " But I made sure you got a proxy anyway. Trying to find a proxy ...")
            proxys = self.parse(returned_array=True)
            if not proxys:
                try:
                    raise Exception(Fore.RED + "[PROXER][ERROR] Your file does not contain proxy addresses, please use the Proxer.update_db_proxy() function.")
                except Exception as e:
                    print(e)
                    return None
                
            print(Fore.GREEN + "[PROXER]" + Fore.WHITE + " Check the found proxies for their ability to work")

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
                print(Fore.GREEN + "[PROXER]" + Fore.WHITE + " But I will remind you that you should use the " + Fore.YELLOW + "update_db_proxy()" + Fore.WHITE + " function to replenish the database of proxy servers", proxy_list)
                return list(proxy_list)
            else:
                try:
                    raise Exception(Fore.RED + "[PROXER][ERROR] Your file does not contain proxy addresses, please use the Proxer.update_db_proxy() function.")
                except Exception as e:
                    print(e)
                    return None

        proxy_list = set()
        print(Fore.GREEN + "[PROXER]" + Fore.WHITE + " We look for a working proxy that Google will let through, this takes up to 5 seconds on average")
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
                print(Fore.GREEN + "[PROXER]" + Fore.WHITE + " Successfully deleted unverified proxy database")

            if os.path.exists(path_save):
                os.remove(path_save)
                print(Fore.GREEN + "[PROXER]" + Fore.WHITE + " Successfully deleted the database of verified proxies")
        else:
            if mode == "output":
                if os.path.exists(path_output):
                    os.remove(path_output)
                    print(Fore.GREEN + "[PROXER]" + Fore.WHITE + " Successfully deleted unverified proxy database")
            elif mode == "save":
                if os.path.exists(path_save):
                    os.remove(path_save)
                    print(Fore.GREEN + "[PROXER]" + Fore.WHITE + " Successfully deleted the database of verified proxies")
            else:
                try:
                    raise Exception(Fore.RED + "[PROXER][ERROR] You have entered the mode parameter incorrectly, read the documentation")
                except Exception as e:
                    print(e)
                    return None

if __name__ == "__main__":
    proxy = Proxer()
    
    # Parsing of new proxies, with uniqueization, if you already have this proxy, it will not add it to the file again
    # print(proxy.parse("./test.txt"))

    # Update the proxy list
    # proxy.update_db_proxy()

    # Get a working proxy
    # print(proxy.get())

    # Check proxy
    # print(proxy.check_proxy("216.80.39.89:3129"))

    # Clear DB
    # proxy.clear_db()

    # Example
    # proxy = Proxer(file_path_output=os.path.join(os.getcwd(), "output.txt"), file_path_save=os.path.join(os.getcwd(), "save.txt"))
    # result = proxy.get(5)
    # print(result)

