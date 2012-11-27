import RestCommand

import cgi
import BaseHTTPServer

restCommand = None

'''
WebHandler: simple Web Server
'''
class WebHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_POST(self):
        if self.path == '/':
            form = cgi.FieldStorage(fp=self.rfile, headers=self.headers, environ={'REQUEST_METHOD':'POST', 'CONTENT_TYPE':self.headers['Content-Type'], })
            self._login_method(form)
        else:
            self._page_error()

    def do_GET(self):
        # strip parameters from page name in get command
        # ie /mycgi?param=value
        # will get /mycgi
        p = self.path
        if p.find('?') != -1:
            p = self.path[:self.path.find('?')]
            params = self.path[self.path.find('?')+1:]

        if p == '/':
            self._login_method()
        elif p == '/action':
            self._action_method(params)
        else:
            self._page_error()

    def _page_error(self):
        self.send_response(404)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write("<html><head><title>Page not found</title></head>")
        self.wfile.write("<body><p>Page not found %s</p>" % self.path)
        self.wfile.write("</body></html>")


    def _action_method(self, params):
        global restCommand
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        form = cgi.parse_qs(params)

        vmid = form['vmid'][0]
        action = form['action'][0]

        res = restCommand.runAction(vmid, action)

        if res['status'] == 'failed':
            html = '''<html><body>
            <p style='color:red'>Action failed!</p>
            <br/>Reason: %s
            <br/>Details: %s
            <br/>
            <button onclick=javascript:history.back()>Back</button>
            </body></html>''' % (res['reason'], res['detail'])

        elif action == 'ticket':
            vm = restCommand.getVmByVmId(vmid)

            if self.headers['user-agent'].lower().find('windows') >= 0:
                html = self._ticketIE(vm, res)
            else:
                html = self._ticketFirefox(vm, res)

        else:
            html = '''<html><body>
            VM '%s' successfully
            <br/>
            <button onclick=javascript:history.back()>Back</button>
            </body></html>
            ''' % action

        self.wfile.write(html)

    def _ticketIE(self, vm, res):
        html = '''<html>
   <script>
       function onConnect() {
           spice.HostIP = '%s';
           spice.Port = '%s';
           spice.Password = '%s'
           spice.Connect();
       }
   </script>
<body>
    <OBJECT style='visibility: hidden' codebase='SpiceX.cab#version=1,0,0,1' ID='spice' CLASSID='CLSID:ACD6D89C-938D-49B4-8E81-DDBD13F4B48A'>
    </OBJECT>
    <form>
        <input type=button onclick='javascript:onConnect();' value='Connect'/>
    </form>
</body>
</html>''' % (vm['address'], vm['port'], res['value'])

        return html

    def _ticketFirefox(self, vm, res):
        html = '''<html>
   <script>
       function onConnect() {
            spice.hostIP = '%s';
            spice.port = '%s';
            spice.Password = '%s';
            spice.connect();
            spice.show()
       }
   </script>
<body>
    <embed id='spice' type="application/x-spice" width=0 height=0><br>
    <form>
        <input type=button value='Connent' onclick='onConnect()'/>
    </form>
</body>
</html>''' % (vm['address'], vm['port'], res['value'])

        return html


    def _uservms_method(self):
        #form = cgi.FieldStorage(fp=self.rfile, headers=self.headers, environ={'REQUEST_METHOD':'POST', 'CONTENT_TYPE':self.headers['Content-Type'], })

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        vms = restCommand.getUserVms()

        # render the html
        html = '''<html>
<body>
    <center><br/><br/>
    <table cellpadding="5" style='border-width: 1px; border-spacing: 2px; border-style: outset; border-color: gray; border-collapse: separate; background-color: white;'>
        <tr>
            <th>VM Name</th>
            <th>Status</th>
            <th>Display</th>
            <th>Start</th>
            <th>Stop</th>
            <th>Connect</th>
        </tr>
        '''

        for vm in vms:
            startable = ''
            if not vm['startable']:
                startable = "disabled='disabled'"
            stopable = ''
            if not vm['stopable']:
                stopable = "disabled='disabled'"
            connectable = ''
            if not vm['connectable'] or vm['display'] != 'spice':
                connectable = "disabled='disabled'"

            startbtn = "<button %s onclick=javascript:location.href='action?vmid=%s&action=start' type='button'>Start</button>" % (startable, vm['vmid'])
            stopbtn = "<button %s onclick=javascript:location.href='action?vmid=%s&action=stop' type='button'>Stop</button>" % (stopable, vm['vmid'])
            connectbtn = "<button %s onclick=javascript:location.href='action?vmid=%s&action=ticket' type='button'>Connect</button>" % (connectable, vm['vmid'])

            html = html + '''       <tr>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
        </tr>''' % (vm['name'], vm['status'], vm['display'], startbtn, stopbtn, connectbtn)

        html = html + '''   </table></center></body></html>'''
        self.wfile.write(html)


    def _login_method(self, form={}):
        global restCommand
        message = ''
        if form.has_key("username") and form.has_key('password'):
            restCommand = RestCommand.RestCommand()
            if restCommand.login(form.getvalue("username"), form.getvalue("password")):
                self._uservms_method()
                return
            else:
                message = 'Login Error'

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        html = '''<html>
<body>
<center><br/><br/>
<form name="input" action="/" method="post">
        <table>
            <tr>
                <td>User name:</td>
                <td><input type="text" name="username" value=""/></td>
            <tr>
                <td>Password:</td>
                <td><input type="password" name="password" value=""/></td>
            <tr>
                <td/>
                <td align="right"><input type="submit" value="Login"/></td>
            </tr>
            <tr>
                <td colspan='2' style='color:red'>%s</td>
            </tr>
    </form>
</body>
</html>'''
        self.wfile.write(html % message)
