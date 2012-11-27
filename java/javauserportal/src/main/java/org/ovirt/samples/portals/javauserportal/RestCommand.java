package org.ovirt.samples.portals.javauserportal;

import java.io.InputStream;

import org.apache.commons.httpclient.Credentials;
import org.apache.commons.httpclient.UsernamePasswordCredentials;

public abstract class RestCommand {
    protected String url;
    protected String message;
    private String cookie;
    // We are saving the credentials but there is no need for that
    // because we are using cookie session
    private Credentials credentials;

    public RestCommand(String url, String userName, String password) {
        this.url = url;
        this.message = "";
        this.credentials = new UsernamePasswordCredentials(userName, password);
    }

    public RestCommand(String url, String cookie) {
        this.url = url;
        this.message = "";
        this.cookie = cookie;
    }

    public String getUrl() {
        return this.url;
    }

    public String getCookie() {
        return this.cookie;
    }

    public void setCookie(String cookie) {
        this.cookie = cookie;
    }

    public Credentials getCredentials() {
        return this.credentials;
    }

    public String getMessage() {
        return message;
    }

    public void setMessage(String message) {
        this.message += message + "\r\n<br/>";
    }

    public abstract void parseResponse(InputStream stream);
}
