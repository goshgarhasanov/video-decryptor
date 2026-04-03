# Video Decryptor

AES-256 ile sifrelenmis video dosyalarini cozen Python scripti.

## Kurulum

```bash
pip install -r requirements.txt
```

## Kullanim

```bash
# Scriptin bulundugu klasordeki .enc dosyalarini coz
python decrypt.py

# Belirli bir klasordeki .enc dosyalarini coz
python decrypt.py D:\
```

Script `.enc` uzantili tum dosyalari bulur, cozer ve orijinal video dosyalarini geri yazar. Cozme basarili olursa `.enc` dosyasi silinir.
