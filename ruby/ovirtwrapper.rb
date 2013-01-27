require 'yaml'
require 'rbovirt'

class OVirtWrapper
    def initialize
        conf = YAML.load_file('ovirt.conf.yml')
        @baseUrl = conf['ovirt']['baseurl'] + '/api'
        @message = ''
    end

    def login(username, password)
        begin
            @client = ::OVIRT::Client.new(username, password, @baseUrl, nil, nil, true)
            @client.vms
        rescue Exception => e
            @client = nil
            @message = e.message
            return false
        end
        return true
    end

    def getMessage
        return @message
    end

    def logout
        @client = nil
    end

    def loggedin?
        return @client == nil
    end

    def vms
        return @client.vms
    end

    def startVm(vmid)
        begin
            @client.vm_action(vmid, :start)
        rescue Exception => e
            @message = e.message
            return false
        end
        return true
    end

    def stopVm(vmid)
        begin
            @client.vm_action(vmid, :stop)
        rescue Exception => e
            @message = e.message
            return false
        end
        return true
    end

    def ticketVm(vmid)
        ticket = ''
        begin
            ticket = @client.set_ticket(vmid)
        rescue Exception => e
            @message = e.message
        end
        return ticket
    end

    def vmById(vmid)
        for i in 0...vms.length
            if vms[i].id == vmid
                return vms[i]
            end
        end
    end
end
