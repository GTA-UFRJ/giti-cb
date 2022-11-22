from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import pss
from Crypto.Hash import SHA256
from Crypto import Random


KEY_SIZE = 2048
PRIVATE_KEY_PATH = "./keys/private.pem"
PUBLIC_KEY_PATH = "./keys/public.pem"
RECEIVER_PUBLIC_KEY_PATH = "./keys/receiver.pem"
ENCRYPTED_MESSAGE_PATH = "./keys/encrypted_data.bin"
SENDER_KEY_PATH = "./keys/sender.pem"

def generateKeyPair():
	"""
	generateKeyPairs generates a RSA2048 key-pair that allows both client and server
	to encrypt, decrypt, and sign messages. By default, we save the private and public
	keys in the keys directory under private.pem and public.pem respectively
	"""
	key = RSA.generate(KEY_SIZE)
	private_key = key.export_key()
	file_out = open(PRIVATE_KEY_PATH, "wb")
	file_out.write(private_key)
	file_out.close()

	public_key = key.publickey().export_key()
	file_out = open(PUBLIC_KEY_PATH, "wb")
	file_out.write(public_key)
	file_out.close()

def signMessage(message):
	"""
	signMessage uses the previouly created private key to sign a given message received
	as an argument by the function. By default, the algorithm checks the keys directory
	looking for private.pem to use as the private key
	"""
	private_key = RSA.import_key(open(PRIVATE_KEY_PATH).read())
	messageHash = SHA256.new(message)
	signature = pss.new(private_key).sign(messageHash)
	return signature

def encryptMessage(message):
	"""
	encryptMessage uses the previouly created public key to encrypt a given message received
	as an argument by the function. By default, the algorithm checks the keys directory
	looking for public.pem to use as the private key
	"""
	file_out = open(ENCRYPTED_MESSAGE_PATH,"wb")
	recipient_key = RSA.import_key(open(PUBLIC_KEY_PATH).read())

	cipher_rsa = PKCS1_OAEP.new(recipient_key)
	enc_message = cipher_rsa.encrypt(message)

	file_out.write(enc_message)
	file_out.close()
	return enc_message

def verifySignature(signature, message):
	"""
	verifySignature receives as argument a signature and a message and verifies if
	the signature is valid or not. If the signature is not valid, the function raises
	an exception displaying an error message
	"""
	sender_key = RSA.import_key(open(SENDER_KEY_PATH).read())	
	messageHash = SHA256.new(message)
	verifier = pss.new(sender_key)
	try:
		verifier.verify(messageHash, signature)
	except (ValueError, TypeError):
		print ("The signature is not authentic")

def decryptMessage(message):
	"""
	decryptMessage uses the previouly created private key to decrypt a given message received
	as an argument by the function. By default, the algorithm checks the keys directory
	looking for private.pem to use as the private key
	"""
	private_key = RSA.import_key(open(PRIVATE_KEY_PATH).read())
	cipher_rsa = PKCS1_OAEP.new(private_key)
	dec_message = cipher_rsa.decrypt(message)
	return 

def hashMessage (message):
	"""
	hashMessage receives a message as an argument and returns the SHA256 hash of the message
	"""
	hash = SHA256.new()
	hash.update(message)
	return hash.hexdigest()