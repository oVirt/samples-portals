package org.ovirt.samples.portals.javauserportal;

import java.io.InputStream;

public class LoginRestCommand extends RestCommand {

    private boolean loggedIn = false;

    public LoginRestCommand(String url, String userName, String password) {
        super(url, userName, password);
    }

    @Override
    public void parseResponse(InputStream stream) {
        this.loggedIn = (this.message == "");
    }

    public boolean isLoggedin() {
        return this.loggedIn;
    }
}
