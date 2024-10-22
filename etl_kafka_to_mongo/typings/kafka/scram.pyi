"""
This type stub file was generated by pyright.
"""

from kafka.vendor import six

if six.PY2:
    def xor_bytes(left, right): # -> bytearray:
        ...
    
else:
    def xor_bytes(left, right): # -> bytes:
        ...
    
class ScramClient:
    MECHANISMS = ...
    def __init__(self, user, password, mechanism) -> None:
        ...
    
    def first_message(self): # -> str:
        ...
    
    def process_server_first_message(self, server_first_message): # -> None:
        ...
    
    def hmac(self, key, msg): # -> bytes:
        ...
    
    def create_salted_password(self, salt, iterations): # -> None:
        ...
    
    def final_message(self): # -> str:
        ...
    
    def process_server_final_message(self, server_final_message): # -> None:
        ...
    


