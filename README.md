# 🔐 Pass Manager

Python ve Tkinter ile geliştirilmiş, verileri şifreli saklayan basit ve kişisel bir masaüstü şifre yöneticisi.

**Versiyon:** 1.2.3

## Özellikler

- **Tek kullanıcılı sistem:** İlk kayıttan sonra yeni hesap açılamaz.
- **Şifreli giriş bilgileri:** Kullanıcı adı, şifre ve e-posta veritabanında şifreli saklanır. Kayıt sırasında şifre en az 6 karakter olmalıdır.
- **Şifreli kayıtlar:** Eklenen site, kullanıcı adı ve şifre bilgilerinin tamamı şifrelenir.
- **Şifreli notlar:** Başlık ve içerik şifrelenerek saklanır. Notlar eklenebilir, listelenebilir, düzenlenebilir ve silinebilir.
- **Otomatik çözme:** Giriş yapınca kayıtlar ek şifre sormadan listelenir.
- **Tarih bilgisi:** Her şifre ve not kaydının oluşturulma tarihi tutulur.
- **Çift dil desteği:** Türkçe / İngilizce. Başlangıç ekranının sol üstündeki butonla değiştirilir.
- **Güvenli çıkış:** Ana menüdeki **Güvenli Çıkış** butonu, bellekteki ana şifreyi temizleyip başlangıç ekranına döner.
- **Hatalı giriş koruması:** 3 yanlış denemede uygulama kapanır.
- **Silme onayı:** Şifre ve not silmeden önce onay istenir.

## Kullanılan Teknolojiler

| Teknoloji     | Kullanım                          |
|---------------|-----------------------------------|
| Python 3      | Ana dil                           |
| Tkinter / ttk | Arayüz                            |
| SQLite3       | Veritabanı                        |
| cryptocode    | Şifreleme                         |
| customtkinter | Kodda içe aktarılır (gereklidir)  |

## Kullanım

1. **Kayıt Ol** ile kullanıcı adı, şifre ve e-posta gir.
2. **Giriş Yap** ile oturum aç.
3. Ana menüden **Veri Ekle**, **Not Ekle** veya **Verileri Listele** seçenekleri ile kullanmaya başla.
4. **Verileri Listele** altında **Şifreler** ve **Notlar** listelerine ulaşabilirsin.
5. Kayıtlar üzerinde sağ tıklayarak düzenleme, silme ve ayrıntı işlemlerini yap.
6. İşin bitince **Güvenli Çıkış** ile oturumu kapat.
7. Bir klasör içerisinde kullanmak veri tabanı bütünlüğü için daha verimli olacaktır.
8. Masaüstünde kullanmak için kısayol oluşturulması tavsiye edilir.

## Dosya Yapısı

```
PassManager/
├── main.py       # Uygulama kodu
├── app_icon/     # Uygulama ikonları (close.ico, open.ico, security.ico)
├── Log.db        # Kullanıcı hesabı (otomatik oluşur)
└── pass.db       # Kayıtlı şifreler ve notlar (otomatik oluşur)
```

## EXE Oluşturma

```bash
python -m pip install pyinstaller
python -m PyInstaller --onefile --windowed --name PassManager --icon=app_icon\security.ico --add-data "app_icon;app_icon" main.py
```

Çıktı `dist/PassManager.exe` klasöründe oluşur.

## ⚠️ Önemli Notlar

- Giriş şifren, tüm verilerin şifreleme anahtarı olarak kullanılır. Şifren hiçbir yerde düz metin olarak saklanmaz.
- Giriş şifreni unutursan verilere erişemezsin. Şifre kurtarma yoktur (e-posta yalnızca kayıt bilgisi olarak saklanır).
- Kayıt tarihleri şifrelenmeden saklanır.
- Şifre ekleme, düzenleme ve ayrıntılar ekranlarında şifre alanı gizlenmeden (düz metin) gösterilir.
- (```pass.db```) Veri tabanını silmeniz halinde verilere bir daha erişemezsiniz. Düzenli yedek almanız önerilir.
- Bu proje eğitim amaçlıdır.

- Şifre öneri fonksiyonu
- Açık/koyu tema desteğinin tamamlanması (şu an yalnızca buton ikonu değişir)
- Şifre alanlarında göster/gizle seçeneği
