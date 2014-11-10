import requests
from config import *


class RazorSession:

    def __init__(self, razorurl):
        self.baseurl = razorurl
        pass

    def getNodes(self):

        nodeinfo = {}

        #Get Node ID's
        url = self.baseurl + "/collections/nodes"
        r = requests.get(url)
        results = r.json()

        #Get Details from Each Node
        for node in results['items']:
            nodename = node['name']
            url = self.baseurl + "/collections/nodes/" + nodename
            r = requests.get(url)
            nodeinfo[nodename] = r.json()
            print nodename

        pass



if __name__ == '__main__':

    razor = RazorSession(RAZOR_REST_URL)
    razor.getNodes()
