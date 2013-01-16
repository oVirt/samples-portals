package org.ovirt.samples.portals.javauserportal;

import java.io.IOException;
import java.io.InputStream;
import java.util.Properties;

public class OVirtProperties {
    private String baseUrl;

    public OVirtProperties() {
        Properties prop = new Properties();
        InputStream in = getClass().getResourceAsStream("/ovirt.properties");
        try {
            prop.load(in);
            this.baseUrl = prop.getProperty("BaseUrl");
            in.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public String getBaseUrl() {
        return this.baseUrl;
    }
}
