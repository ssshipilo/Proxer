from proxy_grab.proxy_grab import proxyGrab

def update_proxy_list(mode="hidemyname"):
    """
    Mode:
        hidemyname - scrape https://hidemy.name/en/proxy-list/
        free_proxy_list - scrape https://free-proxy-list.net/
        proxyscrape - scrape https://proxyscrape.com/
    """

    if mode == "hidemyname":
        output = []
        for d in range(1, 5):
            request = proxyGrab.hidemyname.request(page=d)
            result = proxyGrab.hidemyname.sort(request=request)
            for i in result:
                output.append(i)
        
        return output

    if mode == "free_proxy_list":
        request = proxyGrab.free_proxy_list.request()
        result = proxyGrab.free_proxy_list.sort(request)
        
        return result

    if mode == "proxyscrape":
        request = proxyGrab.proxyscrape.request(protocol="socks5")
        result = proxyGrab.proxyscrape.sort(request)
        return result
    
if __name__ == "__main__":
    print(update_proxy_list())