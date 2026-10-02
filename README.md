# 🔐 Pass Manager

Python ve Tkinter ile geliştirilmiş, verileri şifreli saklayan basit ve kişisel bir masaüstü şifre yöneticisi.

## Özellikler

- **Tek kullanıcılı sistem:** İlk kayıttan sonra yeni hesap açılamaz.
- **Şifreli giriş bilgileri:** Kullanıcı adı, şifre ve e-posta veritabanında şifreli saklanır.
- **Şifreli kayıtlar:** Eklenen site, kullanıcı adı ve şifre bilgilerinin tamamı şifrelenir.
- **Otomatik çözme:** Giriş yapınca kayıtlar ek şifre sormadan listelenir.
- **Kayıt silme:** ID girerek veya tabloda sağ tıklayarak silinebilir.
- **Hatalı giriş koruması:** 3 yanlış denemede uygulama kapanır.

## Kullanılan Teknolojiler

| Teknoloji  | Kullanım   |
__________________________
| Python 3   | Ana dil    |
| Tkinter    | Arayüz     |
| SQLite3    | Veritabanı |
| cryptocode | Şifreleme  |


## Kullanım

1. **Kayıt Ol** ile kullanıcı adı, şifre ve e-posta gir.
2. **Giriş Yap** ile oturum aç..
3. Ana menüden **Veri Ekle** yada **Verileri Listele** seçenekleri ile kullanmaya başla.
4. Bir klasör içerisinde kullanmak veri tabanı bütünlüğü için daha verimli olacaktır.

## Nasıl Çalışır?

Giriş şifren, tüm verilerin şifreleme anahtarı olarak kullanılır. Şifren hiçbir yerde düz metin olarak saklanmaz.

```
Giriş şifresi ──► anahtar ──► kullanıcı adı / şifre / site adı (şifreli) ──► pass.db
```

## Dosya Yapısı

```
PassManager/
├── main.py     # Uygulama kodu
├── Log.db      # Kullanıcı hesabı (otomatik oluşur)
└── pass.db     # Kayıtlı şifreler (otomatik oluşur)
```

## EXE Oluşturma

```bash
python -m pip install pyinstaller
python -m PyInstaller --onefile --windowed --hidden-import cryptocode --name PassManager main.py
```

Çıktı `dist/PassManager.exe` klasöründe oluşur.

## ⚠️ Önemli Notlar

- **Giriş şifreni unutursan verilere erişemezsin.** Şifre kurtarma yoktur.
- Bu proje eğitim amaçlıdır.

## Geliştirme Fikirleri

- Daha güçlü anahtar türetme (`scrypt` + `Fernet`)
- Otomatik yedekleme
- Kayıt düzenleme
- Boşta kalınca otomatik kilitleme
