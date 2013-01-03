import OVirtDispatcher

import cgi
import BaseHTTPServer

dispatcher = None

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
        elif self.path == '/uservms':
            self._uservms_method()
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
        elif p == '/uservms':
            self._uservms_method()
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

    def _failed_action(self, reason, detail):
        return '''<html><body>
        <p style='color:red'>Action failed!</p>
        <br/>Reason: %s
        <br/>Details: %s
        <br/>
        <button onclick=javascript:location.href='/uservms'>Back</button>
        </body></html>''' % (reason, detail)

    def _action_method(self, params):
        global dispatcher
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        form = cgi.parse_qs(params)

        vmid = form['vmid'][0]
        action = form['action'][0]
        success = False

        if action == 'start':
            success, reason, detail = dispatcher.startVm(vmid)
            if not success:
                html = self._failed_action(reason, detail)

        elif action == 'stop':
            success, reason, detail = dispatcher.stopVm(vmid)
            if not success:
                html = self._failed_action(reason, detail)

        elif action == 'ticket':
            try:
                value, expiry = dispatcher.ticketVm(vmid)

                vm = dispatcher.getVmById(vmid)
                display = vm.get_display()

                if self.headers['user-agent'].lower().find('windows') >= 0:
                    html = self._ticketIE(display.get_address(), display.get_port(), value)
                else:
                    html = self._ticketFirefox(display.get_address(), display.get_port(), value)
            except Exception as e:
                reason, detail = e.args
                html = self._failed_action(reason, detail)

        if success:
            html = '''<html><body>
            VM '%s' successfully
            <br/>
            <button onclick=javascript:location.href='/uservms'>Back</button>
            </body></html>
            ''' % action

        self.wfile.write(html)

    def _ticketIE(self, host, port, password):
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
    VMs ticket set:
    <br/>
    <OBJECT style='visibility: hidden' codebase='SpiceX.cab#version=1,0,0,1' ID='spice' CLASSID='CLSID:ACD6D89C-938D-49B4-8E81-DDBD13F4B48A'>
    </OBJECT>
    <form>
        <input type=button onclick='javascript:onConnect();' value='Connect'/>
    </form>
    <button onclick=javascript:location.href='/uservms'>Back</button>
</body>
</html>''' % (host, port, password)

        return html

    def _ticketFirefox(self, host, port, password):
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
    VMs ticket set:
    <br/>
    <embed id='spice' type="application/x-spice" width=0 height=0><br>
    <form>
        <input type=button value='Connent' onclick='onConnect()'/>
    </form>
    <button onclick=javascript:location.href='/uservms'>Back</button>
</body>
</html>''' % (host, port, password)

        return html


    def _uservms_method(self):
        global dispatcher

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        vms = dispatcher.getUserVms()

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
            <th>Console</th>
        </tr>
        '''

        for vm in vms:
            startbtn = "<button onclick=javascript:location.href='action?vmid=%s&action=start' type='button'>Start</button>" % (vm.get_id())
            stopbtn = "<button onclick=javascript:location.href='action?vmid=%s&action=stop' type='button'>Stop</button>" % (vm.get_id())
            connectbtn = "<button onclick=javascript:location.href='action?vmid=%s&action=ticket' type='button'>Console</button>" % (vm.get_id())

            html = html + '''       <tr>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
        </tr> ''' % (vm.get_name(), vm.get_status().get_state(), vm.get_display().get_type(), startbtn, stopbtn, connectbtn)

        html = html + '''
        <tr>
            <td><button onclick=javascript:location.href='/'>Logout</button></td>
        </tr>
        </table></center></body></html>'''
        self.wfile.write(html)

    def _redirectTo(self, url, timeout=0):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write("""<html><head><meta HTTP-EQUIV="REFRESH" content="%i; url=%s"/></head></html>""" % (timeout, url))


    def _login_method(self, form={}):
        global dispatcher
        message = ''
        if form.has_key("username") and form.has_key('password'):
            dispatcher = OVirtDispatcher.OVirtDispatcher()
            loggedin, message = dispatcher.login(form.getvalue("username"), form.getvalue("password"))

            if loggedin:
                self._redirectTo('/uservms')
                return

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
