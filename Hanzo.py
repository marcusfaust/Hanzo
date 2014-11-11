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

        return nodeinfo


    def getNodeNames(self, nodeinfo):

        names = []

        for node in nodeinfo:
            names.append(nodeinfo[node]['name'])

        return names





if __name__ == '__main__':

    razor = RazorSession(RAZOR_REST_URL)
    nodeinfo = razor.getNodes()
    for node in nodeinfo:
        print nodeinfo.__len__()


