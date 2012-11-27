package org.ovirt.samples.portals.javauserportal;

import java.io.IOException;
import java.io.InputStream;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;

import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.xml.sax.SAXException;

public class VmByIdRestCommand extends UserVmsRestCommand {

    private VmDetails vmDetails;

    public VmByIdRestCommand(String url, String cookie) {
        super(url, cookie);
    }

    @Override
    public void parseResponse(InputStream stream) {
        DocumentBuilderFactory fact = DocumentBuilderFactory.newInstance();
        DocumentBuilder builder = null;
        try {
            builder = fact.newDocumentBuilder();
        } catch (ParserConfigurationException e) {
            this.message = "Cannot create DocumentBuilder: " + e.getMessage();
            return;
        }
        try {
            Document doc = builder.parse(stream);
            this.vmDetails = initVmDetails((Element)doc.getElementsByTagName("vm").item(0));

        } catch (SAXException e) {
            this.message = "Error parsing User Vms: " + e.getMessage();
            return;
        } catch (IOException e) {
            this.message = "Error parsing User Vms: " + e.getMessage();
            return;
        }
    }

    public VmDetails getVmDetails() {
        return this.vmDetails;
    }
}
