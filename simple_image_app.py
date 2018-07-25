#!/home/admin/ansible/Python-2.7.13/bin/python2.7

# code to support ONIE image discovery 
# We will be using ONIE's http header, see example:
#ONIE-SERIAL-NUMBER:
#ONIE-ETH-ADDR: F4:8E:38:56:55:F6
#ONIE-VENDOR-ID: 674
#ONIE-MACHINE: dell_s4000_c2338
#ONIE-MACHINE-REV: 0
#ONIE-ARCH: x86_64
#ONIE-SECURITY-KEY:
#ONIE-OPERATION: os-install
#ONIE-VERSION: 3.21.1.1

import SimpleHTTPServer
import SocketServer
import logging
import sys
import simple_sql as q

REPO_DEFAULT = "images"

PORT = 80

#Update the pathname of to the NOS
def update_path(handler,image):
     print("NOS found %s " % image)
     new_path = "/%s/%s" % (REPO_DEFAULT,image);
     print("Redirecting http request from %s  to %s" % (handler.path,new_path));
     handler.path = new_path;
   
class GetHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    """
     A class to handle ONIE requests in the following order.
     ONIE Request and ONIE install mode is on ?
      a: Update image request based ONIE-ETH-ADDR.
      b: If a fails, Update image request based ONIE-MACHINE.
      c: If a and b fails, do nothing.
     finally
      return request
    """

    def do_GET(self):
        print(self.headers);
        isOnieEth = self.headers.get("ONIE-ETH-ADDR",False);
        isOnieInstall = self.headers.get("ONIE-OPERATION",False);
        isOnieMachine = self.headers.get("ONIE-MACHINE",False);
          
        print("Request in isOnieEth:{} isOnieInstall:{} isOnieMachine:{}".format(isOnieEth,isOnieInstall,isOnieMachine))
	# ONIE
        if(isOnieEth and str(isOnieInstall)=="os-install"):
           
	    # for a given switch find the correct image,
	    d1 =  q.get_deviceID(str(isOnieEth))
            d2 =  q.get_deviceID(str(isOnieMachine))
	    if d1:
                update_path(self,d1.image)
            elif d2:
                update_path(self,d2.image)    
            else:
                logging.error("Sorry, we could not find a NOS for %s!" % isOnieEth)
        SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self);


    def end_headers(self):
        self.send_my_headers()
        SimpleHTTPServer.SimpleHTTPRequestHandler.end_headers(self)

    def send_my_headers(self):
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")


Handler = GetHandler
httpd = SocketServer.TCPServer(("", PORT), Handler)

httpd.serve_forever()
