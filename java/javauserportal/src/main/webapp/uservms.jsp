<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%@page import="org.ovirt.samples.portals.javauserportal.UserVmsRestCommand"%>
<%@page import="org.ovirt.samples.portals.javauserportal.RestCommand"%>
<%@page import="org.ovirt.samples.portals.javauserportal.RestClient"%>
<%@page import="org.ovirt.samples.portals.javauserportal.VmDetails"%>
<html>
<body>
    <%
    if (session.getAttribute("cookie") == null) {
        response.sendRedirect("index.jsp");
    }

    UserVmsRestCommand command = new UserVmsRestCommand(session.getAttribute("baseUrl") + "/api/vms", (String)session.getAttribute("cookie"));
    RestClient client = new RestClient();
    client.doGetCommand(command);
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
            <th>Launch</th>
        </tr>
        <%
            for (VmDetails vm: command.getVms()) {
        %>
        <tr>
            <td><%= vm.getName() %></td>
            <td><%= vm.getStatus() %></td>
            <td><%= vm.getDisplay() %></td>
            <td><button %s onclick=javascript:location.href='action.jsp?vmid=<%= vm.getId() %>&action=start' type='button'>Start</button></td>
            <td><button %s onclick=javascript:location.href='action.jsp?vmid=<%= vm.getId() %>&action=stop' type='button'>Stop</button></td>
            <td><button %s onclick=javascript:location.href='action.jsp?vmid=<%= vm.getId() %>&action=ticket' type='button'>Launch</button></td>
        </tr>
        <%
            }
        %>
    </table>

    </center>
</body>
</html>
