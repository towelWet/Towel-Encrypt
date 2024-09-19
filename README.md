# Towel Dual Encryption File Encryptor/Decryptor

This Python application provides a dual-layer encryption mechanism using XOR and Fernet encryption to secure your files. The GUI, built with Tkinter, allows for easy encryption and decryption of files on both macOS and Windows platforms.

## How It Works

### Encryption Process

1. **XOR Encryption**: The first layer of encryption uses the XOR operation, a simple and fast symmetric encryption method. The data is encrypted by performing the XOR operation between the data bytes and bytes of a randomly generated key (`xor_key`) that is the same length as the data. This randomness ensures that the XOR key is unique for each encryption process.

2. **Fernet Encryption**: The second layer uses Fernet, which is a symmetric encryption method provided by the `cryptography` library. It ensures that the data encrypted by XOR is further secured with a robust, industry-standard encryption algorithm.

Both layers are necessary to decrypt the encrypted file, making the encryption more secure compared to using a single method.

### Decryption Process

To decrypt an encrypted file, the process reverses:

1. The Fernet layer decrypts the data first, requiring the Fernet key.
2. The XOR layer then uses the saved XOR key to restore the original data.

The decryption process requires both the Fernet key and the XOR key, ensuring that the file can only be decrypted by someone who has access to both.

### Key Files

- **`secret.key`**: This file contains the Fernet key used for both encryption and decryption. It is automatically generated if not present and should be kept secure and not moved from the application's directory.

- **`filename.key`**: For every file encrypted, a corresponding `.key` file is created containing the XOR key used during the XOR encryption process. This file is critical for decryption and must be kept in the same directory as the encrypted file. Without it, decryption is impossible.

## Installation

1. Clone or download the repository to your local machine.
2. Ensure you have Python installed.
3. Install the `cryptography` library using pip:
   ```bash
   pip install cryptography
   ```
4. Run the application:
   ```bash
   python encrypt_decrypt_app.py
   ```

## Usage

1. **To Encrypt**: Click the "Encrypt File" button and select the file you wish to encrypt. The application will create an encrypted version of the file and a `.key` file in the same directory.

2. **To Decrypt**: Click the "Decrypt File" button and select the encrypted file. Ensure the corresponding `.key` file is in the same directory. The application will restore the original file.

## Security Considerations

- Keep the `secret.key` and all `.key` files secure and private.
- Do not lose the `.key` files; without them, decryption is not feasible.
- Regularly update your `cryptography` library to protect against vulnerabilities.
