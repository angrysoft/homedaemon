import os
import json 

class BaseConfig:
    def get_config(self) -> dict:
        """Return config as dict"""
        pass
    
    def write_config(self, config: dict) -> None:
        """ Wtire dict config to permament memory"""
        pass
    
    
class DbConfig(BaseConfig):
    def __init__(self):
        from pycouchdb import Server
        srv = Server()
        self.db = srv['config']
    
    def get_config(self) -> dict:
        ret = dict()
        for d in self.db.get_all_docs():
            ret[d.id] = d.get_dict()
            
        return ret
    

class JsonConfig(BaseConfig):
    
    def __init__(self, path):
        self._path = path
    
    def get_config(self):
        ret = dict()
        for entry in os.scandir(self._path):
            if entry.is_file and entry.name.endswith('.json'):
                with open(entry.path) as conf_file:
                    ret[os.path.splitext(entry.name)[0]] = json.load(conf_file)
        return ret        


class ArgConfig(BaseConfig):
    def __init__(self, args):
        print(args)
        self.args = vars(args)
    
    def get_config(self):
        return self.args
         

class Config:
    _instace = None
    _configs = dict()
    
    def __new__(cls):
        if Config._instace is None:
            Config._instace = object.__new__(cls)
            
        return cls._instace
    
    def load_config(self, configObj):
        if not isinstance(configObj, BaseConfig):
            raise TypeError(f"{type(configObj)} if not a {type(BaseConfig)}")
        self._configs.update(configObj.get_config())
        
    def get(self, key:str) -> str:
        if key in self._configs:
            return self._configs[key]
        else:
            return dict()
    
    def __getitem__(self, key):
        return self.get(key)
    
    def __str__(self):
        return str(self._configs)

    