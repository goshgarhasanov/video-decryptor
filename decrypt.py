#!/usr/bin/env python3
"""
Decryptor - AES ile sifrelenmis video ve resim dosyalarini cozer.
Kullanim: python decrypt.py [dizin_yolu]
Varsayilan dizin: scriptin bulundugu klasor
"""

import os
import sys
import hashlib

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

VIDEO_EXTENSIONS = {".mp4", ".3gp", ".mov", ".avi", ".mkv", ".wmv", ".flv", ".webm", ".m4v", ".mpeg", ".mpg", ".ts"}
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".tif", ".webp", ".heic", ".heif", ".svg", ".ico", ".raw", ".cr2", ".nef", ".arw", ".dng", ".psd"}


def derive_key(password: str, salt: bytes, iterations: int) -> bytes:
    """PBKDF2 ile sifreleme anahtari turetir (.NET Rfc2898DeriveBytes uyumlu)."""
    key = hashlib.pbkdf2_hmac("sha1", password.encode("utf-8"), salt, iterations, dklen=KEY_LENGTH)
    return key


def decrypt_file(encrypted_path: str, output_path: str, key: bytes) -> bool:
    """Tek bir .enc dosyasini cozer."""
    try:
        with open(encrypted_path, "rb") as f:
            iv = f.read(16)
            encrypted_data = f.read()

        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)

        with open(output_path, "wb") as f:
            f.write(decrypted_data)

        return True
    except Exception as e:
        print(f"  HATA: {e}")
        return False


def get_file_type(filename: str) -> str:
    """Dosya uzantisina gore video mu resim mi belirler."""
    name_without_enc = filename[:-4]  # .enc kaldir
    _, ext = os.path.splitext(name_without_enc)
    ext = ext.lower()
    if ext in VIDEO_EXTENSIONS:
        return "video"
    elif ext in IMAGE_EXTENSIONS:
        return "resim"
    return "diger"


def find_enc_files_recursive(target_dir: str) -> list:
    """Tum alt klasorlerde .enc dosyalarini bulur."""
    enc_files = []
    for root, dirs, files in os.walk(target_dir):
        for f in files:
            if f.endswith(".enc"):
                enc_files.append(os.path.join(root, f))
    return enc_files


def main():
    # Dizin belirleme
    if len(sys.argv) > 1:
        target_dir = sys.argv[1]
    else:
        target_dir = os.path.dirname(os.path.abspath(__file__))

    if not os.path.isdir(target_dir):
        print(f"Dizin bulunamadi: {target_dir}")
        sys.exit(1)

    # Tum .enc dosyalarini bul (alt klasorler dahil)
    all_enc_files = find_enc_files_recursive(target_dir)

    if not all_enc_files:
        print(f"Sifreli dosya bulunamadi: {target_dir}")
        print("(.enc uzantili dosya yok)")
        sys.exit(0)

    # Dosyalari kategorize et
    video_files = [f for f in all_enc_files if get_file_type(os.path.basename(f)) == "video"]
    image_files = [f for f in all_enc_files if get_file_type(os.path.basename(f)) == "resim"]
    other_files = [f for f in all_enc_files if get_file_type(os.path.basename(f)) == "diger"]

    print(f"Bulunan sifreli dosyalar:")
    print(f"  Video : {len(video_files)}")
    print(f"  Resim : {len(image_files)}")
    if other_files:
        print(f"  Diger : {len(other_files)}")
    print()

    # Kullaniciya sor
    print("Ne yapmak istiyorsunuz?")
    print("  1 - Videolari coz")
    print("  2 - Resimleri coz")
    print("  3 - Hepsini coz")
    print("  0 - Cikis")
    print()

    choice = input("Seciminiz (0/1/2/3): ").strip()

    if choice == "0":
        print("Cikis yapiliyor.")
        sys.exit(0)
    elif choice == "1":
        files_to_decrypt = video_files
        label = "video"
    elif choice == "2":
        files_to_decrypt = image_files
        label = "resim"
    elif choice == "3":
        files_to_decrypt = all_enc_files
        label = "tum"
    else:
        print("Gecersiz secim!")
        sys.exit(1)

    if not files_to_decrypt:
        print(f"Cozulecek {label} dosya bulunamadi.")
        sys.exit(0)

    print(f"\n{len(files_to_decrypt)} {label} dosya cozulecek...\n")

    # Anahtar turet
    key = derive_key(PASSWORD, SALT, ITERATIONS)

    success = 0
    fail = 0

    for i, enc_path in enumerate(files_to_decrypt, 1):
        original_path = enc_path[:-4]  # ".enc" kaldir
        original_name = os.path.basename(original_path)

        if i % 10 == 0 or i <= 3 or i == len(files_to_decrypt):
            print(f"[{i}/{len(files_to_decrypt)}] Cozuluyor: {original_name}")

        if decrypt_file(enc_path, original_path, key):
            os.remove(enc_path)
            success += 1
        else:
            fail += 1

    print(f"\nSonuc: {success} basarili, {fail} basarisiz")


if __name__ == "__main__":
    main()
