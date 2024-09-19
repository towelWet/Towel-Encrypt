import tkinter as tk
from tkinter import filedialog, messagebox
from cryptography.fernet import Fernet
import os

def load_or_generate_key():
    try:
        with open("secret.key", "rb") as key_file:
            key = key_file.read()
    except FileNotFoundError:
        key = Fernet.generate_key()
        with open("secret.key", "wb") as key_file:
            key_file.write(key)
    return key

def xor_data(data, key):
    from itertools import cycle
    return bytes(a ^ b for a, b in zip(data, cycle(key)))

# Encrypt the selected file
def encrypt_file():
    filename = filedialog.askopenfilename()
    if not filename:
        return

    key = load_or_generate_key()
    fernet = Fernet(key)

    with open(filename, "rb") as file:
        file_data = file.read()

    # First layer of encryption using XOR
    xor_key = os.urandom(len(file_data))  # Generate a random XOR key of the same length as the data
    xor_encrypted_data = xor_data(file_data, xor_key)

    # Second layer of encryption using Fernet
    encrypted_data = fernet.encrypt(xor_encrypted_data)

    with open(filename, "wb") as file:
        file.write(encrypted_data)

    # Save the XOR key for decryption process
    with open(filename + ".key", "wb") as key_file:
        key_file.write(xor_key)

    messagebox.showinfo("Success", "File encrypted successfully!")

# Decrypt the selected file
def decrypt_file():
    filename = filedialog.askopenfilename()
    if not filename:
        return

    key = load_or_generate_key()
    fernet = Fernet(key)

    try:
        with open(filename, "rb") as file:
            encrypted_data = file.read()
        with open(filename + ".key", "rb") as key_file:
            xor_key = key_file.read()

        # First decrypt with Fernet
        fernet_decrypted_data = fernet.decrypt(encrypted_data)

        # Then decrypt with XOR
        decrypted_data = xor_data(fernet_decrypted_data, xor_key)

    except Exception as e:
        messagebox.showerror("Error", "Decryption failed: " + str(e))
        return

    with open(filename, "wb") as file:
        file.write(decrypted_data)

    messagebox.showinfo("Success", "File decrypted successfully!")

# Setup the main window
def setup_window():
    window = tk.Tk()
    window.title("File Encryptor/Decryptor with Dual Encryption")

    encrypt_button = tk.Button(window, text="Encrypt File", command=encrypt_file)
    encrypt_button.pack(pady=10)

    decrypt_button = tk.Button(window, text="Decrypt File", command=decrypt_file)
    decrypt_button.pack(pady=10)

    exit_button = tk.Button(window, text="Exit", command=window.quit)
    exit_button.pack(pady=10)

    window.mainloop()

if __name__ == "__main__":
    setup_window()
