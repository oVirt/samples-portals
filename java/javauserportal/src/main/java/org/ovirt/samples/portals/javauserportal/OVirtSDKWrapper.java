package org.ovirt.samples.portals.javauserportal;

import java.io.IOException;
import java.util.List;
import java.util.UUID;

import org.apache.http.client.ClientProtocolException;
import org.ovirt.engine.sdk.Api;
import org.ovirt.engine.sdk.decorators.VM;
import org.ovirt.engine.sdk.entities.Action;
import org.ovirt.engine.sdk.exceptions.ServerException;
import org.ovirt.engine.sdk.exceptions.UnsecuredConnectionAttemptError;

public class OVirtSDKWrapper {
    private Api api;
    private String message;

    public void login(String baseUrl, String userName, String password) {
        try {
            // true for filter, ie enable regular users to login
            this.api = new Api(baseUrl, userName, password, null, null, null,
                    null, null, null, null, true, null);
        } catch (ClientProtocolException e) {
            this.message = "Protocol Exception: " + e.getMessage();
        } catch (ServerException e) {
            this.message = "Server Exception: " + e.getMessage();
        } catch (UnsecuredConnectionAttemptError e) {
            this.message = "Unsecured Connection Exception: " + e.getMessage();
        } catch (IOException e) {
            this.message = "IOException Exception: " + e.getMessage();
        }
    }

    public boolean isLoggedin() {
        return this.api != null;
    }

    public String getMessage() {
        return this.message;
    }

    public List<VM> getVms() {
        try {
            return this.api.getVMs().list();
        } catch (ClientProtocolException e) {
            this.message = "Protocol Exception: " + e.getMessage();
        } catch (ServerException e) {
            this.message = "Server Exception: " + e.getMessage();
        } catch (IOException e) {
            this.message = "IOException Exception: " + e.getMessage();
        }
        return null;
    }

    public VM getVmById(String vmid) {
        try {
            return this.api.getVMs().get(UUID.fromString(vmid));
        } catch (ClientProtocolException e) {
            this.message = "Protocol Exception: " + e.getMessage();
        } catch (ServerException e) {
            this.message = "Server Exception: " + e.getMessage();
        } catch (IOException e) {
            this.message = "IOException Exception: " + e.getMessage();
        }
        return null;
    }

    public Action startVm(String vmid) {
        try {
            VM vm = this.api.getVMs().get(UUID.fromString(vmid));
            return vm.start(new Action());
        } catch (ClientProtocolException e) {
            this.message = "Protocol Exception: " + e.getMessage();
        } catch (ServerException e) {
            this.message = "Server Exception: " + e.getReason() + ": " + e.getDetail();
        } catch (IOException e) {
            this.message = "IOException Exception: " + e.getMessage();
        }
        return null;
    }

    public Action stopVm(String vmid) {
        try {
            VM vm = this.api.getVMs().get(UUID.fromString(vmid));
            return vm.stop(new Action());
        } catch (ClientProtocolException e) {
            this.message = "Protocol Exception: " + e.getMessage();
        } catch (ServerException e) {
            this.message = "Server Exception: " + e.getReason() + ": " + e.getDetail();
        } catch (IOException e) {
            this.message = "IOException Exception: " + e.getMessage();
        }
        return null;
    }

    public Action ticketVm(String vmid) {
        try {
            VM vm = this.api.getVMs().get(UUID.fromString(vmid));
            return vm.ticket(new Action());
        } catch (ClientProtocolException e) {
            this.message = "Protocol Exception: " + e.getMessage();
        } catch (ServerException e) {
            this.message = "Server Exception: " + e.getReason() + ": " + e.getDetail();
        } catch (IOException e) {
            this.message = "IOException Exception: " + e.getMessage();
        }
        return null;
    }
}
