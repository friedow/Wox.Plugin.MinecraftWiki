#encoding=utf8

import requests
import webbrowser
from wox import Wox,WoxAPI
import json

class MinecraftWiki(Wox):

    def request(self, url):
        #If user set the proxy, it will be handled.
        if self.proxy and self.proxy.get("enabled") and self.proxy.get("server"):
            proxies = {
                "http":"http://{}:{}".format(self.proxy.get("server"),self.proxy.get("port")),
                "https":"http://{}:{}".format(self.proxy.get("server"),self.proxy.get("port"))}
            return requests.get(url,proxies = proxies)
        else:
            return requests.get(url)

    def query(self, key):
        searchQueryUrl = "https://minecraft-de.gamepedia.com/api.php?action=opensearch&search={}".format(key)
        searchQuery = self.request(searchQueryUrl)
        autocompleteResult = json.loads(searchQuery.text)
        
        results = []
        for title, description, url in zip(autocompleteResult[1], autocompleteResult[2], autocompleteResult[3]):
            results.append({
                "Title": title ,
                "SubTitle":description,
                "IcoPath":"Images/app.png",
                "JsonRPCAction":{
                    "method": "openUrl",
                    "parameters":[url],
                    "dontHideAfterAction":True
                }
            })
        return results

    def openUrl(self, url):
        webbrowser.open(url)
        WoxAPI.change_query(url)

if __name__ == "__main__":
    MinecraftWiki()
