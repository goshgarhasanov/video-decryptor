# Decryptor

AES-256 ile sifrelenmis video ve resim dosyalarini cozen Python scripti.

## Kurulum

```bash
pip install -r requirements.txt
```

## Kullanim

```bash
# Scriptin bulundugu klasordeki .enc dosyalarini coz
python decrypt.py

# Belirli bir klasordeki .enc dosyalarini coz (alt klasorler dahil)
python decrypt.py D:\
```

Script calistiginda size sorar:
```
Ne yapmak istiyorsunuz?
  1 - Videolari coz
  2 - Resimleri coz
  3 - Hepsini coz
  0 - Cikis
```

Secim yaptiktan sonra ilgili `.enc` dosyalarini bulur, cozer ve orijinal hallerine geri donusturur.
