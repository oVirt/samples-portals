#!/usr/bin/ruby -rubygems

require 'sinatra'
require 'yaml'

$LOAD_PATH.unshift(File.join(File.dirname(__FILE__), '.' ))
require 'ovirtwrapper'

## --------------------------------------------
enable :sessions

configure do
    conf = YAML.load_file('ovirt.conf.yml')
    set :bind, conf['server']['host']
    set :port, conf['server']['port']
end

get '/vms' do
    doVms
end

get '/action?*' do
    doAction
end

get '/logout' do
    logout
end

post '*' do
    login
end

get '*' do
    login
end
## --------------------------------------------

def logout
    session[:wrapper] = nil
    redirect to '/'
end

def login
    message = ''
    wrapper = OVirtWrapper.new
    if params['username'] != nil and params['password'] != nil
        if wrapper.login(params['username'], params['password'])
            session[:wrapper] = wrapper
            redirect to('/vms')
        else
            message = wrapper.getMessage
        end
    end

    '<html>
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
                    <td colspan="2" style="color:red">%s</td>
                </tr>
        </form>
    </body>
    </html>' % message
end

def doVms
    wrapper = session[:wrapper]
    if wrapper == nil
        redirect to '/'
    end

    html = '<html>
    <body>
        <center><br/><br/>
        <table cellpadding="5" style="border-width: 1px; border-spacing: 2px; border-style: outset; border-color: gray; border-collapse: separate; background-color: white;">
            <tr>
                <th>VM Name</th>
                <th>Status</th>
                <th>Display</th>
                <th>Start</th>
                <th>Stop</th>
                <th>Console</th>
            </tr>'
    for i in 0...wrapper.vms.length
        vm = wrapper.vms[i]
        startbtn = "<button onclick=javascript:location.href='action?vmid=%s&action=start' type='button'>Start</button>" % vm.id
        stopbtn = "<button onclick=javascript:location.href='action?vmid=%s&action=stop' type='button'>Stop</button>" % vm.id
        connectbtn = "<button onclick=javascript:location.href='action?vmid=%s&action=ticket' type='button'>Console</button>" % vm.id
        html = html + '<tr>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        </tr> ' % [vm.name, vm.status, vm.display[:type], startbtn, stopbtn, connectbtn]
    end

    html += '<tr>
        <td><button onclick=javascript:location.href="/logout">Logout</button></td>
    </tr>
    </table></center></body></html>'

    html
end

def doAction
    wrapper = session[:wrapper]
    if wrapper == nil
        redirect to '/'
    end

    vmid = params['vmid']
    action = params['action']

    success = false
    if action == 'start'
        success = wrapper.startVm(vmid)
    elsif action == 'stop'
        success = wrapper.stopVm(vmid)
    else # ticket
        ticket = wrapper.ticketVm(vmid)
        if ticket != ''
            vm = wrapper.vmById(vmid)
            return show_console(vm, ticket)
        end
    end

    if success
        '<html><body>
        VM "%s" successfully
        <br/>
        <button onclick=javascript:location.href="vms">Back</button>
        </body></html>' % action
    else
        '<html><body>
        <p style="color:red">Action failed!</p>
        <br/>Reason: %s
        <br/>
        <button onclick=javascript:location.href="vms">Back</button>
        </body></html>' % wrapper.getMessage
    end
end

def show_console(vm, ticket)
    html = '<html>
    <head>
    <script type="text/javascript">
    if (window.addEventListener) { // Firefox
        window.addEventListener("load", WindowLoad, false);
    } else if (window.attachEvent) { // IE
        window.attachEvent("onload", WindowLoad);
    }

    function WindowLoad(event) {
        spice.hostIP = "%s";
        spice.port = "%s";
        spice.Password = "%s";
        spice.connect();
        spice.show()
    }
    </script>
    </head>
    ' % [vm.display[:address], vm.display[:port], ticket]

    html += '<body>
        <button onclick=javascript:location.href="vms">Back</button>'

    if request.user_agent.downcase.index('windows') != nil
        html += "<object style='visibility: hidden' codebase='SpiceX.cab#version=1,0,0,1' ID='spice' CLASSID='CLSID:ACD6D89C-938D-49B4-8E81-DDBD13F4B48A'/>"
    else
        html += "<embed id='spice' type='application/x-spice' width=0 height=0/>"
    end
    html += '</body></html>'

    html
end
