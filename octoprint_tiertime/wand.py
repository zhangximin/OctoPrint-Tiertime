# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
from logging import debug
from octoprint.vendor.sockjs.tornado import static
from threading import Thread
from octoprint.vendor.sockjs.tornado.proto import MESSAGE
__author__ = "Simon Cheung <simon@tiertime.net>"
__license__ = "GNU Affero General Public License http://www.gnu.org/licenses/agpl.html"

import io
import json

import websocket
import _thread
import threading
import time

class tiertime_printer_item :
    
    def __init__(self, SN, linkedType, connected, printerName, printerType, systemType, accessCtrl) :
        self._SN = SN
        self._linkedType = linkedType
        self._connected = connected
        self._printerName = printerName        
        self._printerType = printerType
        self._systemType = systemType
        self._accessCtrl = accessCtrl

    @property
    def SN(self):
        return self._SN

    @property
    def linkedType(self):
        return self._linkedType
    @linkedType.setter
    def linkedType(self, linkedType):
        self._linkedType = linkedType

    @property
    def connected(self):
        return self._connected
    @connected.setter
    def connected(self, connected):
        self._connected = connected
    
    @property
    def printerName(self):
        return self._printerName
    @printerName.setter
    def printerName(self, printerName):
        self._printerName = printerName

    @property
    def printerType(self):
        return self._printerType

    @property
    def systemType(self):
        return self._systemType
    @systemType.setter
    def systemType(self, systemType):
        self._systemType = systemType

    @property
    def accessCtrl(self):
        return self._accessCtrl
    
class tiertime_printer_status_item:
    def __init__(self, SN, basePlatTemp, curHeight, curLayer, 
    heaterOn, materialName, materialWeight, motorPositionW, motorPositionX, 
    motorPositionY, motorPositionZ, nozzleTemp1, nozzleTemp2, 
    printerStatus, printing, remainRercent, remainTime, strPrinterStatus) :
        self._sn = str(SN)
        self._basePlatTemp = basePlatTemp
        self._curHeight = curHeight
        self._curLayer = curLayer
        self._heaterOn = heaterOn
        self._materialName = materialName
        self._materialWeight = materialWeight
        self._motorPositionW = motorPositionW
        self._motorPositionX = motorPositionX
        self._motorPositionY = motorPositionY
        self._motorPositionZ = motorPositionZ
        self._nozzleTemp1 = nozzleTemp1
        self._nozzleTemp2 = nozzleTemp2
        self._printerStatus = printerStatus
        self._printing = printing
        self._remainRercent = remainRercent
        self._remainTime = remainTime
        self._strPrinterStatus = strPrinterStatus

    @property
    def SN(self):
        return self._sn

    @property
    def basePlatTemp(self):
        return self._basePlatTemp
    @basePlatTemp.setter
    def basePlatTemp(self, basePlatTemp):
        self._basePlatTemp = basePlatTemp

    @property
    def curHeight(self):
        return self._curHeight
    @curHeight.setter    
    def curHeight(self, curHeight):
        self._curHeight = curHeight

    @property
    def curLayer(self):
        return self._curLayer
    @curLayer.setter    
    def curLayer(self, curLayer):
        self._curLayer = curLayer

    @property
    def heaterOn(self):
        return self._heaterOn
    @heaterOn.setter    
    def heaterOn(self, heaterOn):
        self._heaterOn = heaterOn

    @property
    def materialName(self):
        return self._materialName
    @materialName.setter    
    def materialName(self, materialName):
        self._materialName = materialName

    @property
    def materialWeight(self):
        return self._materialWeight
    @materialWeight.setter    
    def materialWeight(self, materialWeight):
        self._materialWeight = materialWeight

    @property
    def motorPositionW(self):
        return self._motorPositionW
    @motorPositionW.setter    
    def motorPositionW(self, motorPositionW):
        self._motorPositionW = motorPositionW

    @property
    def motorPositionX(self):
        return self._motorPositionX
    @motorPositionX.setter    
    def motorPositionX(self, motorPositionX):
        self._motorPositionX = motorPositionX

    @property
    def motorPositionY(self):
        return self._motorPositionY
    @motorPositionY.setter    
    def motorPositionY(self, motorPositionY):
        self._motorPositionY = motorPositionY

    @property
    def motorPositionZ(self):
        return self._motorPositionZ
    @motorPositionZ.setter    
    def motorPositionZ(self, motorPositionZ):
        self._motorPositionZ = motorPositionZ

    @property
    def nozzleTemp1(self):
        return self._nozzleTemp1
    @nozzleTemp1.setter    
    def nozzleTemp1(self, nozzleTemp1):
        self._nozzleTemp1 = nozzleTemp1

    @property
    def nozzleTemp2(self):
        return self._nozzleTemp2
    @nozzleTemp2.setter    
    def nozzleTemp2(self, nozzleTemp2):
        self._nozzleTemp2 = nozzleTemp2

    @property
    def printerStatus(self):
        return self._printerStatus
    @printerStatus.setter    
    def printerStatus(self, printerStatus):
        self._printerStatus = printerStatus

    @property
    def printing(self):
        return self._printing
    @printing.setter    
    def printing(self, printing):
        self._printing = printing

    @property
    def remainRercent(self):
        return self._remainRercent
    @remainRercent.setter    
    def remainRercent(self, remainRercent):
        self._remainRercent = remainRercent

    @property
    def remainTime(self):
        return self._remainTime
    @remainTime.setter    
    def remainTime(self, remainTime):
        self._remainTime = remainTime

    @property
    def strPrinterStatus(self):
        return self._strPrinterStatus
    @strPrinterStatus.setter    
    def strPrinterStatus(self, strPrinterStatus):
        self._strPrinterStatus = strPrinterStatus

####################################################

class wandServer:

    _ws_socket = None

    def __init__(self, wand_host):
        if self._ws_socket is not None:
            return self

        self.timeout = 15
        self.wand_host = wand_host        
        self.connecting = False
        self.thread = None
        # setInterval
        self.StartTime = None
        self.inter = None
        self.printer_list = list()
        self.lock = threading.Lock()
        self.printer_status_list = list()
        self._joblist = None
        self._isPrinting = False
        self._lastError = None
        
        import logging

        self._logger = logging.getLogger(
            "octoprint.plugins.tier_printer.wandServer"
        )

        self.connect()

    def on_error(self, _ws_socket, error):
        self._logger.critical("-------Error----------")
        self._logger.critical(error)

    def on_open(self, _ws_socket):
        self._logger.info("Connected with wand server ...")
        self.connecting = False
    
    def on_close(self, _ws_socket):
        self._ws_socket = None

    def on_message(self, _ws_socket, message):        
        try:            
            dataJson = json.loads(message)            
            if "reply" in dataJson:                
                func = dataJson["receipted"]["cmd"]                
                if func == "exec" :
                    func = dataJson["receipted"]["action"]
                if dataJson["reply"]["status"] != 2 :
                    # Debug
                    #self._logger.info('self.cb_' + func + '(\''+json.dumps(dataJson, separators=(',', ': '))+'\')')                    
                    class_method = getattr(self, 'cb_'+func)(dataJson)                    

        except ValueError :
            self._logger.critical("Error response from WandServer!")
            self._logger.critical("-------------------------------")
            self._logger.critical(message)
        except Exception as e:
            self._logger.critical("Processing reponse from WandServer error!")
            self._logger.critical(e)

    def close(self):
        if self.wand_host is not None:
            self._ws_socket.close()

    def connect(self):
        if not self.connecting :
            self._logger.info("Connecting to "+self.wand_host)
            self.connecting = True
            self._ws_socket = websocket.WebSocketApp(self.wand_host,
                                on_open=self.on_open,
                                on_message=self.on_message,
                                on_error=self.on_error,
                                on_close=self.on_close)
            self.thread = Thread(target = self._ws_socket.run_forever , args = (None , None , 60, 30))
            # self._ws_socket.run_forever()
            self.thread.start();
            
    def send_command(self,cmd):        
        if self._ws_socket is None:            
            self.connect()
        
        c = 0
        while c < self.timeout and self.connecting :
            self._logger.debug('Connecting ...')
            time.sleep(1)
            c += 1
        
        if self.connecting :
            # Connecting timeout.
            self._logger.debug("Connecting timeout")
            self.connecting = False
            return

        self._ws_socket.send(cmd)        

    def get_job_list(self, sn):
        self._waitting = True
        self.send_command("{\"cmd\":\"exec\",\"sn\":\""+sn+"\",\"action\":\"joblist\"}")

        counter = 0
        while counter < self.timeout and self._waitting:
            time.sleep(1)
            counter += 1
        
        return self._joblist

    def start_job(self, sn, jobid):
        if not self._isPrinting:
            self._isPrinting = False
            self._lastError = None
            self.send_command("{\"cmd\":\"exec\",\"sn\":\""+sn+"\",\"action\":\"jobprepareprint\",\"jobid\":"+str(jobid)+"}")        

    def	cb_jobprepareprint(self, obj) :
        self._logger.info("cb_jobprepareprint :" + json.dumps(obj, sort_keys=True, indent=4, separators=(',', ': ')))
        status = obj["reply"]["status"]
        msg = obj["reply"]["message"]
        if status == 0:
            self._isPrinting = True
        elif status < 0:
            self._isPrinting = False
            self._lastError = msg
            self._logger.error("Start job error:" + msg)            

    def init_printer(self, sn):
        self.send_command("{\"cmd\":\"exec\",\"sn\":\""+sn+"\",\"action\":\"initprinter\"}")

    def cb_initprinter(self, obj):
        self._logger.info("cb_initprinter :" + json.dumps(obj, sort_keys=True, indent=4, separators=(',', ': ')))

    def resume_print(self, sn, jobid):
        tPrinter = self.get_printer_status(sn)
        if tPrinter is not None and tPrinter.printerStatus == 3:
            self.send_command("{\"cmd\":\"exec\",\"sn\":\""+sn+"\",\"action\":\"resumeprint\"}")
        elif tPrinter is not None and tPrinter.printerStatus == 1:
            self.start_job(sn, jobid)
        else:
            self._logger.error("Resume error!")

    def cb_resumeprint(self, obj):
        self._logger.info("cb_resumeprint :" + json.dumps(obj, sort_keys=True, indent=4, separators=(',', ': ')))

    def pause_print(self, sn):
        self._logger.info("Sendding pause!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        self.send_command("{\"cmd\":\"exec\",\"sn\":\""+sn+"\",\"action\":\"pauseprint\"}")

    def cb_pauseprint(self, obj):
        self._logger.info("cb_pauseprint :" + json.dumps(obj, sort_keys=True, indent=4, separators=(',', ': ')))

    def stop_print(self, sn):
        self._isPrinting = False
        self._lastError = None
        self._logger.info("Sending stopprint!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        self.send_command("{\"cmd\":\"exec\",\"sn\":\""+sn+"\",\"action\":\"stopprint\"}")

    def cb_stopprint(self, obj):
        self._logger.info("cb_stopprint :" + json.dumps(obj, sort_keys=True, indent=4, separators=(',', ': ')))

    def extrudematerial(self, sn):
        self.send_command("{\"cmd\":\"exec\",\"sn\":\""+sn+"\",\"action\":\"extrudematerial\"}")
    def cb_extrudematerial(self, obj):
        self._logger.info("cb_extrudematerial :" + json.dumps(obj, sort_keys=True, indent=4, separators=(',', ': ')))

    def withdrawmaterial(self, sn):
        self.send_command("{\"cmd\":\"exec\",\"sn\":\""+sn+"\",\"action\":\"withdrawmaterial\"}")
    def cb_withdrawmaterial(self, obj):
        self._logger.info("cb_withdrawmaterial :" + json.dumps(obj, sort_keys=True, indent=4, separators=(',', ': ')))

    # delete from history list if type=1.
    def delete_job(self, sn, jobid, type = 0):
        self.send_command("{\"cmd\":\"exec\",\"sn\":\""+sn+"\",\"action\":\"jobdelete\",\"jobid\":"+str(jobid)+",\"type\":"+str(type)+"}")

    def cb_jobdelete(self, obj):
        self._logger.info("cb_jobdelete :" + json.dumps(obj, sort_keys=True, indent=4, separators=(',', ': ')))

    def cb_searchallprinters(self, obj) :
        self._logger.info("cb_searchallprinters :" + json.dumps(obj, sort_keys=True, indent=4, separators=(',', ': ')))
        self.send_command("{\"cmd\": \"getallprinters\"}")

    def remove_printer(self, sn):
        for printer_item in self.printer_list:
            if printer_item.SN == sn:                
                try:
                    self.lock.acquire()
                    self.printer_list.remove(printer_item)
                finally:
                    self.lock.release()
                return
    
    def	cb_getallprinters(self, obj) :
        result = obj["reply"]["result"]
        netList = result["net"]
        usbList = result["usb"]
        linked = result["linked"]

        if len(linked) > 0 :
            for linkedPrinter in linked:
                self.remove_printer(str(linkedPrinter["serNum"]))
                
                printer_item = tiertime_printer_item(str(linkedPrinter["serNum"]),linkedPrinter["linkedType"], False, 
                linkedPrinter["printName"], "printType", linkedPrinter["systemType"], str(0))
                
                try:
                    self.lock.acquire()
                    self.printer_list.append(printer_item)
                finally:
                    self.lock.release()

        if len(usbList) > 0 :
            for usbPrinter in usbList :
                printer_item = tiertime_printer_item(str(usbPrinter["serNum"]),"USB", False, 
                usbPrinter["printName"], usbPrinter["printType"], str(usbPrinter["systemType"]), str(usbPrinter["accessCtrl"]))
                
                try:
                    self.lock.acquire()
                    self.printer_list.append(printer_item)
                finally:
                    self.lock.release()
                
        if len(netList) > 0 :
            for netPrinter in netList :
                printer_item = tiertime_printer_item(str(netPrinter["serNum"]),"Ethernet", False, 
                netPrinter["printName"], netPrinter["printType"], str(netPrinter["systemType"]), str(netPrinter["accessCtrl"]))
                
                try:
                    self.lock.acquire()
                    self.printer_list.append(printer_item)
                finally:
                    self.lock.release()
                
    def cb_uploadfile(self, obj) :
        self._logger.info("cb_uploadfile :" + json.dumps(obj, sort_keys=True, indent=4, separators=(',', ': ')))
        
        reply = obj["reply"]        
        #Debug Need display to OctoPrint info.
        self._logger.info("File uploaded "+reply["message"])
        
    def cb_autoheight(self, obj):        
        self._logger.info("cb_autoheight :" + json.dumps(obj, sort_keys=True, indent=4, separators=(',', ': ')))
    
    def cb_printmodel(self, obj) :
        self._logger.info("cb_printmodel")
        
    def cb_netconnect(self, obj) :        
        self._logger.info("cb_netconnect :" + json.dumps(obj, sort_keys=True, indent=4, separators=(',', ': ')))
        status = obj["reply"]["status"]
        sn = str(obj["receipted"]["sn"])
       
        
    def cb_usbconnect(self, obj) :
        self._logger.info("cb_usbconnect :" + json.dumps(obj, sort_keys=True, indent=4, separators=(',', ': ')))
        status = obj["reply"]["status"]
        sn = str(obj["receipted"]["sn"])
        
    def cb_warning(self, sobj) :
        obj = json.loads(sobj)
        reply = obj["reply"];
        otherMsg = reply["other"]
        otherMsg = otherMsg if otherMsg.length > 1 else reply["status"];
        msg = reply["message"]+" [ "+ otherMsg + " ] ";
        #Need to show in OctoPrint error status.
        #Alert ?
        self._logger.warning(msg)

    def cb_joblist(self, obj):
        self._logger.info("cb_joblist :" + json.dumps(obj, sort_keys=True, indent=4, separators=(',', ': ')))
        status = obj["reply"]["status"]
        sn = str(obj["receipted"]["sn"])
        if status is not None:
            if status == 0:
                self._logger.debug("------------------------")
                self._logger.debug("get joblist from printer.")
                self._joblist = obj["reply"]["result"]
        self._waitting = False

    ################################

    def get_printer(self, sn) -> tiertime_printer_item:        
        for printer_item in self.printer_list:            
            if printer_item.SN == sn:                
                return printer_item
        return None
    
    def connect_tier_printer(self, sn) :
        tPrinter = self.get_printer(sn)
        if tPrinter is not None:
            if tPrinter.linkedType == "USB":                
                self.send_command("{\"cmd\": \"usbconnect\", \"sn\": \""+sn+"\"}")
            elif tPrinter.linkedType == "Ethernet":                
                self.send_command("{\"cmd\": \"netconnect\", \"sn\": \""+sn+"\"}")
            else:
                self._logger.info("Already Connected.")

            # Need waitting for status.
            time.sleep(5)
            
            counter = 0
            while self.get_printer_status(sn) is None and counter < self.timeout:
                time.sleep(1)
                counter += 1

            printer_status = self.get_printer_status(sn)
            if printer_status is not None and printer_status.printerStatus == 0:
                self._logger.info("initializing printer ...... ")
                self.init_printer(sn)
                counter = 0
                # Accouding to the lastest product info UP600, we need 60 seconds to init.
                while printer_status is not None and printer_status.printerStatus < 1 and counter < 60:
                    time.sleep(1)
                    printer_status = self.get_printer_status(sn)
                    counter += 1
                    self._logger.info("initializing printer ...... ")
                if printer_status is not None and printer_status.printerStatus == 1:
                    self._logger.info("Printer initialized.")
                    self._logger.info("--------------")
                    self._logger.info("Printer is READY!")
                else:
                    self._logger.info("Printer initialize error:")
                    self._logger.info("--------------")
                    if printer_status is not None:
                        self._logger.info(str(printer_status.strPrinterStatus) + ":" + printer_status.strPrinterStatus)
    
    def get_tier_printer_status(self, sn) :
        tPrinter = self.get_printer(sn)
        if tPrinter is not None:            
            self.send_command("{\"cmd\": \"getprintstatus\", \"sn\": \""+sn+"\"}")

    def cb_getprintstatus(self, obj):
        self._logger.info("cb_getprintstatus :" + json.dumps(obj, sort_keys=True, indent=4, separators=(',', ': ')))
        
    def disconnect_tier_printer(self, sn) :
        tPrinter = self.get_printer(sn)
        if tPrinter is not None:            
            self.send_command("{\"cmd\": \"disconnect\", \"sn\": \""+sn+"\"}")
        else:
            self._logger.info("disconnect_tier_printer: Printer not found! sn:" + str(sn))

    def cb_disconnect(self, obj):
        self._logger.info("cb_disconnect :" + json.dumps(obj, sort_keys=True, indent=4, separators=(',', ': ')))
        status = obj["reply"]["status"]
        sn = str(obj["receipted"]["sn"])
        if status is not None:
            if status != 0:
                self.remove_printer_status(sn)

    def remove_printer_status(self, sn):
        for printer_status_item in self.printer_status_list:
            if printer_status_item.SN == sn:
                
                try:
                    self.lock.acquire()
                    self.printer_status_list.remove(printer_status_item)
                finally:
                    self.lock.release()
                return

    def get_printer_status(self, sn) -> tiertime_printer_status_item:
        for printer_status_item in self.printer_status_list:
            if printer_status_item.SN == sn:                
                return printer_status_item
        return None

    def get_printer_status_index(self, sn):
        for i in range(len(self.printer_status_list)):
            if self.printer_status_list[i].SN == sn:            
                return i
        return -1

    def get_printer_extruderCount(self, sn) -> int:
        t_status = self.get_printer_status(sn)
        if t_status is not None:
            return 2 if "/" in t_status.materialName else 1        
        return 0

    def get_extruder_temperature(self, sn, extruderIndex) -> float:
        t_status = self.get_printer_status(sn)
        if t_status is not None:            
            return float(getattr(t_status, "nozzleTemp"+str(extruderIndex+1), 0.0))        
        return -1
        
    def get_bed_temperature(self, sn) -> float:
        t_status = self.get_printer_status(sn)
        if t_status is not None:
            return getattr(t_status, "basePlatTemp", 0.0)
        return -1

    #Debug WARNING: remainRercent is made by a Mistake.
    # This should be change to "remainPercent". 20210629
    def get_printe_progress(self, sn):
        t_status = self.get_printer_status(sn)
        if t_status is not None:            
            reValue = getattr(t_status, "remainRercent", 0)
            if reValue == 0 and getattr(t_status, "printerStatus", 0) == 6:
                self._isPrinting = False                
            return reValue
        return 0
        
    def refreshPrinters(self) :
        if self.printer_list is not None:            
            try:
                self.lock.acquire()
                self.printer_list.clear()
            finally:
                self.lock.release()
        else :
            self.printer_list = list();

        if self.printer_status_list is not None:            
            try:
                self.lock.acquire()
                self.printer_status_list.clear()
            finally:
                self.lock.release()
        else :
            self.printer_status_list = list();
        
        self.send_command("{\"cmd\": \"searchallprinters\"}");

    def refreshPrinterStatus(self) :
        self.send_command("{\"cmd\": \"getallprintstatus\"}");

    def	cb_getallprintstatus(self, obj) :
        #self._logger.info("cb_getallprintstatus :" + json.dumps(obj, sort_keys=True, indent=4, separators=(',', ': ')))
        # JobList
        jobs = obj["reply"]["result"]["jobs"];
        # No implemention yet. 20210615
        
        statusArray = obj["reply"]["result"]["status"];
        for n in range(0, len(statusArray)) :
            serNum = str(statusArray[n]["sn"])
            i = self.get_printer_status_index(serNum)
            if i > -1:                
                try:
                    self.lock.acquire()
                    #self._logger.debug("Updating PrinterStatus of : " + serNum + " at index " + str(i))
                    self.printer_status_list[i].basePlatTemp = statusArray[n]["basePlatTemp"]
                    self.printer_status_list[i].curHeight = statusArray[n]["curHeight"]
                    self.printer_status_list[i].curLayer = statusArray[n]["curLayer"]
                    self.printer_status_list[i].heaterOn = statusArray[n]["heaterOn"]
                    self.printer_status_list[i].materialName = statusArray[n]["materialName"]
                    self.printer_status_list[i].materialWeight = statusArray[n]["materialWeight"]
                    self.printer_status_list[i].motorPositionW = statusArray[n]["motorPositionW"]
                    self.printer_status_list[i].motorPositionX = statusArray[n]["motorPositionX"]
                    self.printer_status_list[i].motorPositionY = statusArray[n]["motorPositionY"]
                    self.printer_status_list[i].motorPositionZ = statusArray[n]["motorPositionZ"]
                    self.printer_status_list[i].nozzleTemp1 = statusArray[n]["nozzleTemp1"]
                    self.printer_status_list[i].nozzleTemp2 = statusArray[n]["nozzleTemp2"]
                    self.printer_status_list[i].printerStatus = statusArray[n]["printerStatus"]
                    self.printer_status_list[i].printing = statusArray[n]["printing"]
                    self.printer_status_list[i].remainRercent = statusArray[n]["remainRercent"]
                    self.printer_status_list[i].remainTime = statusArray[n]["remainTime"]
                    self.printer_status_list[i].strPrinterStatus = statusArray[n]["strPrinterStatus"]
                finally:
                    self.lock.release()
            else:
                self._logger.debug("Add PrinterStatus of : " + serNum)
                printer_status_item = tiertime_printer_status_item(serNum, statusArray[n]["basePlatTemp"], statusArray[n]["curHeight"], statusArray[n]["curLayer"],
                    statusArray[n]["heaterOn"], statusArray[n]["materialName"], statusArray[n]["materialWeight"], statusArray[n]["motorPositionW"], statusArray[n]["motorPositionX"],
                    statusArray[n]["motorPositionY"], statusArray[n]["motorPositionZ"], statusArray[n]["nozzleTemp1"], statusArray[n]["nozzleTemp2"],
                    statusArray[n]["printerStatus"], statusArray[n]["printing"], statusArray[n]["remainRercent"], statusArray[n]["remainTime"], statusArray[n]["strPrinterStatus"])
                        
                try:
                    self.lock.acquire()
                    self.printer_status_list.append(printer_status_item)
                finally:
                    self.lock.release()

####################################################

    def action(self) :
        #print('action ! -> time : {:.1f}s'.format(time.time()-self.StartTime))
        self.refreshPrinterStatus()
    
    def start_action(self) :
        #Start ONLY ONE thread.
        if self.StartTime is None:
            self.StartTime=time.time()

            # start action every 4s
            self.inter=setInterval(4,self.action)
            self._logger.debug('just after setInterval -> time : {:.1f}s'.format(time.time()-self.StartTime))

    def stop_action(self) :
        # will stop interval in 4s
        t=threading.Timer(4,self.inter.cancel)
        t.start()

class setInterval :
    def __init__(self,interval,action) :
        self.interval=interval
        self.action=action
        self.stopEvent=threading.Event()        
        thread=threading.Thread(target=self.__setInterval)
        thread.start()

    def __setInterval(self) :
        nextTime=time.time()+self.interval
        while not self.stopEvent.wait(nextTime-time.time()) :
            nextTime+=self.interval
            self.action()

    def cancel(self) :
        self.stopEvent.set()


