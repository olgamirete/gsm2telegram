from os import path, makedirs
from datetime import datetime

class Logger:
    def __init__(self, name: str, logs_folder: str) -> None:
        
        self.name = name
        self.LOG_FILE=path.join(logs_folder, self.name, 'log')
        self.ERROR_LOG_FILE=path.join(logs_folder, self.name, 'errors')
        
        for x in [self.LOG_FILE, self.ERROR_LOG_FILE]:
            if path.exists(path.dirname(x)) == False:
                makedirs(path.dirname(x))
    
    def log(self, msg: str):
        with open(self.LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(f'{datetime.now().isoformat()}: {msg}\n')

    def log_error(self, e):
        with open(self.ERROR_LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(f'{datetime.now().isoformat()}:\n{e}\n')
            f.write('--------------------------------------------------------------------------------\n')