import win32serviceutil
import win32service
import win32event
import servicemanager
import logging
import time
from app import app, db
from gevent.pywsgi import WSGIServer
import socket
import webbrowser
 
logging.basicConfig(
    filename='.\\automato-service.log',
    level=logging.DEBUG,
    format='[automato-service] %(levelname)-7.7s %(message)s'
)
 
global http_server
 
class AutomatoSvc(win32serviceutil.ServiceFramework):
    _svc_name_ = "Automato-Service"
    _svc_display_name_ = "Automato Service"
   
    def __init__(self,args):
        win32serviceutil.ServiceFramework.__init__(self,args)
        self.stop_event = win32event.CreateEvent(None,0,0,None)
        socket.setdefaulttimeout(60)
        self.stop_requested = False
 
    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.stop_event)
        logging.info('Stopping service ...')
        http_server.stop()
        self.stop_requested = True
 
    def SvcDoRun(self):
        servicemanager.LogMsg(
            servicemanager.EVENTLOG_INFORMATION_TYPE,
            servicemanager.PYS_SERVICE_STARTED,
            (self._svc_name_,'')
        )
        self.main()
 
    def main(self):
        logging.info('Automato Windows Service Started')
        # Simulate a main loop
        db.create_all()
        logging.info('Starting server')
        global http_server
        http_server = WSGIServer(('0.0.0.0' , 80) , app)
        http_server.serve_forever()
        webbrowser.open_new_tab('localhost')
 
if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(AutomatoSvc)