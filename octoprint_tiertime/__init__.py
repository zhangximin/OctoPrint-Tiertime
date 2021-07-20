# coding=utf-8
from __future__ import absolute_import, unicode_literals, division, print_function

__author__ = "Simon Cheung <simon@tiertime.net>"
__license__ = "GNU Affero General Public License http://www.gnu.org/licenses/agpl.html"
__copyright__ = "Copyright (C) 2021 Tiertime Co. Ltd. - Released under terms of the AGPLv3 License"

import octoprint.plugin
import time
import threading
import logging
import logging.handlers
from os import defpath
from datetime import datetime
from octoprint.logging.handlers import CleaningTimedRotatingFileHandler
from octoprint.printer.estimation import PrintTimeEstimator
from octoprint.settings import settings
from .wand import wandServer
from .tier import TierPrinter

g_ws = None

class TiertimePlugin(octoprint.plugin.SettingsPlugin,    
    octoprint.plugin.TemplatePlugin, octoprint.plugin.RestartNeedingPlugin
):
    def __init__(self):
        global g_ws
        super().__init__()        
        g_ws = None
        self._logger = logging.getLogger(
            "octoprint.plugins.tiertime"
        )
        self._current_sn = 0
        self._serial_obj = None

    def get_template_configs(self):
        return [{"type": "settings", "custom_bindings": False}]
    
    def get_settings_defaults(self):
        return {
            "enabled": False,
            "okAfterResend": False,
            "forceChecksum": False,
            "numExtruders": 1,
            "pinnedExtruders": None,
            "includeCurrentToolInTemps": True,
            "includeFilenameInOpened": False,
            "hasBed": True,
            "hasChamber": False,
            "repetierStyleTargetTemperature": False,
            "okBeforeCommandOutput": False,
            "smoothieTemperatureReporting": True,
            "klipperTemperatureReporting": False,
            "reprapfwM114": False,
            "sdFiles": {"size": True, "longname": True},
            "throttle": 0.01,
            "sendWait": True,
            "waitInterval": 1.0,
            "rxBuffer": 64,
            "commandBuffer": 4,
            "supportM112": True,
            "echoOnM117": True,
            "brokenM29": True,
            "brokenResend": False,
            "supportF": False,
            "firmwareName": "Tiertime Printer 1.0",
            "sharedNozzle": False,
            "sendBusy": False,
            "busyInterval": 2.0,
            "simulateReset": True,
            "resetLines": ["start", "Tiertime: Tiertime Printers!", "\x80", "SD card ok"],
            "preparedOks": [],
            "okFormatString": "ok",
            "m115FormatString": "FIRMWARE_NAME:{firmware_name} PROTOCOL_VERSION:1.0",
            "m115ReportCapabilities": True,
            "capabilities": {
                "AUTOREPORT_TEMP": True,
                "AUTOREPORT_SD_STATUS": True,
                "EMERGENCY_PARSER": True,
            },
            "m114FormatString": "X:{x} Y:{y} Z:{z} E:{e[current]} Count: A:{a} B:{b} C:{c}",
            "m105TargetFormatString": "{heater}:{actual:.2f}/ {target:.2f}",
            "m105NoTargetFormatString": "{heater}:{actual:.2f}",
            "ambientTemperature": 20,
            "errors": {
                "checksum_mismatch": "Checksum mismatch",
                "checksum_missing": "Missing checksum",
                "lineno_mismatch": "expected line {} got {}",
                "lineno_missing": "No Line Number with checksum, Last Line: {}",
                "maxtemp": "MAXTEMP triggered!",
                "mintemp": "MINTEMP triggered!",
                "command_unknown": "Unknown command {}",
            },
            "enable_eeprom": True,
            "support_M503": True,
            "resend_ratio": 0,
        }

    def get_settings_version(self):
        return 1    

    def on_settings_migrate(self, target, current):
        if current is None:
            config = self._settings.global_get(["devel", "Tiertime"])
            if config:
                self._logger.info(
                    "Migrating settings from devel.Tiertime to plugins.Tiertime ..."
                )
                self._settings.global_set(
                    ["plugins", "Tiertime"], config, force=True
                )
                self._settings.global_remove(["devel", "Tiertime"])

    def get_assets(self):
        # Define your plugin's asset files to automatically include in the
        # core UI here.
        #"js": ["js/tiertime.js"],
        # "css": ["css/tiertime.css"],
        # "less": ["less/tiertime.less"]
        return {
            
        }

    ##~~ Softwareupdate hook

    def get_update_information(self):
        # Define the configuration for your plugin to use with the Software Update
        # Plugin here. See https://docs.octoprint.org/en/master/bundledplugins/softwareupdate.html
        # for details.
        return {
            "tiertime": {
                "displayName": "Tiertime",
                "displayVersion": self._plugin_version,

                # version check: github repository
                "type": "github_release",
                "user": "zhangximin",
                "repo": "OctoPrint-Tiertime",
                "current": self._plugin_version,

                # update method: pip
                "pip": "https://github.com/zhangximin/OctoPrint-Tiertime/archive/{target_version}.zip",
            }
        }

    def tier_printer_factory(self, comm_instance, port, baudrate, read_timeout):
        global g_ws

        if not self._settings.get_boolean(["enabled"]):
            return None

        if port is None or not port.startswith("TIER"):
            return None

        seriallog_handler = CleaningTimedRotatingFileHandler(
            self._settings.get_plugin_logfile_path(postfix="serial"),
            when="D",
            backupCount=3,
        )
        seriallog_handler.setFormatter(logging.Formatter("%(asctime)s %(message)s"))
        seriallog_handler.setLevel(logging.DEBUG)

        self._serial_obj = TierPrinter(
            self._settings,
            g_ws,
            port,
            data_folder=self.get_plugin_data_folder(),
            seriallog_handler=seriallog_handler,
            read_timeout=float(read_timeout),
            faked_baudrate=baudrate,
        )

        if self._serial_obj is not None:
            self._current_sn = self._serial_obj._sn
        else:
            self._printer.disconnect()

        return self._serial_obj

    def get_additional_port_names(self, *args, **kwargs):
        global g_ws
        if self._settings.get_boolean(["enabled"]):            
            if g_ws is None:                
                g_ws = wandServer(self._settings, self._identifier)                
                g_ws.connect()
                g_ws.start_action()
            else:
                if not g_ws._connecting_printer:
                    g_ws.refreshPrinters()

                    counter = 0
                    # Not sure if we should wait here. 2021061
                    while ( g_ws.printer_list is None or len(g_ws.printer_list) < 1 ) and counter < g_ws._timeout:
                        time.sleep(1)
                        counter += 1

            if g_ws is not None and g_ws.printer_list is not None and len(g_ws.printer_list) > 0:
                reValue = []
                for sn in g_ws.printer_list.keys():
                    tPrinter = g_ws.get_printer(sn)
                    if tPrinter.accessCtrl == "1":
                        reValue.append("TIER-" + tPrinter.SN + u"\U0001F512")
                    else:
                        reValue.append("TIER-"+  tPrinter.SN)
                return reValue
            else :
                return []
        else:
            if g_ws is not None:
                try:
                    g_ws.stop_action()
                finally:
                    pass
            return []

    # add tsk extention support.
    def get_extension_tree(self, *args, **kwargs):
        return dict(
            machinecode=dict(
                tiertask=["tsk"]
            )
        )

    def upload_to_tier_printer(self, printer, filename, path, sd_upload_started, sd_upload_succeeded, sd_upload_failed, *args, **kwargs):
        if self._settings.get_boolean(["enabled"]):
            def process():
                g_ws.uploadfile(self._current_sn, path)
                while g_ws._upload_progress != 0:
                    self._logger.info("Uploading ......" + str(g_ws._upload_progress) + "%")
                    time.sleep(1)
                if self._serial_obj is not None and g_ws._upload_jobid > 0:
                    self._serial_obj._selectSdFileByJobID(g_ws._upload_jobid)
                    if self._serial_obj._selectedSdJobID == g_ws._upload_jobid:
                        self._serial_obj._sdCardReady = True
                        self._serial_obj._sdPrint_needStart = False
                        self._serial_obj._startSdPrint()

                if g_ws._lastError is not None:
                    self._serial_obj._send("// action:notification " + g_ws._lastError)
                    g_ws._lastError = None

            thread = threading.Thread(target=process)
            thread.daemon = True
            thread.start()

        return ""

    class TiertimePrintTimeEstimator(PrintTimeEstimator):
        def __init__(self, job_type):
            super().__init__(job_type)
            self._logger = logging.getLogger(
                "octoprint.plugins.tiertime.TiertimePrintTimeEstimator"
            )

        def get_total_seconds(self, stringHMS):
            timedeltaObj = datetime.strptime(stringHMS, "%H:%M:%S") - datetime(1900,1,1)
            return timedeltaObj.total_seconds()

        def estimate(self, progress, printTime, cleanedPrintTime, statisticalTotalPrintTime, statisticalTotalPrintTimeType):
            global g_ws
            reValue = 0
            #get estimate time from wandServer
            if g_ws is not None:
                tStatus = g_ws.get_printer_status(g_ws._upload_sn)
                if tStatus is not None and (tStatus.printerStatus == 2 or tStatus.printerStatus == 3):
                    reValue = self.get_total_seconds(tStatus.remainTime)
            return reValue, "estimate"

    def tiertime_estimator_factory(self, *args, **kwargs):
        return self.TiertimePrintTimeEstimator

# If you want your plugin to be registered within OctoPrint under a different name than what you defined in setup.py
# ("OctoPrint-PluginSkeleton"), you may define that here. Same goes for the other metadata derived from setup.py that
# can be overwritten via __plugin_xyz__ control properties. See the documentation for that.
__plugin_name__ = "Tiertime"

# Starting with OctoPrint 1.4.0 OctoPrint will also support to run under Python 3 in addition to the deprecated
# Python 2. New plugins should make sure to run under both versions for now. Uncomment one of the following
# compatibility flags according to what Python versions your plugin supports!
#__plugin_pythoncompat__ = ">=2.7,<3" # only python 2
__plugin_pythoncompat__ = ">=3,<4" # only python 3
#__plugin_pythoncompat__ = ">=2.7,<4" # python 2 and 3

def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = TiertimePlugin()

    global __plugin_hooks__
    __plugin_hooks__ = {
        "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information,
        "octoprint.comm.transport.serial.factory": __plugin_implementation__.tier_printer_factory,
        "octoprint.comm.transport.serial.additional_port_names": __plugin_implementation__.get_additional_port_names,
        "octoprint.filemanager.extension_tree": __plugin_implementation__.get_extension_tree,
        "octoprint.printer.estimation.factory": __plugin_implementation__.tiertime_estimator_factory,
        "octoprint.printer.sdcardupload": __plugin_implementation__.upload_to_tier_printer,
    }
