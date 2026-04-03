#!/usr/bin/env python3
"""
Video Decryptor - AES ile sifrelenmis video dosyalarini cozer.
Kullanim: python decrypt.py [dizin_yolu]
Varsayilan dizin: scriptin bulundugu klasor
"""

import os
import sys
import hashlib
from pathlib import Path

try:
    from Crypto.Cipher import AES
    from Crypto.Util.Padding import unpad
except ImportError:
    try:
        from Cryptodome.Cipher import AES
        from Cryptodome.Util.Padding import unpad
    except ImportError:
        print("Gerekli kutuphane eksik. Kurmak icin:")
        print("  pip install pycryptodome")
        sys.exit(1)


PASSWORD = "VideolarSifre2026"
SALT = bytes([1, 2, 3, 4, 5, 6, 7, 8])
ITERATIONS = 10000
KEY_LENGTH = 32  # AES-256


def derive_key(password: str, salt: bytes, iterations: int) -> bytes:
    """PBKDF2 ile sifreleme anahtari turetir (.NET Rfc2898DeriveBytes uyumlu)."""
    # .NET Rfc2898DeriveBytes uses HMAC-SHA1 by default
    key = hashlib.pbkdf2_hmac("sha1", password.encode("utf-8"), salt, iterations, dklen=KEY_LENGTH)
    return key


def decrypt_file(encrypted_path: str, output_path: str, key: bytes) -> bool:
    """Tek bir .enc dosyasini cozer."""
    try:
        with open(encrypted_path, "rb") as f:
            iv = f.read(16)  # Ilk 16 byte = IV
            encrypted_data = f.read()

        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)

        with open(output_path, "wb") as f:
            f.write(decrypted_data)

        return True
    except Exception as e:
        print(f"  HATA: {e}")
        return False


def main():
    # Dizin belirleme
    if len(sys.argv) > 1:
        target_dir = sys.argv[1]
    else:
        target_dir = os.path.dirname(os.path.abspath(__file__))

    if not os.path.isdir(target_dir):
        print(f"Dizin bulunamadi: {target_dir}")
        sys.exit(1)

    # .enc dosyalarini bul
    enc_files = [f for f in os.listdir(target_dir) if f.endswith(".enc")]

    if not enc_files:
        print(f"Sifreli dosya bulunamadi: {target_dir}")
        print("(.enc uzantili dosya yok)")
        sys.exit(0)

    print(f"{len(enc_files)} sifreli dosya bulundu.\n")

    # Anahtar turet
    key = derive_key(PASSWORD, SALT, ITERATIONS)

    success = 0
    fail = 0

    for i, enc_file in enumerate(enc_files, 1):
        # .enc uzantisini kaldir -> orijinal dosya adi
        original_name = enc_file[:-4]  # ".enc" kaldir
        encrypted_path = os.path.join(target_dir, enc_file)
        output_path = os.path.join(target_dir, original_name)

        print(f"[{i}/{len(enc_files)}] Cozuluyor: {original_name}")

        if decrypt_file(encrypted_path, output_path, key):
            # Basarili - .enc dosyasini sil
            os.remove(encrypted_path)
            print("  Tamam!")
            success += 1
        else:
            fail += 1

    print(f"\nSonuc: {success} basarili, {fail} basarisiz")


if __name__ == "__main__":
    main()
