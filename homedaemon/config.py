from argparse import Namespace
import os
import json 
from typing import Dict, Any
from abc import ABC, abstractmethod


class BaseConfig(ABC):
    @abstractmethod
    def get_config(self) -> Dict[str,Any]:
        """Return config as dict"""
        pass
    

class JsonConfig(BaseConfig):
    
    def __init__(self, path:str):
        self._path = path
    
    def get_config(self) -> Dict[str,Any]:
        ret: Dict[str,Any] = dict()
        for entry in os.scandir(self._path):
            if entry.is_file and entry.name.endswith('.json'):
                with open(entry.path) as conf_file:
                    ret[os.path.splitext(entry.name)[0]] = json.load(conf_file)
        return ret    


class ArgConfig(BaseConfig):
    def __init__(self, args: Namespace):
        self._args = vars(args)
    
    def get_config(self) -> Dict[str,Any]:
        return self._args
         

class Config:
    _instace = None
    
    def __new__(cls):
        if Config._instace is None:
            Config._instace = object.__new__(cls)
            
        return cls._instace
    
    def __init__(self) -> None:
        self._configs: Dict[str, Any] = {}
    
    def load_config(self, configObj: BaseConfig) -> None:
        self._configs.update(configObj.get_config())
        
    def get(self, key:str, default:Any='') -> Any:
        if key in self._configs:
            return self._configs[key]
        else:
            return default
    
    def __getitem__(self, key:str):
        return self.get(key)
    
    def __str__(self):
        return str(self._configs)


class ConfigError(Exception):
    pass