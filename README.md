<h1 align="center">Proxer</h1>

![GPT 4 Private](https://github.com/ssshipilo/Proxer/blob/main/git/welcome.png)

<div align="center">
  <a href="https://github.com/ssshipilo/microsoft_account/pull">
    <img src="https://img.shields.io/github/issues-pr/cdnjs/cdnjs.svg" alt="GitHub pull requests" />
  </a>
</div>

<br />


___

<div align="center">
    The Proxer class provides methods to retrieve, validate, and save proxies.
</div>


## Features

- Huge proxy database
- Parsing of new available proxies (with uniqueization function)
- You can use your own proxy database
- Cleaning of database, working proxies, and general proxy list
- Checking proxies for performance, using popular sites giants for verification

## Documentation
[![Read Documentation](https://github.com/ssshipilo/Proxer/blob/main/git/btn.png)](https://github.com/ssshipilo/Proxer/blob/main/git/documentation.md)

## Steps 

### Install

#### Copy repository
    git clone https://github.com/ssshipilo/Proxer

#### Dependency installation
    pip install -r requirements.txt

## OR

#### Install library
    pip install Proxer

## Starting Proxer

Import the library into your project, and initialize the Proxer class, sample code to get 1 working proxies

```python
from Proxer import Proxer
import os

proxy = Proxer(file_path_output=os.path.join(os.getcwd(), "output.txt"), file_path_save=os.path.join(os.getcwd(), "save.txt"))
result = proxy.update_db_proxy() # Update or add files with database where you can mix proxy servers database
result = proxy.get(1) # Get the number of references, the answer in an array

print(result)
```

A huge database of proxy servers can be found [here](https://raw.githubusercontent.com/ssshipilo/Proxer/main/output.txt)

#### Result:
![Result Proxer](https://github.com/ssshipilo/Proxer/blob/main/git/result.png)

## Todo:
- [x] DONE. Create a library to get a working proxy
- [x] DONE. Put it on PyPI
- [ ] Find a specialist in multithreading to speed up the work of the code
- [ ] Add new providers for scraping available proxies
- [ ] Create a service so that ordinary users can use available proxies

## Resources
[The code that added the first 3 providers @rodukov](https://github.com/rodukov/proxyGrab/tree/main)