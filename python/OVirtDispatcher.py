from ovirtsdk.api import API
from ovirtsdk.infrastructure.errors import RequestError, ConnectionError

import ConfigParser
api = None

class OVirtDispatcher(object):

    def __init__(self):
        self.config = ConfigParser.ConfigParser()
        self.config.read('ovirt.conf')
        self.baseUrl = self.config.get('oVirt', 'BaseUrl')

    def login(self, username, password):
        global api
        try:
            api = API(url=self.baseUrl, username=username, password=password, filter=True)
        except RequestError as reqErr:
            return False, "Login error"
        except ConnectionError as conErr:
            return False, "Bad URL"
        return True, ''

    def getUserVms(self):
        global api
        return api.vms.list()

    def getVmById(self, id):
        global api
        return api.vms.get(id)

    def startVm(self, vmid):
        global api
        try:
            api.vms.get(id=vmid).start()
        except RequestError as reqErr:
            return False, reqErr.reason, reqErr.detail
        except ConnectionError as conErr:
            return False, 'Connection Error'
        return True, None, None

    def stopVm(self, vmid):
        global api
        try:
            api.vms.get(id=vmid).stop()
        except RequestError as reqErr:
            return False, reqErr.reason, reqErr.detail
        except ConnectionError as conErr:
            return False, 'Connection Error'
        return True, None, None

    def ticketVm(self, vmid):
        global api
        try:
            ticket = api.vms.get(id=vmid).ticket()
            return ticket.get_ticket().get_value(), ticket.get_ticket().get_expiry()
        except RequestError as reqErr:
            raise Exception(reqErr.reason, reqErr.detail)
        except ConnectionError as conErr:
            raise Exception('Connection Error', '')
