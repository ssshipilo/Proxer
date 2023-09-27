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
<div style="text-align: center; width: 100%; background: linear-gradient(45deg, #ff00ff, rgb(0, 119, 255)); padding: 10px 10px; border-radius: 5px; color: #fff;">
    <a href="">
        Go to documentation
    </a>
</div>

## Steps 

### Install

#### Copy repository
    git clone https://github.com/ssshipilo/Proxer

#### Dependency installation
    pip install -r requirements.txt

___ or ___

#### Install library
    pip install Proxer

## Starting Proxer

Import the library into your project, and initialize the Proxer class, sample code to get 5 working proxies

```python
proxy = Proxer(file_path_output=os.path.join(os.getcwd(), "output.txt"), file_path_save=os.path.join(os.getcwd(), "save.txt"))
result = proxy.get(5)
print(result)
```

Result:
![Result Proxer](https://github.com/ssshipilo/Proxer/blob/main/git/result.png)
