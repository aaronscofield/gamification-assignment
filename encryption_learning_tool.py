import socket
from time import sleep
import re
from des import DesKey
import random
import string

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = 12345
s.bind(('', port))

s.listen(5)
print("Socket is now listening...")

c, addr = s.accept()
print("Accepted connection from ", addr)


# converts input to a string and sends message to the user's console
def send_message(message):
    c.send(str.encode(message))


# introduces encryption, provides historical context, and prompts the example
def welcome_message():
    sleep(2)
    send_message("\nHi, this is the server, and welcome to a quick tutorial about encryption!\n\n")
    sleep(6)
    send_message("Encryption is a powerful tool that combines mathematics and secret codes.\n")
    sleep(6)
    send_message("It dates back to over 4000 years ago, and has even been used by people like\n")
    send_message("Thomas Jefferson and Julius Caesar!\n\n")
    sleep(6)
    send_message("In modern day, every single company uses encryption to protect their customers',\n")
    send_message("data as well as their own. Let's run through an example!\n")
    sleep(6)


# generates the randomized 8 letter DES key and writes it to a file
def genDESKey():
    f = open("DESkey.txt", "w")
    letters = string.ascii_letters
    f.write(''.join(random.choice(letters) for _ in range(8)))
    f.close()


# prompts the user to enter a word, uses regex to make it readable,
# then encrypts the word with the previously generated DES key from file.
# the function then outputs this encrypted word to the user's console and returns it
def example():
    send_message("\nFor this quick example of encryption, I'll need you to type a word. Any word!\n")
    send_message("Enter it here: ")
    word_received = c.recv(1024)

    # clean up input with regex
    word_received = re.sub(r'[b\'(.*?)\\r\\n\']', '', str(word_received))

    if word_received == "":
        send_message("Oops! You didn't enter anything, let's try again.\n")
        example()
    else:
        genDESKey()
        f = open("DESkey.txt", "r")
        key_from_file = str.encode(f.read())
        key0 = DesKey(key_from_file)

        word_received = bytes(word_received, 'latin-1')
        encrypted_word = key0.encrypt(word_received, padding=True)

        substring = re.search(r"b'(.*?)'", str(encrypted_word)).group(1)

        send_message("\nYour word, encrypted, looks like this: " + substring + "\n\n")
        sleep(7)
        send_message("Pretty hard to read, right? It was encrypted using a popular algorithm called DES, \n")
        send_message("which stands for \"data encryption standard\".\n\n")
        sleep(7)

        return encrypted_word


# introduces the concept of encryption keys, outputs the key used to encrypt the user's word
# decrypts the message, and outputs the original word.
def key_discussion(ciphertext):
    send_message("\"But computer,\" you say, \"how could someone decode that message?\"\n\n")
    sleep(7)
    send_message("Your original message was encoded with a \"secret key\", and\n")
    send_message("with that same key, your message can be decoded!\n\n")
    sleep(7)

    f = open("DESkey.txt", "r")
    key_from_file = str.encode(f.read())
    key0 = DesKey(key_from_file)

    substring = re.search(r"b'(.*?)'", str(key_from_file)).group(1)

    send_message("For this example, the key was an 8-character string that \n")
    send_message("was randomly generated: " + substring + "\n\n")
    sleep(7)

    send_message("When we decode that ciphertext with the key, we get the original word you typed!\n")

    plaintext = key0.decrypt(ciphertext, padding=True)

    cleaned_plaintext = re.search(r"b'(.*?)'", str(plaintext)).group(1)

    send_message("Original word: " + cleaned_plaintext + "\n\n")
    sleep(7)


# concludes the program
def conclusion():
    send_message("There are hundreds of different encryption algorithms, \n")
    send_message("and some are more secure than others! \n\n")
    sleep(7)
    send_message("I hope you enjoyed this brief introduction to encryption,\n")
    send_message("may your encryption be secure and your passwords be safe!\n\n")


# main function, calls each function in turn then quits
def main():
    welcome_message()
    returned_encryption = example()
    key_discussion(returned_encryption)
    conclusion()
    quit()


if __name__ == "__main__":
    main()
