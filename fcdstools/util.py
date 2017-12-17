# -*- coding: utf-8 -*-

import base64
import binascii
import itertools
import string

class AsciiSafe:
    @staticmethod
    def from_bytes(buf: bytes):
        if is_ascii_nonctl(buf):
            return AsciiSafe(buf.decode("ascii"), False)
        else:
            return AsciiSafe(base64.b64encode(buf).decode("ascii"), True)
    @staticmethod
    def from_dict(dic):
        return AsciiSafe(dic["value"], dic["is_base64"])
    @property
    def value(self): return self._value
    @property
    def is_base64(self): return self._is_base64
    def to_bytes(self):
        return base64.b64decode(self.value) if self.is_base64 else self.value.encode("ascii")
    def to_dict(self):
        return dict(
            value     = self.value,
            is_base64 = self.is_base64,
        )
    def __init__(self, value: str, is_base64: bool): # private
        self._value     = value
        self._is_base64 = is_base64

def crc32digest(data: bytes):
    """return CRC-32 digest in lower case."""
    crc = binascii.crc32(data)
    return f"{crc:08x}"

def nulpad(buf: bytes, size):
    n = len(buf)
    if n >= size: return buf
    return buf + b"\x00" * (size-n)

def is_ascii_nonctl(o):
    if isinstance(o, int):
        return 0x20 <= o <= 0x7E
    elif isinstance(o, bytes):
        return all(is_ascii_nonctl(b) for b in o)
    elif isinstance(o, str):
        return all(is_ascii_nonctl(ord(c)) for c in o)
    else:
        raise AssertionError("NOTREACHED")

def is_filename_safe(o):
    if isinstance(o, int):
        return o in _FILENAME_SAFES
    elif isinstance(o, bytes):
        return all(is_filename_safe(b) for b in o)
    elif isinstance(o, str):
        return all(is_filename_safe(ord(c)) for c in o)
    else:
        raise AssertionError("NOTREACHED")

_FILENAME_SAFES = frozenset(itertools.chain(
    map(ord, string.ascii_letters),
    map(ord, string.digits),
    map(ord, " !#$%&'()+,-.;=@[]^_`{}~"),
))
