import base64
import os
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES

'''
with open('public.pem', 'rb') as f:
    public = f.read()
print(base64.b64encode(public))
'''

# public key with base64 encoding
pubKey = '''MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAjNu9yZviDavCCmnF5U1NBMSmWvDo38Ozib3XbQcIweO24A8sH84I2CeRj2NmDs3oUyPDTwSLhwbTCxnKO8XvrbCaGvoOH26zfE/bBBFSSva4lJdGYcZXNAHa0//bVDeFsMjVl6Fqtm2x4+xC/HhSKj+oDR66FcjhB+JmRJ61RjRw1JbGiY9Xb5y2CZW39GR4yFLxanIugLnZTi23+g8GDgFFxizEmYWD4PmNaLKyjkQwQDuSiBE7/vwAVv6+/MSmZq0bvGbNXLqQHTCevGXIFLOBWkvfzQ5QrHwnWgkuAlAFmXFFBiumhubYXo9iSrs5tiRe4CfxWUaxq6PD1dOEQwIDAQAB'''
pubKey = base64.b64decode(pubKey)


def scanRecurse(baseDir):
    '''
    Scan a directory and return a list of all files
    return: list of files
    '''
    for entry in os.scandir(baseDir):
        if entry.is_file():
            yield entry
        else:
            yield from scanRecurse(entry.path)


def encrypt(dataFile, publicKey):
    '''
    use EAX mode to allow detection of unauthorized modifications
    '''
    # read data from file
    with open(dataFile, 'rb') as f:
        data = f.read()
    
    # convert data to bytes
    data = bytes(data)

    # create public key object
    key = RSA.import_key(publicKey)
    sessionKey = os.urandom(16)

    # encrypt the session key with the public key
    cipher = PKCS1_OAEP.new(key)
    encryptedSessionKey = cipher.encrypt(sessionKey)

    # encrypt the data with the session key
    cipher = AES.new(sessionKey, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(data)

    # save the encrypted data to file
    [ fileName, fileExtension ] = dataFile.split('.')
    encryptedFile = fileName + '_encrypted.' + fileExtension
    with open(encryptedFile, 'wb') as f:
        [ f.write(x) for x in (encryptedSessionKey, cipher.nonce, tag, ciphertext) ]
    print('Encrypted file saved to ' + encryptedFile)

fileName = 'test.txt'
encrypt(fileName, pubKey)
