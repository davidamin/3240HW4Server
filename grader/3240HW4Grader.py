#3240 Encryption Homework Autograder
#Assumes functions are in encrypt.py and named secret_string(reg_string,pub_key_obj), encrypt_file(filename,symm_key) and decrypt_file(filename,symm_key)
#Assumes there are sample files 3240test1.txt, 3240test2.jpg, and 3240test3.txt in the folder
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto import Random
import sys
import os

from encrypt import secret_string, encrypt_file, decrypt_file

debug=False
cleanup=True

def hash_equal(filename1,filename2):
	with open(filename1, 'rb') as file1:
		text1 = file1.read()
		
	with open(filename2, 'rb') as file2:
		text2 = file2.read()

	hash1 = SHA256.new(text1).hexdigest()
	hash2 = SHA256.new(text2).hexdigest()
	
	return hash1 == hash2
	
def len_diff(filename1,filename2):
	with open(filename1, 'rb') as file1:
		text1 = file1.read()
		
	with open(filename2, 'rb') as file2:
		text2 = file2.read()
		
	return abs(len(text1) - len(text2))
	
def contains_text(filename1, filename2):
	with open(filename1, 'rb') as file1:
		text1 = file1.read()
		
	with open(filename2, 'rb') as file2:
		text2 = file2.read()
		
	return text1 in text2
	
def test_pub_priv():
	try:
		random_num = Random.new().read
		key = RSA.generate(1024,random_num)
		to_encrypt = "This is my sample string"
		pub = key.publickey()
		enc = secret_string(to_encrypt,pub)
		dec = key.decrypt(enc)
		if to_encrypt != dec.decode("utf-8"):
			if debug:
				print("TEST 1: Couldn't decrypt string with private key. -20 Points.\n ")
			return -20
	except Exception as e:
		if debug:
			print("TEST 1: Exception " + type(e).__name__ + " when tried to decrypt string with private key. -20 Points.\n ")
		return -20	
	return 0
	
def test_txt():
	points = 0
	try:
		encrypt_file("3240test1.txt",b"sixteenbytekey!!")
		with open("3240test1.txt.enc",'rb') as file:
			if contains_text("3240test1.txt","3240test1.txt.enc"):
				if debug:
					print("TEST 2: The encrypted file contained the unencrypted contents. -20 Points.\n ")
				points -= 20
	except Exception as e:
		if debug:
			print("TEST 2: Exception " + type(e).__name__ + " during encryption. -20 Points.\n ")
		points -= 20			
			
	#Check for existence of decrypted file here? Run the decrypt in a different process to stop trickery?
	try:
		decrypt_file("3240test1.txt.enc",b"sixteenbytekey!!")
		if not hash_equal("3240test1.txt","DEC_3240test1.txt"):
			if debug:
				print("TEST 2: The decrypted file differs from the original. -10 Points.\n ")
			points -= 10
			if not contains_text("3240test1.txt","DEC_3240test1.txt"):
				if debug:
					print("TEST 2: The differences between the files don't appear to be related to padding. -10 Points.\n ")
				points -= 10
	except Exception as e:
		if debug:
			print("TEST 2: Exception " + type(e).__name__ + " during decryption. -20 Points.\n ")
		points -= 20	
	return points
	
def test_block():
	try:
		encrypt_file("3240test3.txt",b"sixteenbytekey!!")
		decrypt_file("3240test3.txt.enc",b"sixteenbytekey!!")
		if not hash_equal("3240test3.txt","DEC_3240test3.txt"):
			if not contains_text("3240test3.txt","DEC_3240test3.txt"):
				if debug:
					print("TEST 3: Incorrectly decrypted with a file of non-block size length. -10 Points.\n ")
				return -10
			else:
				if debug:
					print("TEST 3: Failed to remove padding with a file of non-block size length. -5 Points.\n ")
				return -5	
	except Exception as e:
		if debug:
			print("TEST 3: Encountered exception " + type(e).__name__ + " with a file of non-block size length. -10 Points.\n ")
		return -10
	return 0
	
def test_bin():
	try:
		encrypt_file("3240test2.jpg",b"sixteenbytekey!!")
		decrypt_file("3240test2.jpg.enc",b"sixteenbytekey!!")
		if not hash_equal("3240test2.jpg","DEC_3240test2.jpg"):
			if debug:
				print("TEST 4: The decrypted binary file differs from the original. -10 Points.\n ")
			return -10
	except Exception as e:
		if debug:
			print("TEST 4: Exception " + type(e).__name__ + " during decryption. -10 Points.\n ")
		return -10		
	return 0
	
def test_keys():
	try:
		encrypt_file("3240test1.txt",b"This is my key that's super long and oh my goodness it works so well")
		decrypt_file("3240test1.txt.enc",b"This is my key that's super long and oh my goodness it works so well")
		if not hash_equal("3240test1.txt","DEC_3240test1.txt"):
			if not contains_text("3240test1.txt","DEC_3240test1.txt"):
				if debug:
					print("TEST 5: Incorrectly decrypted with key of non-16 byte length. -10 Points.\n ")
				return -10
			else:
				return 0		
	except Exception as e:
		if debug:
			print("TEST 5: Encountered exception " + type(e).__name__ + " with key of non-16 byte length. -10 Points.\n ")
		return -10		
	return 0

if __name__ == "__main__":
	if "-d" in sys.argv:
		debug=True
		print("Running test cases...")
	if "-c" in sys.argv:
		cleanup=False
		print("Not deleting produced files on complete")
	points = 100
	points += test_pub_priv()
	points += test_txt()
	points += test_block()
	points += test_bin()
	points += test_keys()
	if cleanup:
		try:
			os.remove("3240test1.txt.enc")
		except:
			pass
		try:
			os.remove("3240test2.jpg.enc")
		except:
			pass
		try:
			os.remove("3240test3.txt.enc")
		except:
			pass
		try:
			os.remove("DEC_3240test1.txt")
		except:
			pass
		try:
			os.remove("DEC_3240test2.jpg")
		except:
			pass
		try:
			os.remove("DEC_3240test3.txt")
		except:
			pass
	print("Recommended Score: " + str(points) + "/100")
	