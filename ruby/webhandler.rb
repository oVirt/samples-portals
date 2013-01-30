#!/usr/bin/env ruby

require 'rubygems'
require 'bundler'

Bundler.require

require 'yaml'

APP_ROOT = File.dirname(__FILE__)
$LOAD_PATH.unshift(File.join(APP_ROOT, '.' ))
require 'ovirtwrapper'

## --------------------------------------------
enable :sessions

configure do
    conf = YAML.load_file("#{APP_ROOT}/ovirt.conf.yml")
    set :bind, conf['server']['host']
    set :port, conf['server']['port']
    set :views, APP_ROOT + "/views"
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
    @message = ''
    wrapper = OVirtWrapper.new
    if params['username'] != nil and params['password'] != nil
        if wrapper.login(params['username'], params['password'])
            session[:wrapper] = wrapper
            redirect to('/vms')
        else
            @message = wrapper.getMessage
        end
    end
    erb :'login.html'
end

def doVms
    wrapper = session[:wrapper]
    redirect to '/' unless wrapper
    @vms = wrapper.vms
    erb :'vms.html'
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
