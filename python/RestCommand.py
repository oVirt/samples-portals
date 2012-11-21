import RestClient

import ConfigParser
from xml.dom import minidom

restClient = RestClient.RestClient()

class RestCommand(object):

    def __init__(self):
        global restClient
        self.config = ConfigParser.ConfigParser()
        self.config.read('ovirt.conf')
        self.baseUrl = self.config.get('oVirt', 'BaseUrl')

    def _parseVm(self, xmlVm):
        vm = {}
        vm['startable'] = True
        vm['stopable'] = True
        vm['connectable'] = True
        vm['vmid'] =  xmlVm.getAttribute('id')
        vm['name'] = xmlVm.getElementsByTagName('name').item(0).firstChild.nodeValue
        vm['status'] = xmlVm.getElementsByTagName('status').item(0).getElementsByTagName('state').item(0).firstChild.nodeValue
        vm['display'] = xmlVm.getElementsByTagName('display').item(0).getElementsByTagName('type').item(0).firstChild.nodeValue
        if len(xmlVm.getElementsByTagName('port')) > 0:
            vm['port'] = xmlVm.getElementsByTagName('port').item(0).firstChild.nodeValue
        else:
            vm['port'] = '-1'
        if len(xmlVm.getElementsByTagName('address')) > 0:
            vm['address'] = xmlVm.getElementsByTagName('address').item(0).firstChild.nodeValue
        else:
            vm['address'] = ''
        return vm

    def login(self, userName, password):
        self.userName = userName
        self.password = password

        try:
            restClient.resetCookie()
            xml = restClient.doGetMethod(self.baseUrl + '/api', userName, password)
            return True
        except:
            return False

    def getUserVms(self):
        global restClient
        xml = restClient.doGetMethod(self.baseUrl + '/api/vms')
        dom = minidom.parseString(xml)
        xmlVms = dom.getElementsByTagName('vm')
        vms = []
        for xmlVm in xmlVms:
            vms.append(self._parseVm(xmlVm))

        return vms

    def getVmByVmId(self, vmid):
        global restClient
        xml = restClient.doGetMethod(self.baseUrl + '/api/vms/' + vmid)
        dom = minidom.parseString(xml)
        return self._parseVm(dom.getElementsByTagName('vm')[0])

    '''
        Method return action results

        input:
            vmid: guid of vm
            action: action to run (start, stop or ticket) - there are more actions...(never tested)

        return value:
            dictionary
            { 'status': 'complete',
              'reason': '...',    # only if failed
              'detail': '...',    # only if failed
              'value': 'XXYYZZ',  # the ticket (password)
              'expired': '7200',  # in minutes
            }
    '''
    def runAction(self, vmid, action):
        global restClient
        ret = {}
        url = '%s/api/vms/%s/%s' % (self.baseUrl, vmid, action)

        xml = restClient.doPostMethod(url)
        dom = minidom.parseString(xml)

        ret['status'] = dom.getElementsByTagName('state').item(0).firstChild.nodeValue
        if ret['status'] == 'failed':
            ret['reason'] = dom.getElementsByTagName('reason').item(0).firstChild.nodeValue
            ret['detail'] = dom.getElementsByTagName('detail').item(0).firstChild.nodeValue

        if action == 'ticket':
            elem = dom.getElementsByTagName('ticket').item(0)
            ret['value'] = elem.getElementsByTagName('value').item(0).firstChild.nodeValue
            ret['expired'] = elem.getElementsByTagName('expiry').item(0).firstChild.nodeValue

        return ret
