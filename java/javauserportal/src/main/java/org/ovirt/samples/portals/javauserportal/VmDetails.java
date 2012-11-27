package org.ovirt.samples.portals.javauserportal;

public class VmDetails {
    private String id;
    private String name;
    private String status;
    private String display;
    private String port;
    private String address;

    public VmDetails() {
    }

    public void setId(String id) {
        this.id = id;
    }
    public String getId() {
        return this.id;
    }

    public void setName(String name) {
        this.name = name;
    }
    public String getName() {
        return this.name;
    }

    public void setStatus(String status) {
        this.status = status;
    }
    public String getStatus() {
        return this.status;
    }

    public void setDisplay(String display) {
        this.display = display;
    }
    public String getDisplay() {
        return this.display;
    }

    public void setPort(String port) {
        this.port = port;
    }
    public String getPort() {
        return this.port;
    }

    public void setAddress(String address) {
        this.address = address;
    }
    public String getAddress() {
        return this.address;
    }
}
