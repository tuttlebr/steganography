# steganography

Steganography is the practice of hiding a file, message, image or video within another file, message, image or video. The word steganography is derived from the Greek words steganos (meaning hidden or covered) and graphe (meaning writing).

It is often used among hackers to hide secret messages or data within media files such as images, videos or audio files. Even though there are many legitimate uses for Steganography such as watermarking, malware programmers have also been found to use it to obscure the transmission of malicious code.

In this tutorial, we're going to write a Python code to hide text messages using a technique called Least Significant Bit.

Least Significant Bit (LSB) is a technique in which last bit of each pixel is modified and replaced with the data bit. This method only works on Lossless-compression images, which means that the files are stored in a compressed format, but that this compression does not result in the data being lost or modified, PNG, TIFF, and BMP as an example, are lossless-compression image file formats.

As you may already know, an image consists of several pixels, each pixel contains three values (which are Red, Green, Blue), these values range from `0` to `255`, in other words, they are 8-bit values. For example, a value of `225` is `11100001` in binary and so on.

Let's take an example of how this technique works, say I want to hide the message "hi" into a 4x4 image, here are the example image pixel values:

```
[(225, 12, 99), (155, 2, 50), (99, 51, 15), (15, 55, 22),
(155, 61, 87), (63, 30, 17), (1, 55, 19), (99, 81, 66),
(219, 77, 91), (69, 39, 50), (18, 200, 33), (25, 54, 190)]
```

By looking at the ASCII Table, we can convert this message into decimal values and then into binary:

```
0110100 0110101
```

Now, we iterate over the pixel values one by one, after converting them to binary, we replace each least significant bit with that message bits sequentially (e.g `225` is `11100001`, we replace the last bit, the bit in the right (1) with the first data bit (0) and so on).

This will only modify the pixel values by +1 or -1 which is not visually noticable at all, you can also use 2-Least Significant Bits too which will modify the pixels by a range of -3 to +3.

Here is the resulting pixel values (you can check them on your own):

```
[(224, 13, 99),(154, 3, 50),(98, 50, 15),(15, 54, 23),
(154, 61, 87),(63, 30, 17),(1, 55, 19),(99, 81, 66),
(219, 77, 91),(69, 39, 50),(18, 200, 33),(25, 54, 190)]
```

## Encoding an Image

```typescript
brandon@olympus:~/steganography$ docker-compose build

brandon@olympus:~/steganography$ docker-compose up encode
[+] Running 1/0
 ⠿ Container steganography-encode-1  Created                                                                                                                  0.0s
Attaching to steganography-encode-1
steganography-encode-1  | INFO: 2021-12-28 16:04:37,088 [*] Encrypting & Encoding data...
steganography-encode-1  | INFO: 2021-12-28 16:04:37,116 [*] Maximum bytes to encode: 524505
steganography-encode-1 exited with code 0

brandon@olympus:~/steganography$ docker-compose up decode
[+] Running 1/0
 ⠿ Container steganography-decode-1  Created                                                                                                                  0.0s
Attaching to steganography-decode-1
steganography-decode-1  | INFO: 2021-12-28 16:04:45,116 [+] Decoding...
steganography-decode-1  | INFO: 2021-12-28 16:04:48,794 b'BVEyrau2cabIfpM5XgOx8YiVnlFmjZlaroeW--f1GM8='
steganography-decode-1  | INFO: 2021-12-28 16:04:48,834 b'hello, friend.__'
steganography-decode-1 exited with code 0

brandon@olympus:~/steganography$ docker-compose down
```

Here is what the `encode()` function does:

1. Reads the image using cv2.imread() function.
2. Counts the maximum bytes available to encode the data.
3. Checks whether we can encode all the data into the image.
4. Adding a stopping criteria, this will be as indicator for the decoder to stop decoding whenever it sees this (feel free to implement a better and more efficient one).
5. Finally, modifying the last bit of each pixel and replacing it by the data bit.

## Decoding an Image

```bash
docker-compose up --build decode
 ⠿ Container steganography-decode-1  Created                                                                                             0.0s
Attaching to steganography-decode-1
steganography-decode-1  | INFO: 2021-11-26 14:53:48,888 [+] Decoding...
steganography-decode-1  | INFO: 2021-11-26 14:53:53,263 b'i6VSFHWoa5_X2ZSDvu_H9_m2Nn0ZIsh56TodhIw6ESI='
steganography-decode-1  | INFO: 2021-11-26 14:53:53,330 b'hello, friend.__'
steganography-decode-1 exited with code 0
```

Regarding the `decode()` fn, we read the image and then get all the last bits of every pixel of the image. After that, we keep decoding until we see the previously defined stopping criteria.
