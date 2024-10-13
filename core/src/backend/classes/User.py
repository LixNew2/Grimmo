from dataclasses import dataclass

@dataclass
class User:
    cn : str
    groups : list
    uid : str
    last_name :str
    first_name : str
    phone : str