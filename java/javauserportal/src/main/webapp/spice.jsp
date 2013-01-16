<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<%@page import=" org.ovirt.engine.sdk.entities.Ticket"%>
<%@page import="org.ovirt.samples.portals.javauserportal.OVirtSDKWrapper"%>
<%@page import="org.ovirt.engine.sdk.decorators.VM"%>
<html>
<head>
    <%
        if (session.getAttribute("wrapper") == null ||
            session.getAttribute("ticket")  == null) {
            response.sendRedirect("index.jsp");
        }
        Ticket ticket = (Ticket)session.getAttribute("ticket");
        session.removeAttribute("ticket");
        OVirtSDKWrapper wrapper = (OVirtSDKWrapper)session.getAttribute("wrapper");
        VM vm = wrapper.getVmById(request.getParameter("vmid"));

    %>

    <script type="text/javascript">
    if (window.addEventListener) { // Firefox
        window.addEventListener('load', WindowLoad, false);
    } else if (window.attachEvent) { // IE
        window.attachEvent('onload', WindowLoad);
    }

    function WindowLoad(event) {
        spice.hostIP = '<%=  vm.getDisplay().getAddress() %>';
        spice.port = '<%= vm.getDisplay().getPort() %>';
        spice.Password = '<%= ticket.getValue() %>';
        spice.connect();
        spice.show()
    }
    </script>
</head>

<body>
    <button onclick=javascript:location.href='uservms.jsp'>Back</button>
    <%
    if (request.getHeader("user-agent").toLowerCase().contains("windows")) {
    %>
    <object style='visibility: hidden' codebase='SpiceX.cab#version=1,0,0,1' ID='spice' CLASSID='CLSID:ACD6D89C-938D-49B4-8E81-DDBD13F4B48A'/>
    <%  } else { %>
    <embed id='spice' type="application/x-spice" width=0 height=0/>
    <%  } %>
</body>
</html>
