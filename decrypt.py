#!/usr/bin/env python3
"""
Decryptor - AES ilə şifrələnmiş video və şəkil fayllarını açır.
İstifadə: python decrypt.py [qovluq_yolu]
Default qovluq: skriptin yerləşdiyi qovluq
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
        print("Lazımi kitabxana çatışmır. Quraşdırmaq üçün:")
        print("  pip install pycryptodome")
        sys.exit(1)


PASSWORD = "VideolarSifre2026"
SALT = bytes([1, 2, 3, 4, 5, 6, 7, 8])
ITERATIONS = 10000
KEY_LENGTH = 32  # AES-256

VIDEO_EXTENSIONS = {".mp4", ".3gp", ".mov", ".avi", ".mkv", ".wmv", ".flv", ".webm", ".m4v", ".mpeg", ".mpg", ".ts"}
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".tif", ".webp", ".heic", ".heif", ".svg", ".ico", ".raw", ".cr2", ".nef", ".arw", ".dng", ".psd"}


def derive_key(password: str, salt: bytes, iterations: int) -> bytes:
    """PBKDF2 ilə şifrələmə açarı yaradır (.NET Rfc2898DeriveBytes uyğunluqlu)."""
    key = hashlib.pbkdf2_hmac("sha1", password.encode("utf-8"), salt, iterations, dklen=KEY_LENGTH)
    return key


def decrypt_file(encrypted_path: str, output_path: str, key: bytes) -> bool:
    """Tək bir .enc faylını açır."""
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
        print(f"  XƏTA: {e}")
        return False


def get_file_type(filename: str) -> str:
    """Fayl uzantısına görə video, yoxsa şəkil olduğunu müəyyən edir."""
    name_without_enc = filename[:-4]  # .enc hissəsini sil
    _, ext = os.path.splitext(name_without_enc)
    ext = ext.lower()
    if ext in VIDEO_EXTENSIONS:
        return "video"
    elif ext in IMAGE_EXTENSIONS:
        return "şəkil"
    return "digər"


def find_enc_files_recursive(target_dir: str) -> list:
    """Bütün alt qovluqlarda .enc fayllarını tapır."""
    enc_files = []
    for root, dirs, files in os.walk(target_dir):
        for f in files:
            if f.endswith(".enc"):
                enc_files.append(os.path.join(root, f))
    return enc_files


def main():
    # Qovluğun təyin edilməsi
    if len(sys.argv) > 1:
        target_dir = sys.argv[1]
    else:
        target_dir = os.path.dirname(os.path.abspath(__file__))

    if not os.path.isdir(target_dir):
        print(f"Qovluq tapılmadı: {target_dir}")
        sys.exit(1)

    # Bütün .enc fayllarını tap (alt qovluqlar daxil)
    all_enc_files = find_enc_files_recursive(target_dir)

    if not all_enc_files:
        print(f"Şifrəli fayl tapılmadı: {target_dir}")
        print("(.enc uzantılı fayl yoxdur)")
        sys.exit(0)

    # Faylları kateqoriyalara ayır
    video_files = [f for f in all_enc_files if get_file_type(os.path.basename(f)) == "video"]
    image_files = [f for f in all_enc_files if get_file_type(os.path.basename(f)) == "şəkil"]
    other_files = [f for f in all_enc_files if get_file_type(os.path.basename(f)) == "digər"]

    print(f"Tapılan şifrəli fayllar:")
    print(f"  Video : {len(video_files)}")
    print(f"  Şəkil : {len(image_files)}")
    if other_files:
        print(f"  Digər : {len(other_files)}")
    print()

    # İstifadəçidən soruş
    print("Nə etmək istəyirsiniz?")
    print("  1 - Videoları aç")
    print("  2 - Şəkilləri aç")
    print("  3 - Hamısını aç")
    print("  0 - Çıxış")
    print()

    choice = input("Seçiminiz (0/1/2/3): ").strip()

    if choice == "0":
        print("Çıxış edilir.")
        sys.exit(0)
    elif choice == "1":
        files_to_decrypt = video_files
        label = "video"
    elif choice == "2":
        files_to_decrypt = image_files
        label = "şəkil"
    elif choice == "3":
        files_to_decrypt = all_enc_files
        label = "bütün"
    else:
        print("Yanlış seçim!")
        sys.exit(1)

    if not files_to_decrypt:
        print(f"Açılacaq {label} fayl tapılmadı.")
        sys.exit(0)

    print(f"\n{len(files_to_decrypt)} {label} fayl açılacaq...\n")

    # Açar yarat
    key = derive_key(PASSWORD, SALT, ITERATIONS)

    success = 0
    fail = 0

    for i, enc_path in enumerate(files_to_decrypt, 1):
        original_path = enc_path[:-4]  # ".enc" hissəsini sil
        original_name = os.path.basename(original_path)

        if i % 10 == 0 or i <= 3 or i == len(files_to_decrypt):
            print(f"[{i}/{len(files_to_decrypt)}] Açılır: {original_name}")

        if decrypt_file(enc_path, original_path, key):
            os.remove(enc_path)
            success += 1
        else:
            fail += 1

    print(f"\nNəticə: {success} uğurlu, {fail} uğursuz")


if __name__ == "__main__":
    main()
