package org.ovirt.samples.portals.javauserportal;

import java.io.IOException;
import java.io.InputStream;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;

import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.NodeList;
import org.xml.sax.SAXException;

public class ActionRestCommand extends RestCommand {

    private String failReason;
    private String failDetails;
    private String ticketValue;
    private String ticketExpired;

    public ActionRestCommand(String url, String cookie) {
        super(url, cookie);
    }

    @Override
    public void parseResponse(InputStream stream) {
            DocumentBuilderFactory fact = DocumentBuilderFactory.newInstance();
            DocumentBuilder builder = null;
            Document doc = null;

            try {
                builder = fact.newDocumentBuilder();
            } catch (ParserConfigurationException e) {
                this.setMessage("Document parsing error: " + e.getMessage());
                return;
            }
            try {
                doc = builder.parse(stream);
            } catch (SAXException e) {
                this.setMessage("Document building error: " + e.getMessage());
                return;
            } catch (IOException e) {
                this.setMessage("IO Exception: " + e.getMessage());
                return;
            }

            String status = doc.getElementsByTagName("state").item(0).getFirstChild().getNodeValue();

            if (status.equals("failed")) {
                this.failReason = doc.getElementsByTagName("reason").item(0).getFirstChild().getNodeValue();
                this.failDetails = doc.getElementsByTagName("detail").item(0).getFirstChild().getNodeValue();
            } else if (this.url.contains("ticket")) {
                Element t = (Element)doc.getElementsByTagName("ticket").item(0);
                this.ticketValue = t.getElementsByTagName("value").item(0).getFirstChild().getNodeValue();
                this.ticketExpired = t.getElementsByTagName("expiry").item(0).getFirstChild().getNodeValue();
            }
    }

    public String getFailReason() {
        return failReason;
    }

    public String getFailDetails() {
        return failDetails;
    }

    public String getTicketValue() {
        return ticketValue;
    }

    public String getTicketExpired() {
        return ticketExpired;
    }
}
