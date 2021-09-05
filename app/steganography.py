import cv2
from logging import info, INFO, basicConfig
import numpy as np
from os import getenv
from cryptography.fernet import Fernet
import re
import sys


basicConfig(
    format="%(levelname)s: %(asctime)s %(message)s",
    level=INFO,
)

input_image = "image.jpg"
output_image = "output/steganography.png"
secret_data = getenv("SECRET_DATA")


def normalize_secret(data):
    # try:
    #     data = data.lower()
    # except:
    #     1 == 1
    # data = re.sub("[^a-z0-9 ]+", " ", data).ljust(16, "_")

    return data.ljust(16, "_")


def write_key(key_file_name="output/key.key"):
    """
    Generates a key and save it into a file
    """
    key = Fernet.generate_key()
    with open(key_file_name, "wb") as key_file:
        key_file.write(key)


def load_key(file_name="output/key.key"):
    """
    Loads the key from the current directory named file_name
    """
    return open(file_name, "rb").read()


def decrypt(secret_data, key_file_name="output/key.key"):
    # load key
    key = load_key(key_file_name)
    info(key)

    # initialize the Fernet class
    f = Fernet(key)

    return f.decrypt(secret_data.encode())


def encrypt(secret_data, key_file_name="output/key.key"):
    # initialize key
    write_key(key_file_name)
    # load key
    key = load_key(key_file_name)
    # initialize the Fernet class
    f = Fernet(key)
    try:
        return f.encrypt(secret_data.encode())
    except:
        return f.encrypt(secret_data)


def to_bin(data):
    """Convert `data` to binary format as string"""
    if isinstance(data, str):
        return "".join([format(ord(i), "08b") for i in data])
    elif isinstance(data, bytes) or isinstance(data, np.ndarray):
        return [format(i, "08b") for i in data]
    elif isinstance(data, int) or isinstance(data, np.uint8):
        return format(data, "08b")
    else:
        raise TypeError("Type not supported.")


def encode(image_name, secret_data, key_file_name="output/key.key"):
    # read the image
    image = cv2.imread(image_name)
    info("[*] Encrypting & Encoding data...")
    secret_data = normalize_secret(secret_data)
    secret_data = encrypt(secret_data, key_file_name).decode()
    # maximum bytes to encode
    n_bytes = image.shape[0] * image.shape[1] * 3 // 8
    info("[*] Maximum bytes to encode: {}".format(n_bytes))
    if len(secret_data) > n_bytes:
        raise ValueError(
            "[!] Insufficient bytes, need bigger image or less data."
        )
    # add stopping criteria
    secret_data += "====="
    data_index = 0
    # convert data to binary
    binary_secret_data = to_bin(secret_data)
    # size of data to hide
    data_len = len(binary_secret_data)
    for row in image:
        for pixel in row:
            # convert RGB values to binary format
            r, g, b = to_bin(pixel)
            # modify the least significant bit only if there is still data to store
            if data_index < data_len:
                # least significant red pixel bit
                pixel[0] = int(r[:-1] + binary_secret_data[data_index], 2)
                data_index += 1
            if data_index < data_len:
                # least significant green pixel bit
                pixel[1] = int(g[:-1] + binary_secret_data[data_index], 2)
                data_index += 1
            if data_index < data_len:
                # least significant blue pixel bit
                pixel[2] = int(b[:-1] + binary_secret_data[data_index], 2)
                data_index += 1
            # if data is encoded, just break out of the loop
            if data_index >= data_len:
                break
    return image


def decode(image_name, key_file_name="output/key.key"):
    info("[+] Decoding...")
    # read the image
    image = cv2.imread(image_name)
    binary_data = ""
    for row in image:
        for pixel in row:
            r, g, b = to_bin(pixel)
            binary_data += r[-1]
            binary_data += g[-1]
            binary_data += b[-1]
    # split by 8-bits
    all_bytes = [binary_data[i : i + 8] for i in range(0, len(binary_data), 8)]
    # convert from bits to characters
    decoded_data = ""
    for byte in all_bytes:
        decoded_data += chr(int(byte, 2))
        if decoded_data[-5:] == "=====":
            break
    # return decrypt(decoded_data[:-5], key_file_name)
    pad_decoded_data = decoded_data[:-5] + "="
    return decrypt(pad_decoded_data, key_file_name)


if __name__ == "__main__":

    if sys.argv[1] == "encode":
        # encode the data into the image
        encoded_image = encode(image_name=input_image, secret_data=secret_data)

        # save the output image (encoded image)
        cv2.imwrite(output_image, encoded_image)
    elif sys.argv[1] == "decode":
        decode(
            output_image,
        )
    else:
        info("Input arg must be one of decode, or encode.")
