import tkinter as tk
from tkinter import filedialog, messagebox
from cryptography.fernet import Fernet
import sys
import os
import tarfile
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG, filename='app.log', filemode='w',
                    format='%(asctime)s - %(levelname)s - %(message)s')

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def load_or_generate_key():
    key_path = resource_path("secret.key")
    try:
        with open(key_path, "rb") as key_file:
            return key_file.read()
    except FileNotFoundError:
        key = Fernet.generate_key()
        with open(key_path, "wb") as key_file:
            key_file.write(key)
        return key

def xor_data(data, key):
    from itertools import cycle
    return bytes(a ^ b for a, b in zip(data, cycle(key)))

def archive_directory(path):
    output_tar = path.rstrip(os.sep) + '.tar'
    with tarfile.open(output_tar, "w") as tar:
        tar.add(path, arcname=os.path.basename(path))
    return output_tar

def unarchive_file(tar_path, dest_dir):
    with tarfile.open(tar_path, "r") as tar:
        tar.extractall(path=os.path.dirname(dest_dir))
    os.remove(tar_path)

def encrypt_file():
    try:
        filepath = filedialog.askopenfilename()
        if not filepath:
            return

        is_directory = os.path.isdir(filepath)
        if is_directory:
            tar_filepath = archive_directory(filepath)
            filename = tar_filepath
        else:
            filename = filepath

        key = load_or_generate_key()
        fernet = Fernet(key)

        with open(filename, "rb") as file:
            file_data = file.read()

        xor_key = os.urandom(len(file_data))
        xor_encrypted_data = xor_data(file_data, xor_key)
        encrypted_data = fernet.encrypt(xor_encrypted_data)

        encrypted_filename = filename + ".encrypted"
        with open(encrypted_filename, "wb") as file:
            file.write(encrypted_data)

        with open(encrypted_filename + ".key", "wb") as key_file:
            key_file.write(xor_key)

        if is_directory:
            os.remove(filename)

        messagebox.showinfo("Success", f"Encryption successful!\nEncrypted file: {encrypted_filename}")
    except Exception as e:
        logging.error(f"Encryption failed: {e}")
        messagebox.showerror("Error", f"Encryption failed: {e}")

def decrypt_file():
    try:
        encrypted_filename = filedialog.askopenfilename()
        if not encrypted_filename or not encrypted_filename.endswith('.encrypted'):
            messagebox.showerror("Error", "Selected file is not an encrypted file.")
            return

        key_file_path = encrypted_filename + ".key"
        if not os.path.exists(key_file_path):
            messagebox.showerror("Error", "Key file missing for the encrypted file!")
            return

        with open(encrypted_filename, "rb") as file:
            encrypted_data = file.read()
        with open(key_file_path, "rb") as key_file:
            xor_key = key_file.read()

        key = load_or_generate_key()
        fernet = Fernet(key)

        fernet_decrypted_data = fernet.decrypt(encrypted_data)
        decrypted_data = xor_data(fernet_decrypted_data, xor_key)

        if encrypted_filename.endswith('.tar.encrypted'):
            filename = encrypted_filename[:-len('.encrypted')]
            with open(filename, "wb") as file:
                file.write(decrypted_data)
            dest_dir = filename[:-len('.tar')]
            unarchive_file(filename, dest_dir)
            messagebox.showinfo("Success", f"Decryption successful!\nDecrypted directory: {dest_dir}")
        else:
            filename = encrypted_filename[:-len('.encrypted')]
            with open(filename, "wb") as file:
                file.write(decrypted_data)
            messagebox.showinfo("Success", f"Decryption successful!\nDecrypted file: {filename}")
    except Exception as e:
        logging.error(f"Decryption failed: {e}")
        messagebox.showerror("Error", f"Decryption failed: {e}")

def setup_window():
    window = tk.Tk()
    window.title("Towel Encrypt")

    encrypt_button = tk.Button(window, text="Encrypt File", command=encrypt_file)
    encrypt_button.pack(pady=10)

    decrypt_button = tk.Button(window, text="Decrypt File", command=decrypt_file)
    decrypt_button.pack(pady=10)

    exit_button = tk.Button(window, text="Exit", command=window.quit)
    exit_button.pack(pady=10)

    window.mainloop()

if __name__ == "__main__":
    setup_window()
