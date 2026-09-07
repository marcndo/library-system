from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()

class User:
    def __init__(self, user_name:str, hash_password:str):
        self.user_name = user_name
        self.hash_password = hash_password
    
    def verify_password(self, plain_password: str):
        return password_hash.verify(plain_password,self.hash_password)
   
    @classmethod
    def create(cls, user_name: str, plain_password:str):
        hashed = password_hash.hash(plain_password)
        return cls(user_name, hashed)

    def __repr__(self):
        return f"User('{self.user_name}')"