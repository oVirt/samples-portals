<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<%@page import="org.ovirt.samples.portals.javauserportal.OVirtSDKWrapper"%>
<%@page import=" org.ovirt.engine.sdk.entities.Action"%>
<html>
<body>
    <%
    if (session.getAttribute("wrapper") == null) {
        response.sendRedirect("index.jsp");
    }
    OVirtSDKWrapper wrapper = (OVirtSDKWrapper)session.getAttribute("wrapper");
    String vmid = request.getParameter("vmid");
    String action = request.getParameter("action");

    Action results = null;
    if (action.equals("start")) {
        results = wrapper.startVm(vmid);
    }
    else if (action.equals("stop")) {
        results = wrapper.stopVm(vmid);
    }
    else if (action.equals("ticket")) {
        results = wrapper.ticketVm(vmid);
         if (results != null && !results.isSetFault()) {
            session.setAttribute("ticket", results.getTicket());
            response.sendRedirect("spice.jsp?vmid=" + vmid);
        }
    }
    else {
        response.sendRedirect("index.jsp");
    }

    if (results != null && results.isSetFault()) {
    %>
        <p style='color:red'>Action failed!</p>
        <br/>Reason: <%= results.getFault().getReason() %>
        <br/>Details:<%= results.getFault().getDetail() %>
        <br/>
        <button onclick=javascript:history.back()>Back</button>
    <%
    } else if (results == null) {
    %>
    <p style='color:red'>Action failed!</p>
    <br/>
    <%= wrapper.getMessage() %>
    <br/>
    <button onclick=javascript:location.href='uservms.jsp'>Back</button>
    <%
    } else {
    %>
    Action success
    <br/>
    <button onclick=javascript:location.href='uservms.jsp'>Back</button>
    <%
    }
    %>
</body>
</html>
