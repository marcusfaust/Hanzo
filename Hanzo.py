import re
import requests
import urllib
import json
import operator
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


    def updateRU(self, node, ru):

        url = self.baseurl + "/commands/update-node-metadata"
        json_dict = {'node': node,
                     'key': 'RU',
                     'value': ru}
        headers = {"Content-type": "application/json"}
        r = requests.post(url, data=json.dumps(json_dict), headers=headers)
        print r


    def updateMeta(self, node, key, value):
        url = self.baseurl + "/commands/update-node-metadata"
        json_dict = {'node': node,
                     'key': key,
                     'value': value}
        headers = {"Content-type": "application/json"}
        r = requests.post(url, data=json.dumps(json_dict), headers=headers)


    def getNodesWithRU(self):

        nodeinfo = self.getNodes()
        sorted_nodeinfo = []
        rudict = {}
        for i in nodeinfo:
            if (nodeinfo[i]['metadata'].has_key('RU')):
                sorted_nodeinfo.append(i)

        for node in sorted_nodeinfo:
            rudict.update({nodeinfo[node]['name'] : nodeinfo[node]['metadata']['RU']})

        rudict_sorted = sorted(rudict, key=rudict.get)

        return rudict_sorted


    def toJSON_HASH(self, json_dict):

        json_string = json.dumps(json_dict)
        json_hash = urllib.urlencode({'json_hash': json_string})

        return json_hash


    def test_filter(self):
        url = self.baseurl + "/collections/nodes?name=node44"
        r = requests.get(url)
        results = r.json()

        return results


def extractLastOctet(ipaddress):
    last = re.split(r'(.*)\.(.*)\.(.*)\.(.*)', ipaddress)
    str_last = str(last[-2])
    return str_last

def extractSubnet(ipaddress):
    subnet = re.split(r'(.*\..*\..*\.).*', ipaddress)
    return subnet[-2]


if __name__ == '__main__':

    razor = RazorSession(RAZOR_REST_URL)
    razor.getNodesWithRU()


