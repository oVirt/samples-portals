package org.ovirt.samples.portals.javauserportal;

import java.io.IOException;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.List;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;

import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.NodeList;
import org.xml.sax.SAXException;


public class UserVmsRestCommand extends RestCommand {

    private List<VmDetails> vms;

    public UserVmsRestCommand(String url, String cookie) {
        super(url, cookie);
        this.vms = new ArrayList<VmDetails>();
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
            NodeList allVms = doc.getElementsByTagName("vm");
            for(int i=0; i < allVms.getLength(); i++) {
                Element node = (Element)allVms.item(i);
                this.vms.add(initVmDetails(node));
            }

        } catch (SAXException e) {
            this.message = "Error parsing User Vms: " + e.getMessage();
            return;
        } catch (IOException e) {
            this.message = "Error parsing User Vms: " + e.getMessage();
            return;
        }
    }

    protected VmDetails initVmDetails(Element node) {
        VmDetails vmDetails = new VmDetails();

        vmDetails.setId(node.getAttribute("id"));
        vmDetails.setName(node.getElementsByTagName("name").item(0).getFirstChild().getNodeValue());
        vmDetails.setStatus(((Element)node.getElementsByTagName("status").item(0)).getElementsByTagName("state").item(0).getFirstChild().getNodeValue());

        Element displayElement = (Element)node.getElementsByTagName("display").item(0);
        vmDetails.setDisplay(displayElement.getElementsByTagName("type").item(0).getFirstChild().getNodeValue());

        if (displayElement.getElementsByTagName("port").getLength() > 0) {
            vmDetails.setPort(displayElement.getElementsByTagName("port").item(0).getFirstChild().getNodeValue());
        }

        if (displayElement.getElementsByTagName("address").getLength() > 0) {
            vmDetails.setAddress(displayElement.getElementsByTagName("address").item(0).getFirstChild().getNodeValue());
        }

        return vmDetails;
    }

    public List<VmDetails> getVms() {
        return vms;
    }

    public void setVms(List<VmDetails> vms) {
        this.vms = vms;
    }
}
