import importlib
import pkgutil

import fire


# init,add,list,install,build,publish,config,export ,info,,install,list,lock,plugin,publish,remove,run,search,show,sync,update,use,venv}
# help version verbose
class Core(object):
    def __init__(self):
        print("init")
        COMMANDS_MODULE_PATH: str = importlib.import_module(
            "cdm.plugins"
        ).__path__  # type: ignore

        for _, name, _ in pkgutil.iter_modules(COMMANDS_MODULE_PATH):
            module = importlib.import_module(f"cdm.plugins.{name}", __name__)
            try:
                klass = module.Command  # type: ignore
            except AttributeError:
                continue
            self.register(klass, klass.name or name)
    
    def register(self, command: object) -> None:
        setattr(self, command.__name__, command)
    
    @staticmethod
    def version():
        return "0.1.0"


app = fire.Fire
