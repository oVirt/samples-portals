package org.ovirt.samples.portals.javauserportal;

import java.io.IOException;
import java.net.HttpURLConnection;

import org.apache.commons.httpclient.DefaultHttpMethodRetryHandler;
import org.apache.commons.httpclient.HttpClient;
import org.apache.commons.httpclient.HttpException;
import org.apache.commons.httpclient.HttpStatus;
import org.apache.commons.httpclient.auth.AuthScope;
import org.apache.commons.httpclient.methods.GetMethod;
import org.apache.commons.httpclient.methods.PostMethod;
import org.apache.commons.httpclient.methods.RequestEntity;
import org.apache.commons.httpclient.methods.StringRequestEntity;
import org.apache.commons.httpclient.params.HttpMethodParams;

public class RestClient {
    public void doGetCommand(RestCommand command) {
        HttpClient client = new HttpClient();
        GetMethod method = new GetMethod(command.getUrl());
        method.getParams().setParameter(HttpMethodParams.RETRY_HANDLER,
                new DefaultHttpMethodRetryHandler(3, false));
        method.setRequestHeader("filter", "true");
        method.setRequestHeader("Prefer", "persistent-auth");

        if (command.getCookie() != null) {
            method.setRequestHeader("Cookie", command.getCookie());
        } else {
            client.getParams().setAuthenticationPreemptive(true);
            client.getState().setCredentials(AuthScope.ANY, command.getCredentials());
        }

        try {
            int statusCode = client.executeMethod(method);

            if (statusCode != HttpStatus.SC_OK) {
                command.setMessage("Get Method failed: " + method.getStatusLine());
                return;
            }

            if (method.getResponseHeader("Set-Cookie") != null) {
                command.setCookie(method.getResponseHeader("Set-Cookie").getValue());
            }
            command.parseResponse(method.getResponseBodyAsStream());

        } catch (HttpException e) {
            command.setMessage("Fatal protocol violation: " + e.getMessage());
        } catch (IOException e) {
            command.setMessage("Fatal transport error: " + e.getMessage());
        } finally {
            method.releaseConnection();
        }
    }

    public void doPostCommand(RestCommand command) {
        HttpClient client = new HttpClient();
        PostMethod method = new PostMethod(command.getUrl());

        method.getParams().setParameter(HttpMethodParams.RETRY_HANDLER,
                new DefaultHttpMethodRetryHandler(3, false));
        method.setRequestHeader("Content-type", "application/xml");
        method.setRequestHeader("filter", "true");
        method.setRequestHeader("Prefer", "persistent-auth");

        if (command.getCookie() != null) {
            method.setRequestHeader("Cookie", command.getCookie());
        } else {
            client.getParams().setAuthenticationPreemptive(true);
            client.getState().setCredentials(AuthScope.ANY, command.getCredentials());
        }

        // @deprecated...
        //method.setRequestBody("<action/>");
        RequestEntity entity = new StringRequestEntity("<action/>");
        method.setRequestEntity(entity);

        try {
            if (method.getResponseHeader("Set-Cookie") != null) {
                command.setCookie(method.getResponseHeader("Set-Cookie").getValue());
            }
            int statusCode = client.executeMethod(method);
            if (statusCode != HttpStatus.SC_OK) {
                command.setMessage("Post Method failed: " + method.getStatusLine());
            }
            command.parseResponse(method.getResponseBodyAsStream());

        } catch (HttpException e) {
            command.setMessage("Fatal protocol violation: " + e.getMessage());
        } catch (IOException e) {
            command.setMessage("Fatal transport error: " + e.getMessage());
        } catch (Exception e) {
            command.setMessage("Fatal error: " + e.getMessage());
        } finally {
            method.releaseConnection();
        }
    }
}
