#!/usr/bin/python

import pygtk
import gtk
import gtk.glade
import gobject
import time
import sys
import os
import subprocess
from threading import Thread
import dispatcher
import urllib2
import tempfile

global dispatcher
dispatcher = dispatcher.OvirtApi()
VarSaida = True


class Client:
    def Quit(*args, **kwargs):
        global VarSaida
        VarSaida = False
        gtk.main_quit(*args, **kwargs)
        sys.exit()

    def Connect(self, button=None):
        selected_vm = self._cmb_main_vms.get_active_text().split(" :: ")[1]
        ticket, expiry = dispatcher.ticketVm(selected_vm)

        port = "port="+str(self._port)+"&" if self._port else ""
        sport = "tls-port="+str(self._sport)+"&" if self._sport else ""
        uri = "spice://%s/?%s%spassword=%s" % (self._host,
                                               port,
                                               sport,
                                               ticket)
        cmd = ["spicy", "--uri", uri]

        if self._ca_file is not None:
            cmd.append("--spice-ca-file=%s" % self._ca_file)

        subprocess.Popen(cmd)

    def Auth(self, button=None):
        url = self._ent_auth_server.get_text()
        cert_path = "/ovirt-engine/ca.crt"
        username = self._ent_auth_user.get_text()
        password = self._ent_auth_pass.get_text()

        try:
            cert = urllib2.urlopen(url+cert_path).read()
            cert_file = tempfile.NamedTemporaryFile(delete=False)
            cert_file
            cert_file.write(cert)
            cert_file.close()

            self._ca_file = cert_file.name
        except:
            self._sta_main.push(0, "CA certificate not found in %s%s" %
                                (url, cert_path))
            self._ca_file = None

        login, msg = dispatcher.login(url,
                                      username,
                                      password,
                                      self._ca_file)

        if login:
            self._sta_main.push(0, "User %s logged in" % username)
            self._window1.hide()
            self._window2.show()
            self.List()
            t = Thread(target=self.Status)
            t.start()
        else:
            self._sta_auth.push(0, msg)

    def List(self, button=None):
        self._liststore.clear()
        for vm in dispatcher.getUserVms():
            self._liststore.append([vm.name + " :: " + vm.id])

        self._cmb_main_vms.set_active(0)

    def Status(self, button=None):
        global VarSaida
        while VarSaida:
            selected_vm = self._cmb_main_vms.get_active_text().split(" :: ")[1]
            vm = dispatcher.getVmById(selected_vm)
            state = vm.status.state
            vcpus = vm.cpu.topology
            memory = vm.memory
            os = vm.os.type_
            if vm.usb.enabled:
                usb = "Enabled"
            else:
                usb = "Disabled"

            display = vm.get_display()
            self._port = display.get_port()
            self._sport = display.get_secure_port()
            self._host = display.get_address()

            self._btn_main_refresh.set_sensitive(True)
            self._lab_Smp.set_text(str(vcpus.cores * vcpus.sockets))
            self._lab_Memory.set_text(str(memory / (1024*1024)))
            self._lab_Display.set_text(vm.display.type_)
            self._lab_Usb.set_text(usb)
            self._lab_Status.set_text(state)

            if "rhel" in os:
                self._img_So.set_from_file(self._dir + "/images/rhel.png")
            elif "sles" in os:
                self._img_So.set_from_file(self._dir + "/images/sles.png")
            elif "ubuntu" in os:
                self._img_So.set_from_file(self._dir + "/images/ubuntu.png")
            elif "other_linux" in os:
                self._img_So.set_from_file(self._dir + "/images/linux.png")
            elif "windows" in os:
                self._img_So.set_from_file(self._dir + "/images/win.png")
            else:
                self._img_So.set_from_file(self._dir + "/images/ovirt.png")

            if state == "up" or state == "powering_up":
                self._checkbutton1.set_sensitive(True)
                self._cmb_main_vms.set_sensitive(True)
                self._btn_main_refresh.set_sensitive(True)
                self._btn_main_start.set_sensitive(False)
                self._btn_main_stop.set_sensitive(True)
                self._btn_main_connect.set_sensitive(True)
            else:
                self._checkbutton1.set_sensitive(True)
                self._cmb_main_vms.set_sensitive(True)
                self._btn_main_refresh.set_sensitive(True)
                self._btn_main_start.set_sensitive(True)
                self._btn_main_stop.set_sensitive(False)
                self._btn_main_connect.set_sensitive(False)

            time.sleep(2)

    def Start(self, button=None):
        selected_vm = self._cmb_main_vms.get_active_text().split(" :: ")[1]
        start, msg, details = dispatcher.startVm(selected_vm)
        if start:
            self._sta_main.push(0, "Success starting VM")
        else:
            self._sta_main.push(0, "%s: %s" % (msg, details))

    def Stop(self, button=None):
        selected_vm = self._cmb_main_vms.get_active_text().split(" :: ")[1]
        stop, msg, details = dispatcher.stopVm(selected_vm)
        if stop:
            self._sta_main.push(0, "Success stopping VM")
        else:
            self._sta_main.push(0, "%s: %s" % (msg, details))

    def __init__(self):
        gtk.gdk.threads_init()
        self._dir = os.path.dirname(os.path.abspath(__file__))
        self._gladefile = "%s/%s" % (self._dir, "userportalgtk.glade")
        self._wTree = gtk.glade.XML(self._gladefile)

        self._window1 = self._wTree.get_widget("window1")
        self._window2 = self._wTree.get_widget("window2")
        if (self._window1):
            self._window1.connect("destroy", self.Quit)
        if (self._window2):
            self._window2.connect("destroy", self.Quit)

        self._btn_auth_ok = self._wTree.get_widget("button1")
        self._btn_auth_cancel = self._wTree.get_widget("button2")
        self._ent_auth_user = self._wTree.get_widget("entry1")
        self._ent_auth_pass = self._wTree.get_widget("entry2")
        self._ent_auth_server = self._wTree.get_widget("entry3")
        self._sta_auth = self._wTree.get_widget("statusbar1")
        self._sta_main = self._wTree.get_widget("statusbar2")

        self._lab_Smp = self._wTree.get_widget("label7")
        self._lab_Memory = self._wTree.get_widget("label9")
        self._lab_Display = self._wTree.get_widget("label11")
        self._lab_Usb = self._wTree.get_widget("label13")
        self._lab_Status = self._wTree.get_widget("label15")

        self._img_So = self._wTree.get_widget("image1")

        self._btn_main_refresh = self._wTree.get_widget("button3")
        self._btn_main_start = self._wTree.get_widget("button4")
        self._btn_main_connect = self._wTree.get_widget("button5")
        self._btn_main_stop = self._wTree.get_widget("button6")
        self._checkbutton1 = self._wTree.get_widget("checkbutton1")

        self._cmb_main_vms = self._wTree.get_widget("combobox1")
        self._liststore = gtk.ListStore(gobject.TYPE_STRING)
        self._cmb_main_vms.set_model(self._liststore)
        cell = gtk.CellRendererText()
        self._cmb_main_vms.pack_start(cell, True)
        self._cmb_main_vms.add_attribute(cell, 'text', 0)

        self._btn_main_refresh.connect("clicked", self.List)
        self._btn_main_start.connect("clicked", self.Start)
        self._btn_main_stop.connect("clicked", self.Stop)
        self._btn_main_connect.connect("clicked", self.Connect)

        self._btn_auth_ok.connect("clicked", self.Auth)
        self._btn_auth_cancel.connect("clicked", self.Quit)

        self._window1.show()


if __name__ == "__main__":
        hwg = Client()
        gtk.main()
