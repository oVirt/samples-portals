<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<%@page import="org.ovirt.samples.portals.javauserportal.ActionRestCommand"%>
<%@page import="org.ovirt.samples.portals.javauserportal.VmByIdRestCommand"%>
<%@page import="org.ovirt.samples.portals.javauserportal.RestCommand"%>
<%@page import="org.ovirt.samples.portals.javauserportal.RestClient"%>
<html>
<body>
    <%
    if (session.getAttribute("cookie") == null) {
        response.sendRedirect("index.jsp");
    }

    ActionRestCommand command = new ActionRestCommand(session.getAttribute("baseUrl") + "/api/vms/" +
            request.getParameter("vmid") + "/" + request.getParameter("action"),
            (String)session.getAttribute("cookie"));
    RestClient client = new RestClient();
    client.doPostCommand(command);
    %>
    <%
    if (command.getFailReason() != null) {
    %>
        <p style='color:red'>Action failed!</p>
        <br/>Reason: <%= command.getFailReason() %>
        <br/>Details:<%= command.getFailDetails() %>
        <br/>
        <button onclick=javascript:history.back()>Back</button>
    <%
    } else if (command.getUrl().contains("ticket")) {
        VmByIdRestCommand vmCommand = new VmByIdRestCommand(session.getAttribute("baseUrl") + "/api/vms/" +
                request.getParameter("vmid"),
                (String)session.getAttribute("cookie"));
        client.doGetCommand(vmCommand);

        if (request.getHeader("user-agent").toLowerCase().contains("windows")) {
    %>
       <OBJECT style='visibility: hidden' codebase='SpiceX.cab#version=1,0,0,1' ID='spice' CLASSID='CLSID:ACD6D89C-938D-49B4-8E81-DDBD13F4B48A'>
       </OBJECT>
       <script>
       function onConnect() {
           spice.HostIP = '<%= vmCommand.getVmDetails().getAddress() %>'
           spice.Port = '<%= vmCommand.getVmDetails().getPort() %>'
           spice.Password = '<%= command.getTicketValue() %>'
           spice.Connect();
       }
       </script>

        <form>
            <input type=button onclick='javascript:onConnect();' value='Connect'/>
        </form>
        <br/>
        <button onclick=javascript:location.href='uservms.jsp'>Back</button>
    <%
        } else {
    %>
        <script>
           function onConnect() {
               spice.hostIP = '<%= vmCommand.getVmDetails().getAddress() %>';
               spice.port = '<%= vmCommand.getVmDetails().getPort() %>';
               spice.Password = '<%= command.getTicketValue() %>';
               spice.connect();
               spice.show()
           }
        </script>
        <embed id='spice' type="application/x-spice" width=0 height=0><br>
        <form>
            <input type=button value='Connent' onclick='onConnect()'/>
        </form>
        <br/>
        <button onclick=javascript:location.href='uservms.jsp'>Back</button>
    <%
        }
    }
    else {
    %>
    Action success
    <br/>
    <button onclick=javascript:location.href='uservms.jsp'>Back</button>
    </body></html>
    <%
    }
    %>
</body>
</html>
