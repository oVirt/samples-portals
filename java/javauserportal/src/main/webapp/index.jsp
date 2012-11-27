<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%@page import="org.ovirt.samples.portals.javauserportal.OVirtProperties"%>
<%@page import="org.ovirt.samples.portals.javauserportal.RestCommand"%>
<%@page import="org.ovirt.samples.portals.javauserportal.LoginRestCommand"%>
<%@page import="org.ovirt.samples.portals.javauserportal.RestClient"%>
<html>
<body>
    <form name="input" action="index.jsp" method="post">
        <%
        String username = "";
        String message = "";

        if (request.getParameter("username") != null && request.getParameter("password") != null) {
            session.removeAttribute("cookie");
            OVirtProperties prop = new OVirtProperties();
            session.setAttribute("baseUrl", prop.getBaseUrl());

            LoginRestCommand command = new LoginRestCommand(prop.getBaseUrl() + "/api", request.getParameter("username"), request.getParameter("password"));
            RestClient client = new RestClient();
            client.doGetCommand(command);
            if (command.isLoggedin()) {
                session.setAttribute("cookie", command.getCookie());
                response.sendRedirect("uservms.jsp");
            }
            else {
                message = "Login Error<br/>(" + command.getMessage() + ")";
            }
        }

        %>
        <center>
            <br/><br/>
            <table>
                <tr>
                    <td>User name:</td>
                    <td><input type="text" name="username" /></td>
                <tr>
                    <td>Password:</td>
                    <td><input type="password" name="password" /></td>
                <tr>
                    <td/>
                    <td align="right"><input type="submit" value="Login"/></td>
                </tr>
            </table>
            <p style='color:red;'><%= message %></p>
        </center>
    </form>
</body>
</html>
