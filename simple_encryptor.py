# simple_encryptor.py
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes
import os

class SimpleEncryptor:
    def __init__(self):
        self.salt = b'salt_12345'  # For extra security
    
    def encrypt_file(self, file_path, password):
        """Lock a file with password"""
        
        # 1. Read the file
        with open(file_path, 'rb') as f:
            data = f.read()
        
        # 2. Create a key from password
        key = PBKDF2(password, self.salt, dkLen=32)  # 32 bytes = 256 bits
        
        # 3. Create encryption machine
        cipher = AES.new(key, AES.MODE_GCM)
        
        # 4. Encrypt the data
        ciphertext, tag = cipher.encrypt_and_digest(data)
        
        # 5. Save encrypted file
        encrypted_file = file_path + '.enc'
        with open(encrypted_file, 'wb') as f:
            f.write(cipher.nonce)  # Save special number
            f.write(tag)           # Save security check
            f.write(ciphertext)    # Save encrypted data
        
        print(f"✅ File encrypted: {encrypted_file}")
        return encrypted_file
    
    def decrypt_file(self, encrypted_file, password):
        """Unlock a file with password"""
        
        # 1. Read encrypted file
        with open(encrypted_file, 'rb') as f:
            nonce = f.read(16)   # Read special number
            tag = f.read(16)     # Read security check
            ciphertext = f.read()  # Read encrypted data
        
        # 2. Create key from password (same as before)
        key = PBKDF2(password, self.salt, dkLen=32)
        
        # 3. Create decryption machine
        cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
        
        # 4. Decrypt the data
        try:
            data = cipher.decrypt_and_verify(ciphertext, tag)
            
            # 5. Save original file
            original_name = encrypted_file.replace('.enc', '_decrypted')
            with open(original_name, 'wb') as f:
                f.write(data)
            
            print(f"✅ File decrypted: {original_name}")
            return original_name
            
        except ValueError:
            print("❌ Wrong password or file corrupted!")
            return None

# HOW TO USE THIS:
if __name__ == "__main__":
    encryptor = SimpleEncryptor()
    
    print("=== File Encryption Tool ===")
    print("1. Encrypt a file")
    print("2. Decrypt a file")
    print("3. Exit")
    
    while True:  # Keep showing menu until exit
        print("\n" + "="*30)
        choice = input("Enter choice (1, 2, or 3): ")
        
        if choice == "1":
            file_path = input("Enter file path to encrypt: ").strip()
            password = input("Enter password: ").strip()
            if os.path.exists(file_path):
                encryptor.encrypt_file(file_path, password)
            else:
                print(f"❌ File not found: {file_path}")
        
        elif choice == "2":
            file_path = input("Enter encrypted file path (.enc file): ").strip()
            password = input("Enter password: ").strip()
            if os.path.exists(file_path):
                encryptor.decrypt_file(file_path, password)
            else:
                print(f"❌ File not found: {file_path}")
        
        elif choice == "3":
            print("Goodbye!")
            break
        
        else:
            print("❌ Invalid choice! Please enter 1, 2, or 3") 
