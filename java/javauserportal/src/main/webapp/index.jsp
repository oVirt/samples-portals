<%@page import="org.ovirt.samples.portals.javauserportal.OVirtSDKWrapper"%>
<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%@page import="org.ovirt.samples.portals.javauserportal.OVirtProperties"%>
<html>
<body>
    <form name="input" action="index.jsp" method="post">
        <%
        String message = "";
        session.setAttribute("wrapper", null);

        if (request.getParameter("username") != null && request.getParameter("password") != null) {
            OVirtProperties prop = new OVirtProperties();
            session.setAttribute("baseUrl", prop.getBaseUrl());
            OVirtSDKWrapper wrapper = new OVirtSDKWrapper();
            session.setAttribute("wrapper", wrapper);

            wrapper.login(prop.getBaseUrl() + "/api", request.getParameter("username"), request.getParameter("password"));
            if (wrapper.isLoggedin()) {
                response.sendRedirect("uservms.jsp");
            }
            else {
                message = "Login Error<br/>(" + wrapper.getMessage() + ")";
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
