<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%@page import="org.ovirt.samples.portals.javauserportal.OVirtSDKWrapper"%>
<%@page import="org.ovirt.engine.sdk.decorators.VM"%>
<html>
<body>
    <%
    if (session.getAttribute("wrapper") == null) {
        response.sendRedirect("index.jsp");
    }
    OVirtSDKWrapper wrapper = (OVirtSDKWrapper)session.getAttribute("wrapper");
    %>
    <center>
    <br/><br/>
    <table cellpadding="5" style='border-width: 1px; border-spacing: 2px; border-style: outset; border-color: gray; border-collapse: separate; background-color: white;'>
        <tr>
            <th>VM Name</th>
            <th>Status</th>
            <th>Display</th>
            <th>Start</th>
            <th>Stop</th>
            <th>Console</th>
        </tr>
        <%

            for (VM vm: wrapper.getVms()) {
        %>
        <tr>
            <td><%= vm.getName() %></td>
            <td><%= vm.getStatus().getState() %></td>
            <td><%= vm.getDisplay().getType() %></td>
            <td><button %s onclick=javascript:location.href='action.jsp?vmid=<%= vm.getId() %>&action=start' type='button'>Start</button></td>
            <td><button %s onclick=javascript:location.href='action.jsp?vmid=<%= vm.getId() %>&action=stop' type='button'>Stop</button></td>
            <td><button %s onclick=javascript:location.href='action.jsp?vmid=<%= vm.getId() %>&action=ticket' type='button'>Console</button></td>
        </tr>
        <%
            }
        %>
        <tr>
            <td><button onclick=javascript:location.href='index.jsp'>Logout</button></td>
        </tr>
    </table>

    </center>
</body>
</html>
