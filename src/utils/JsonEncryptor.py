from cryptography.fernet import Fernet
import json
import os

KEY=os.getenv("ENCRYPTION_KEY")

class JsonEncryptor:
    instance = None
    def __init__(self):
        self.key = KEY
        self.cipher_suite = Fernet(self.key)

    @classmethod
    async def get_instance(cls):
        if cls.instance is None:
            cls.instance = JsonEncryptor()
        return cls.instance

    async def encrypt_json_file(self, input_path, output_path):

        with open(input_path, 'r') as file:
            data = json.load(file)

        json_str = json.dumps(data)
        encrypted_data = self.cipher_suite.encrypt(json_str.encode())

        with open(output_path, 'wb') as file:
            file.write(encrypted_data)

    async def decrypt_enc_file(self, input_path):
        with open(input_path, 'rb') as file:
            encrypted_data = file.read()

        decrypted_data = self.cipher_suite.decrypt(encrypted_data)
        data = json.loads(decrypted_data.decode())

        return data
    
    async def decrypt_add_encrypt(self,path,key,value):
        data=await self.decrypt_enc_file(path)
        data[key]=value
        json_str = json.dumps(data)
        encrypted_data = self.cipher_suite.encrypt(json_str.encode())

        with open(path, 'wb') as file:
            file.write(encrypted_data)
        
    async def decrypt_pop_encrypt(self,path,key):
        data=await self.decrypt_enc_file(path)
        data.pop(key)
        json_str = json.dumps(data)
        encrypted_data = self.cipher_suite.encrypt(json_str.encode())

        with open(path, 'wb') as file:
            file.write(encrypted_data)