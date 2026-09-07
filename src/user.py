from pwdlib import PasswordHash

hash_password = PasswordHash.recommended()

class User:
    def __init__(self, user_name:str, hashed_password:str):
        self.user_name = user_name
        self._hashed_password = hashed_password

    @property
    def hashed_password(self):
        return self._hashed_password
    
    def verify_password(self, plain_password: str):
        return hash_password.verify(plain_password,self.hashed_password)
   
    @classmethod
    def create(cls, user_name: str, plain_password:str):
        hashed = hash_password.hash(plain_password)
        return cls(user_name, hashed)

    def __repr__(self):
        return f"User('{self.user_name}')"