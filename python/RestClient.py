import base64
import httplib
import urllib2
import urlparse

cookie = None

'''
RestClient: handler RESTful post/get methods
'''
class RestClient(object):

    def doGetMethod(self, url, userName=None, password=None):
        global cookie
        req = urllib2.Request(url)
        if cookie is None:
            auth = "%s:%s" % (userName, password)
            auth = base64.encodestring(auth)
            req.add_header("Authorization", "Basic %s" % auth)
        else:
            req.add_header("Cookie", cookie)

        # run in user level API
        req.add_header('filter', 'true')
        # For using REST session via cookies, so we won't have to login on every request
        req.add_header('Prefer', 'persistent-auth')
        response = urllib2.urlopen(req)
        if not response.info().getheader('Set-Cookie') is None:
            cookie = response.info().getheader('Set-Cookie')

        return response.read()

    def doPostMethod(self, url):
        global cookie
        u = urlparse.urlparse(url)

        headers = {"Content-type": "application/xml"}
        headers['filter'] = 'true'
        headers['Prefer'] = 'persistent-auth'
        headers['Cookie'] = cookie

        conn = httplib.HTTPConnection(u.hostname, u.port)
        conn.request("POST", u.path, body="<action/>", headers=headers)
        res = conn.getresponse()
        return res.read()

    def resetCookie(self):
        global cookie
        cookie = None
