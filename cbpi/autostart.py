import os
import logging

from cbpi.api import CBPiExtension

PATH = "/etc/init.d/craftbeerpiboot"


class AutostartManager(CBPiExtension):  # todo - inheritance?
    __on_startup = None

    @staticmethod
    def instance(cbpi):
        if not AutostartManager.__on_startup:
            AutostartManager.__on_startup = AutostartManager(cbpi)
        return AutostartManager.__on_startup

    def __init__(self, cbpi):
        if AutostartManager.__on_startup:
            raise Exception("This class is a singleton!")
        else:
            super().__init__(cbpi=cbpi)
            self.logger = logging.getLogger(__name__)

    def init(self):
        logging.info("Checking user autostart settings")
        self.value = self.cbpi.config.get("ADD_TO_SYSTEM_STARTUP")
        try:
            if self.value == "Yes":
                self.add_to_autostart()
            else:
                self.remove_from_autostart()
        except FileNotFoundError:  # todo - any other catches?
            self.cbpi.notify("Addition to startup protocol failed.\n""This option currently works only on RaspberryPi",
                             type="danger")

    def remove_from_autostart(self):
        if os.path.exists(PATH):
            os.remove(PATH)
            os.system('update-rc.d -f craftbeerpiboot remove')
            self.cbpi.notify("CBPi4 Removed from Autostart", type="info")
            logging.info("CBPi4 removed from autostart")

    def add_to_autostart(self):
        if not os.path.exists(PATH):
            os.system('sed "s@#DIR#@{path}@g" /usr/local/lib/python3.7/dist-packages/cbpi/config/craftbeerpiboot > '
                      .format(path=os.path.realpath(os.curdir)) + PATH)
            os.system("sudo chmod 755 " + PATH)
            os.system('update-rc.d craftbeerpiboot defaults')
            self.cbpi.notify("CBPi4 Added to Autostart", type="success")
            logging.info("CBPi4 added to autostart")
