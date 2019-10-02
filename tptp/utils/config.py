import json
import os
from pathlib import Path


class Config(dict):
    def __init__(self, path:Path, initialDict=None):
        if initialDict:
            super().__init__(initialDict)
        self._path = path

    @staticmethod
    def load(path:Path):
        with path.open(mode='r') as fd:
            c =  Config(path, json.load(fd))
            for k, v in Config.getInitialConfig(None):
                if not k in c:
                    c[k] = v
            return c

    @staticmethod
    def getInitialConfig(path:Path):
        return Config(path, {
            'awsDefaults': {
                'region': 'eu-central-1', # required by awsLambdaSolver
                's3SolverBucket': None, # optional for awsLambdaSolver
                'roleArn': None, # optional for awsLambdaSolver
            },
            'awsLambdaSolvers': [],
            'dockerSolvers': [],
            'localSolvers': [],
            'systemOnTptpSolvers': [],
        })

    def save(self):
        if not self._path.exists():
            self._path.parent.mkdir(exist_ok=True)
            self._path.touch()
        self._path.write_text(json.dumps(self), encoding='utf-8')


BASE_PATH = Path(
    os.environ.get('APPDATA') or
    os.environ.get('XDG_CONFIG_HOME') or
    os.path.join(os.environ['HOME'], '.config')
)
CONFIG_DIR_PATH = BASE_PATH / 'tptp_python_lib'
CONFIG_FILE_PATH = CONFIG_DIR_PATH / 'config.json'
CONFIG = None # This is the configuration dict accessed throughout the library
try:
    CONFIG = Config.load(CONFIG_FILE_PATH)
except:
    CONFIG = Config.getInitialConfig(CONFIG_FILE_PATH)

