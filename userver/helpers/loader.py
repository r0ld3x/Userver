import os, sys
import glob
from importlib import import_module

from userver.helpers.logger import log
from userver.plugins import HELP,HELP_NAME
from userver import HANDLER

class Importer:
    def __init__(self, path="userver/plugins") -> None:
        self.path = path
        return self.load()
    
    def load(self):
        files = glob.glob(f"{self.path}/*.py")
        log.info(f"• Installing Plugins Count : {len(files)} •")
        for plugin in sorted(files):
            plugin = plugin.replace("/", ".").replace("\\", ".")
            plugin = plugin.replace(".py", "")
            cmd_name = plugin.split(".")[-1]
            try:
                doc_str = import_module(plugin)
            except Exception as er:
                log.info(f"Error while Loading {plugin}")
                return log.exception(er)
            if cmd_name not in HELP and '_' not in cmd_name:
                full_doc = doc_str.__doc__.format(i = HANDLER, cmd_name = cmd_name) + """
\n\nGithub: [TheUserver](https://www.github.com/r0ld3x/Userver)
License:  [GNU Affero General Public License](https://www.github.com/r0ld3x/Userver/LICENSE")
Channel: @TheUserver || @TheUserverSupport
©[Userver](https://www.github.com/r0ld3x/Userver)"""
                doc = full_doc
                HELP[cmd_name] = doc
            log.info(f"Successfully Loaded {plugin}!")