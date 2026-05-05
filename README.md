# Decryptor

AES-256 ilə şifrələnmiş video və şəkil fayllarını açan Python skripti.

## Quraşdırma

```bash
pip install -r requirements.txt
```

## İstifadə

```bash
# Skriptin yerləşdiyi qovluqdakı .enc fayllarını aç
python decrypt.py

# Müəyyən bir qovluqdakı .enc fayllarını aç (alt qovluqlar daxil)
python decrypt.py D:\
```

Skript işə salındıqda sizdən soruşur:

```
Nə etmək istəyirsiniz?
  1 - Videoları aç
  2 - Şəkilləri aç
  3 - Hamısını aç
  0 - Çıxış
```

Seçim etdikdən sonra müvafiq `.enc` fayllarını tapır, açır və orijinal halına qaytarır.

## Tələblər

- Python 3.7+
- pycryptodome

## Necə işləyir?

- Şifrə `PBKDF2-HMAC-SHA1` ilə (10 000 iterasiya, 8 baytlıq salt) 32 baytlıq AES-256 açarına çevrilir.
- Hər `.enc` faylının ilk 16 baytı IV (initialization vector) kimi oxunur.
- Qalan məlumat `AES-CBC` rejimində açılır və PKCS7 padding silinir.
- Uğurlu açılışdan sonra orijinal fayl yaradılır, `.enc` versiyası silinir.

## Dəstəklənən formatlar

**Video:** `.mp4`, `.3gp`, `.mov`, `.avi`, `.mkv`, `.wmv`, `.flv`, `.webm`, `.m4v`, `.mpeg`, `.mpg`, `.ts`

**Şəkil:** `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`, `.tiff`, `.tif`, `.webp`, `.heic`, `.heif`, `.svg`, `.ico`, `.raw`, `.cr2`, `.nef`, `.arw`, `.dng`, `.psd`
