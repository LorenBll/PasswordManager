try:
    from cryptography.fernet import Fernet
except ImportError:
    print("Module 'cryptography' not found. Install it with 'pip install cryptography'.")
    exit()

def generate_key ( path:str ) -> str:
    # funzione che genera una chiave e la salva in un file
    
    key = Fernet.generate_key()
    with open(path, "wb") as file:
        file.write(key)
        
    return key.decode() # restituisco la chiave generata come stringa


def get_key ( path:str ) -> str:
    # funzione che legge la chiave (salvata in binario) dal file e la restituisce come stringa
    
    try:
        with open(path, "rb") as file:
            key = file.read()
    
    except FileNotFoundError:
        return "FNF"
    
    except Exception:
        return "ERR"
    
    key = key.decode() # decodifico la chiave in stringa
    return key


def encrypt ( data:str , key:str ) -> str:
    # funzione che cifra i dati
    
    key = key.encode() # codifico la chiave in binario
    cipher = Fernet(key)
    encrypted_data = cipher.encrypt(data.encode())
    
    encrypted_data = encrypted_data.decode() # decodifico i dati cifrati in stringa
    return encrypted_data


def decrypt ( data:str , key:str ) -> str:
    # funzione che decifra i dati
    
    key = key.encode() # codifico la chiave in binario
    cipher = Fernet(key)
    decrypted_data = cipher.decrypt(data.encode())
    
    decrypted_data = decrypted_data.decode() # decodifico i dati decifrati in stringa
    return decrypted_data



if __name__ == "__main__":
    print("This is a module, import it in your code to use it.")
    exit()