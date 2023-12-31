# Documentation Proxer

## Description
The Proxer class provides methods to retrieve, validate, and save proxies.

## Initialization
```python
from Proxer import Proxer
import os

proxy = Proxer(file_path_output=os.path.join(os.getcwd(), "output.txt"), file_path_save=os.path.join(os.getcwd(), "save.txt"))
```

*path must be absolute*
<br/>
file_path_output: path to the file where the list of sparse proxies will be saved.
<br/>
file_path_save: path to the file where the list of working proxies will be saved.

---

## To summarize
```python
from Proxer import Proxer
import os

proxy = Proxer(file_path_output=os.path.join(os.getcwd(), "output.txt"), file_path_save=os.path.join(os.getcwd(), "save.txt"))
result = proxy.update_db_proxy() # Update or add files with database where you can mix proxy servers database
result = proxy.get(1) # Get the number of references, the answer in an array
print(result)

proxy.parse("./test.txt") # Parses new proxies to a file
print(proxy.check_proxy("216.80.39.89:3129")) # Checks if this proxy is working
proxy.clear_db() # Clearing databases, you can delete 2 at once, proxy list and verified proxy list
```

## Methods

### parse()
Parsing of popular proxy providers:

- hidemyname: [https://hidemy.name/en/proxy-list/](https://hidemy.name/en/proxy-list/)
- free_proxy_list: [https://free-proxy-list.net/](https://free-proxy-list.net/) 
- proxyscrape: [https://proxyscrape.com/](https://proxyscrape.com/)  

*They may be added over time, or maybe they already are.*

Arguments:
path: path to the file where the proxy list will be written. By default - the path from file_path_output.
<br/>
returned_array: whether to return the array of sparse proxies. By default - False.


---
### check_proxy()
Checking the proxy to make sure it works.

Arguments:
proxy: proxy to check.
<br/>
_class: whether to save the working proxy to a file. The default is False.


---
### update_db_proxy()
Updating the database of working proxies.

Arguments:
path: (optional) - path to the list of sparser proxies
<br/>
file: True - from your file. The default is False. Make parsing of known services with proxy


---
### get()
Get a working proxy.

Arguments:
count: number of required proxies. The default is 1.

---
### clear_db()
Cleaning databases, verified and unverified proxies.

Arguments:
mode: cleaning mode. Can be "output" (unchecked proxies) or "save" (checked proxies). The default is None (clearing both databases).
<br/>
path_output: path to the file with unchecked proxies.
<br/>
path_save: path to the file with verified proxies.