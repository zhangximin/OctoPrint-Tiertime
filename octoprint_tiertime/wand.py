# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import json
import logging
import os
import threading
import time
from pathlib import Path
from threading import Thread
import websocket

__author__ = "Simon Cheung <simon@tiertime.net>"
__license__ = "GNU Affero General Public License http://www.gnu.org/licenses/agpl.html"


class tiertime_printer_item:
    def __init__(
        self, SN, linkedType, connected, printerName, printerType, systemType, accessCtrl
    ):
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
    def __init__(
        self,
        SN,
        basePlatTemp,
        curHeight,
        curLayer,
        heaterOn,
        materialName,
        materialWeight,
        motorPositionW,
        motorPositionX,
        motorPositionY,
        motorPositionZ,
        nNozzleNum,
        nTargetPlatTemp,
        nTargetTemp1,
        nTargetTemp2,
        nozzleTemp1,
        nozzleTemp2,
        printerStatus,
        printing,
        remainPercent,
        remainTime,
        strPrinterStatus,
    ):
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
        self._nNozzleNum = nNozzleNum
        self._nTargetPlatTemp = nTargetPlatTemp
        self._nTargetTemp1 = nTargetTemp1
        self._nTargetTemp2 = nTargetTemp2
        self._nozzleTemp1 = nozzleTemp1
        self._nozzleTemp2 = nozzleTemp2
        self._printerStatus = printerStatus
        self._printing = printing
        self._remainPercent = remainPercent
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
    def nNozzleNum(self):
        return self._nNozzleNum

    @nNozzleNum.setter
    def nNozzleNum(self, nNozzleNum):
        self._nNozzleNum = nNozzleNum

    @property
    def nTargetPlatTemp(self):
        return self._nTargetPlatTemp

    @nTargetPlatTemp.setter
    def nTargetPlatTemp(self, nTargetPlatTemp):
        self._nTargetPlatTemp = nTargetPlatTemp

    @property
    def nTargetTemp1(self):
        return self._nTargetTemp1

    @nTargetTemp1.setter
    def nTargetTemp1(self, nTargetTemp1):
        self._nTargetTemp1 = nTargetTemp1

    @property
    def nTargetTemp2(self):
        return self._nTargetTemp2

    @nTargetTemp2.setter
    def nTargetTemp2(self, nTargetTemp2):
        self._nTargetTemp2 = nTargetTemp2

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
    def remainPercent(self):
        return self._remainPercent

    @remainPercent.setter
    def remainPercent(self, remainPercent):
        self._remainPercent = remainPercent

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
    _settings = None

    def __init__(self, settings, identifier):
        if self._ws_socket is not None:
            return self

        self._joblist = None
        self._isPrinting = False
        self._lastError = None
        self._upload_sn = 0
        self._upload_progress = 0
        self._upload_jobid = 0
        self._identifier = identifier
        self._timeout = 10
        self._busy = False
        self._if_refreshPrinters = False

        self._settings = settings
        self.connecting = False
        self.thread = None
        self.StartTime = None
        self.inter = None
        self.lock = threading.Lock()
        self.printer_list = None
        self.printer_status_list = None

        self._logger = logging.getLogger("octoprint.plugins.tiertime.wandServer")

    def on_error(self, ws, error):
        self.connecting = False
        self._lastError = error
        self._logger.critical("-------Error----------")
        self._logger.critical(error)
        if self._ws_socket is not None:
            self._ws_socket.close()
            self._ws_socket = None

    def on_open(self, ws):
        self._logger.info("Connected with wand server ...")
        self.connecting = False

    def on_close(self, ws):
        self._ws_socket = None

    def on_message(self, ws, message):
        try:
            dataJson = json.loads(message)
            if "reply" in dataJson:
                func = dataJson["receipted"]["cmd"]
                if func == "exec":
                    func = dataJson["receipted"]["action"]
                if dataJson["reply"]["status"] != 2:
                    getattr(self, "cb_" + func)(dataJson)
                # else:
                #     self._logger.critical(
                #         "Receiveing unknown reponses from WandServer error!" + 
                #         json.dumps(dataJson, sort_keys=True, indent=4, separators=(",", ": "))
                #     )

        except ValueError:
            self._logger.critical("Error response from WandServer!")
            self._logger.critical(message)
        except Exception as e:
            self._logger.critical("Processing reponse from WandServer error!")
            self._logger.critical(e)

    def close(self):
        self.connecting = False
        if self._ws_socket is not None:
            self._ws_socket.close()

    def connect(self):
        if not self.connecting:
            self._logger.info("Connecting to " + self._settings.get(["wand_host"]))
            self.connecting = True
            self._ws_socket = websocket.WebSocketApp(self._settings.get(["wand_host"]),
                on_open=lambda ws : self.on_open(ws),
                on_message=lambda ws, message : self.on_message(ws, message),
                on_error=lambda ws, error : self.on_error(ws, error),
                on_close=lambda ws : self.on_close(ws))
            self.thread = Thread(
                target=self._ws_socket.run_forever, args=(None, None, 60, 30)
            )
            self.thread.start()

    def send_command(self, cmd):
        if self._ws_socket is None:
            self.connect()

        if self._ws_socket is not None and not self.connecting:
            self._ws_socket.send(cmd)

    def get_job_list(self, sn):
        self._waitting = True
        self.send_command('{"cmd":"exec","sn":"' + sn + '","action":"joblist"}')

        counter = 0
        while counter < self._timeout and self._waitting:
            time.sleep(1)
            counter += 1

        return self._joblist

    def cb_joblist(self, obj):
        # self._logger.info(
        #     "cb_joblist :"
        #     + json.dumps(obj, sort_keys=True, indent=4, separators=(",", ": "))
        # )
        status = obj["reply"]["status"]
        # sn = str(obj["receipted"]["sn"])
        if status is not None:
            if status == 0:
                self._joblist = obj["reply"]["result"]
            else:
                self._joblist = None
        self._waitting = False

    def start_job(self, sn, jobid):
        if not self._isPrinting:
            self._isPrinting = False
            self._lastError = None
            self.send_command(
                '{"cmd":"exec","sn":"'
                + sn
                + '","action":"jobprepareprint","jobid":'
                + str(jobid)
                + "}"
            )

    def cb_jobprepareprint(self, obj):
        status = obj["reply"]["status"]
        msg = obj["reply"]["message"]
        if status == 0:
            self._isPrinting = True
        elif status < 0:
            self._isPrinting = False
            self._lastError = msg
            self._logger.error("Start job error:" + msg)

    def init_printer(self, sn):
        status = self.get_printer_status(sn)
        # printing/2 or paused/3
        if status is not None and status.printerStatus != 2 and status.printerStatus != 3:
            self.send_command('{"cmd":"exec","sn":"' + sn + '","action":"initprinter"}')

    def cb_initprinter(self, obj):
        status = obj["reply"]["status"]
        if status != 0 and status != 2:
            self._lastError = obj["reply"]["message"]

    def resume_print(self, sn, jobid):
        tPrinter = self.get_printer_status(sn)
        if tPrinter is not None and tPrinter.printerStatus == 3:
            self.send_command('{"cmd":"exec","sn":"' + sn + '","action":"resumeprint"}')
        elif tPrinter is not None and tPrinter.printerStatus == 1:
            self.start_job(sn, jobid)
        else:
            self._logger.error("Resume error!")

    def cb_resumeprint(self, obj):
        status = obj["reply"]["status"]
        if status != 0 and status != 2:
            self._lastError = obj["reply"]["message"]

    def pause_print(self, sn):
        self.send_command('{"cmd":"exec","sn":"' + sn + '","action":"pauseprint"}')

    def cb_pauseprint(self, obj):
        status = obj["reply"]["status"]
        if status != 0:
            self._lastError = obj["reply"]["message"]

    def stop_print(self, sn):
        self._isPrinting = False
        self._lastError = None
        self.send_command('{"cmd":"exec","sn":"' + sn + '","action":"stopprint"}')

    def cb_stopprint(self, obj):
        status = obj["reply"]["status"]
        if status != 0:
            self._lastError = obj["reply"]["message"]

    def extrudematerial(self, sn):
        self.send_command('{"cmd":"exec","sn":"' + sn + '","action":"extrudematerial"}')

    def cb_extrudematerial(self, obj):
        self._logger.info(
            "cb_extrudematerial :"
            + json.dumps(obj, sort_keys=True, indent=4, separators=(",", ": "))
        )

    def withdrawmaterial(self, sn):
        self.send_command('{"cmd":"exec","sn":"' + sn + '","action":"withdrawmaterial"}')

    def cb_withdrawmaterial(self, obj):
        self._logger.info(
            "cb_withdrawmaterial :"
            + json.dumps(obj, sort_keys=True, indent=4, separators=(",", ": "))
        )

    # delete from history list if type=1.
    def delete_job(self, sn, jobid, type=0):
        self.send_command(
            '{"cmd":"exec","sn":"'
            + sn
            + '","action":"jobdelete","jobid":'
            + str(jobid)
            + ',"type":'
            + str(type)
            + "}"
        )

    def cb_jobdelete(self, obj):
        status = obj["reply"]["status"]
        if status != 0:
            self._lastError = obj["reply"]["message"]

    def cb_searchallprinters(self, obj):
        self.send_command('{"cmd": "getallprinters"}')

    def remove_printer(self, sn):
        del self.printer_list[sn]

    def cb_getallprinters(self, obj):
        # self._logger.info("cb_getallprinters :" + json.dumps(obj, sort_keys=True, indent=4, separators=(',', ': ')))
        self._if_refreshPrinters = False
        self._busy = False
        result = obj["reply"]["result"]
        netList = result["net"]
        usbList = result["usb"]
        linked = result["linked"]

        try:
            self.lock.acquire()

            if self.printer_list is not None:
                self.printer_list.clear()
            else:
                self.printer_list = {}

            if self.printer_status_list is not None:
                self.printer_status_list.clear()
            else:
                self.printer_status_list = {}

            if len(linked) > 0:
                for linkedPrinter in linked:
                    # self.remove_printer()

                    printer_item = tiertime_printer_item(
                        str(linkedPrinter["serNum"]),
                        linkedPrinter["linkedType"],
                        False,
                        linkedPrinter["printName"],
                        "printType",
                        linkedPrinter["systemType"],
                        str(0),
                    )
                    self.printer_list[str(linkedPrinter["serNum"])] = printer_item

            if len(usbList) > 0:
                for usbPrinter in usbList:
                    printer_item = tiertime_printer_item(
                        str(usbPrinter["serNum"]),
                        "USB",
                        False,
                        usbPrinter["printName"],
                        usbPrinter["printIcon"],
                        usbPrinter["systemType"],
                        str(0),
                    )
                    self.printer_list[str(usbPrinter["serNum"])] = printer_item

            if len(netList) > 0:
                for netPrinter in netList:
                    printer_item = tiertime_printer_item(
                        str(netPrinter["serNum"]),
                        "Ethernet",
                        False,
                        netPrinter["printName"],
                        netPrinter["printType"],
                        netPrinter["systemType"],
                        str(netPrinter["accessCtrl"]),
                    )
                    self.printer_list[str(netPrinter["serNum"])] = printer_item

        finally:
            self.lock.release()

    def uploadfile(self, sn, filename, printTimes=1):
        self._upload_sn = sn
        self._upload_progress = 1

        data = Path(filename).read_bytes()
        data = data.decode("raw_unicode_escape")

        fname = os.path.basename(filename)
        self.send_command(
            'sf:{"cmd": "uploadfile","fileName":"'
            + fname
            + '","taskqueue":0,"printcount":'
            + str(printTimes)
            + "}"
        )
        self.send_command(data)

    def cb_uploadfile(self, obj):
        status = obj["reply"]["status"]
        msg = obj["reply"]["message"]

        if status == 0:
            filepath = obj["receipted"]["filepath"]
            if filepath is not None:
                self.send_command(
                    '{"cmd":"exec","sn":"'
                    + self._upload_sn
                    + '","action":"sendtaskfile","filepaths":["'
                    + filepath
                    + '"],"username":"'
                    + self._identifier
                    + '"}'
                )
        elif status < 0 and msg is not None:
            self._upload_progress = 0
            self._lastError = msg

    def cb_sendtaskfile(self, obj):
        status = obj["reply"]["status"]

        if "result" in obj["reply"]:
            if "nprogress" in obj["reply"]["result"]:
                progress = obj["reply"]["result"]["nprogress"]
        if status == 0:
            self._upload_sn = 0
            self._upload_progress = 0
            if "jobid" in obj["reply"]["result"]:
                self._upload_jobid = obj["reply"]["result"]["jobid"]
                self._isPrinting = True
            self._lastError = "File uploaded successfully."
        elif status == 3 and progress is not None:
            self._upload_progress = progress
        else:
            msg = obj["reply"]["message"]
            self._upload_sn = 0
            self._upload_progress = 0
            if msg is not None:
                self._lastError = msg

    def cb_autoheight(self, obj):
        self._logger.info(
            "cb_autoheight :"
            + json.dumps(obj, sort_keys=True, indent=4, separators=(",", ": "))
        )

    def cb_printmodel(self, obj):
        self._logger.info(
            "cb_printmodel :"
            + json.dumps(obj, sort_keys=True, indent=4, separators=(",", ": "))
        )

    def cb_warning(self, sobj):
        obj = json.loads(sobj)
        reply = obj["reply"]
        otherMsg = reply["other"]
        otherMsg = otherMsg if otherMsg.length > 1 else reply["status"]
        msg = reply["message"] + " [ " + otherMsg + " ] "
        # Need to show in OctoPrint error status.
        self._lastError = msg
        self._logger.warning(msg)

    def get_printer(self, sn) -> tiertime_printer_item:
        # reValue = None
        # try:
        #     self.lock.acquire()

        #     reValue = self.printer_list.get(sn, None)
        #     counter = 0
        #     while reValue is None and counter < 5:
        #         time.sleep(1)
        #         reValue = self.printer_list.get(sn, None)
        #         counter += 1
        # finally:
        #     self.lock.release()

        # return reValue
        return self.printer_list.get(sn, None)

    def connect_tier_printer(self, sn):
        counter = 0
        while self._if_refreshPrinters and counter < 20:
            time.sleep(1)
            counter += 1

        self._lastError = None
        self._upload_sn = sn
        tPrinter = self.get_printer(sn)
        if tPrinter is not None:
            if tPrinter.linkedType == "USB":
                self._busy = True
                self.send_command('{"cmd": "usbconnect", "sn": "' + sn + '", "pwd":""}')
            elif tPrinter.linkedType == "Ethernet":
                self._busy = True
                self.send_command('{"cmd": "netconnect", "sn": "' + sn + '", "pwd": ""}')
            else:
                self._logger.info("Already Connected.")

    def cb_netconnect(self, obj):
        # self._logger.info(
        #     "cb_netconnect :"
        #     + json.dumps(obj, sort_keys=True, indent=4, separators=(",", ": "))
        # )
        self._busy = False
        status = obj["reply"]["status"]
        msg = obj["reply"]["message"]
        # sn = str(obj["receipted"]["sn"])
        if status != 0:
            self._lastError = msg
        self.refreshPrinters()

    def cb_usbconnect(self, obj):
        self._busy = False
        status = obj["reply"]["status"]
        msg = obj["reply"]["message"]
        sn = str(obj["receipted"]["sn"])
        if status == 0:
            self.refreshPrinterStatus()
        else:
            self._lastError = msg
            self.remove_printer(sn)

    def get_tier_printer_status(self, sn):
        tPrinter = self.get_printer(sn)
        if tPrinter is not None:
            self.send_command('{"cmd": "getprintstatus", "sn": "' + sn + '"}')

    def cb_getprintstatus(self, obj):
        self._logger.info(
            "cb_getprintstatus :"
            + json.dumps(obj, sort_keys=True, indent=4, separators=(",", ": "))
        )

    def disconnect_tier_printer(self, sn):
        # tPrinter = self.get_printer(sn)
        # if tPrinter is not None:
        #     self.send_command("{\"cmd\": \"disconnect\", \"sn\": \""+sn+"\"}")
        # else:
        #     self._logger.info("disconnect_tier_printer: Printer not found! sn:" + str(sn))

        # Only remove status from local.
        self.remove_printer_status(sn)

    def cb_disconnect(self, obj):
        status = obj["reply"]["status"]
        sn = str(obj["receipted"]["sn"])
        if status is not None:
            if status != 0:
                self.remove_printer_status(sn)

    def motors_off(self, sn):
        self._isPrinting = False
        self._lastError = None
        self.send_command('{"cmd":"exec","sn":"' + sn + '","action":"motorstop"}')

    def cb_motorstop(self, obj):
        status = obj["reply"]["status"]
        if status != 0:
            self._lastError = obj["reply"]["message"]

    def remove_printer_status(self, sn):
        del self.printer_status_list[sn]

    def get_printer_status(self, sn) -> tiertime_printer_status_item:
        reValue = None
        try:
            self.lock.acquire()

            reValue = self.printer_status_list.get(sn, None)
            counter = 0
            while reValue is None and counter < 5:
                time.sleep(1)
                reValue = self.printer_status_list.get(sn, None)
                counter += 1
        finally:
            self.lock.release()

        return reValue

    def get_printer_extruderCount(self, sn) -> int:
        t_status = self.get_printer_status(sn)
        if t_status is not None:
            # return 2 if "/" in t_status.materialName else 1
            return t_status.nNozzleNum
        return 1

    def get_extruder_temperature(self, sn, extruderIndex) -> float:
        t_status = self.get_printer_status(sn)
        if t_status is not None:
            temp = float(getattr(t_status, "nozzleTemp" + str(extruderIndex + 1), 0.0))
            if temp > 0 and temp < 10:
                temp = (
                    float(getattr(t_status, "nTargetTemp" + str(extruderIndex + 1), 0.0))
                    * temp
                )
            return temp
        return -1

    def get_bed_temperature(self, sn) -> float:
        t_status = self.get_printer_status(sn)
        if t_status is not None:
            temp = float(t_status.basePlatTemp)
            if temp > 0 and temp < 10:
                temp = t_status.nTargetPlatTemp * temp
            return temp
        return -1

    def get_printe_progress(self, sn):
        t_status = self.get_printer_status(sn)
        if t_status is not None and t_status.printing:
            reValue = getattr(t_status, "remainPercent", 0)
            if reValue == 0 and getattr(t_status, "printerStatus", 0) == 6:
                self._isPrinting = False
            elif getattr(t_status, "printerStatus", 0) == 2:
                self._isPrinting = True
            if reValue == 0:
                reValue = 0.1
            return reValue
        return 0

    def refreshPrinters(self):
        if not self._if_refreshPrinters:
            self.t_refreshPrinters()

    def t_refreshPrinters(self):
        self._if_refreshPrinters = True
        self._busy = True
        self.send_command('{"cmd": "searchallprinters"}')

    def refreshPrinterStatus(self):
        self.send_command('{"cmd": "getallprintstatus"}')

    def cb_getallprintstatus(self, obj):
        # self._logger.info(
        #     "cb_getallprintstatus :"
        #     + json.dumps(obj, sort_keys=True, indent=4, separators=(",", ": "))
        # )
        # JobList
        # jobs = obj["reply"]["result"]["jobs"]
        # No implemention yet. 20210615

        statusArray = obj["reply"]["result"]["status"]
        for n in range(0, len(statusArray)):
            serNum = str(statusArray[n]["sn"])
            printer_status_item = tiertime_printer_status_item(
                serNum,
                statusArray[n]["basePlatTemp"],
                statusArray[n]["curHeight"],
                statusArray[n]["curLayer"],
                statusArray[n]["heaterOn"],
                statusArray[n]["materialName"],
                statusArray[n]["materialWeight"],
                statusArray[n]["motorPositionW"],
                statusArray[n]["motorPositionX"],
                statusArray[n]["motorPositionY"],
                statusArray[n]["motorPositionZ"],
                statusArray[n]["nNozzleNum"],
                statusArray[n]["nTargetPlatTemp"],
                statusArray[n]["nTargetTemp1"],
                statusArray[n]["nTargetTemp2"],
                statusArray[n]["nozzleTemp1"],
                statusArray[n]["nozzleTemp2"],
                statusArray[n]["printerStatus"],
                statusArray[n]["printing"],
                statusArray[n]["remainPercent"],
                statusArray[n]["remainTime"],
                statusArray[n]["strPrinterStatus"],
            )

            try:
                self.lock.acquire()
                self.printer_status_list[serNum] = printer_status_item
            finally:
                self.lock.release()

    ####################################################

    def action(self):
        if not self._busy:
            self.refreshPrinterStatus()

    def start_action(self):
        if self.inter is None:
            self.StartTime = time.time()

            # do action every 4s
            self.inter = setInterval(4, self.action)
            self._logger.debug(
                "just after setInterval -> time : {:.1f}s".format(
                    time.time() - self.StartTime
                )
            )

    def stop_action(self):
        # will stop interval in 5s
        t = threading.Timer(5, self.inter.cancel)
        t.start()


class setInterval:
    def __init__(self, interval, action):
        self.interval = interval
        self.action = action
        self.stopEvent = threading.Event()
        thread = threading.Thread(target=self.__setInterval)
        thread.start()

    def __setInterval(self):
        nextTime = time.time() + self.interval
        while not self.stopEvent.wait(nextTime - time.time()):
            nextTime += self.interval
            self.action()

    def cancel(self):
        self.stopEvent.set()
