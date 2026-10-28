#________________________________________________________________________________________________________________
# Kullanılan kütüphaneler
import sqlite3
import webbrowser
import cryptocode
import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
import customtkinter as ctk

#________________________________________________________________________________________________________________

# Ekranda taşıma yapıldığında sabit kalması için bir modül yazılacak.
# customtkinter kullanılarak arayüz güncellenecek.

#________________________________________________________________________________________________________________
# Ara Elemanlar

versiyon = "1.2.3"
backemoji = " \u2190 "  # ⏻
ekran_boyutu = "350x250+600+300"
dil = "TR"
tema = "acik"
yanlis = 0

#________________________________________________________________________________________________________________
# Ara Fonksiyonlar

def temizle():
    for widget in root.winfo_children():
        widget.destroy()

def tarih_info():
    now = datetime.now()
    tarih = now.strftime("%d/%m/%Y %H:%M:%S")
    return tarih

def tr_kucult(s):
    # "Instagram" yazınca "instagram" da bulunsun (Türkçe İ/ı sorunu)
    return str(s).replace("İ", "i").replace("I", "i").replace("ı", "i").lower()

def dil_degistir():
    global dil
    dil = "ENG" if dil == "TR" else "TR"
    secim_ekrani()

def tema_degistir():
    global tema
    tema = "koyu" if tema == "acik" else "acik"
    secim_ekrani()

def cevir(tr_metin, eng_metin):
    return tr_metin if dil == "TR" else eng_metin

#________________________________________________________________________________________________________________
# kullanıcı Giriş fonksiyonu

def login():
    global ana_sifre, yanlis

    username = entry_name.get()
    password = entry_pass.get()

    if username and password:
        db = sqlite3.connect("Log.db")
        a = db.cursor()

        a.execute("CREATE TABLE IF NOT EXISTS Log (id INTEGER PRIMARY KEY, Username TEXT, Password TEXT, Email TEXT)")

        a.execute("SELECT Username, Password FROM Log")
        row = a.fetchone()

        db.close()

        user = False
        if row:
            cozulen_user = cryptocode.decrypt(row[0], password)
            cozulen_sifre = cryptocode.decrypt(row[1], password)
            user = (cozulen_user == username and cozulen_sifre == password)

        if user:
            ana_sifre = password
            yanlis = 0
            messagebox.showinfo(cevir("Başarılı", "Success"), cevir("Giriş Başarılı!", "Login successful!"))
            ana_menu_ekrani()
        else:
            yanlis += 1
            messagebox.showerror(cevir("Hata", "Error"), cevir("Kullanıcı adı veya şifre hatalı!", "Wrong username or password!"))
            if yanlis >= 3:
                messagebox.showerror(cevir("Hata", "Error"), cevir("3 kez hatalı giriş yaptınız.", "You entered wrong credentials 3 times."))
                yanlis = 0
                root.destroy()

    else:
        messagebox.showwarning(cevir("Uyarı", "Warning"), cevir("Lütfen kullanıcı adı ve şifre girin!", "Please enter username and password!"))

#________________________________________________________________________________________________________________
# kullanıcı kayıt Fonksiyonu 

def register():

    username = entry_name.get()
    password = entry_pass.get()
    email = entry_email.get()

    if not (username and password and email):
        messagebox.showwarning(cevir("Uyarı", "Warning"), cevir("Lütfen tüm alanları doldurun!", "Please fill in all fields!"))
        return

    elif len(password) < 6:
        messagebox.showwarning(cevir("Uyarı", "Warning"), cevir("Şifre en az 6 karakter uzunluğunda olmalıdır!", "Password must be at least 6 characters long!"))

        return

    db = sqlite3.connect("Log.db")
    a = db.cursor()

    a.execute("CREATE TABLE IF NOT EXISTS Log (id INTEGER PRIMARY KEY, Username TEXT, Password TEXT, Email TEXT)")

    a.execute("SELECT COUNT(*) FROM Log")
    if a.fetchone()[0] > 0:
        db.close()
        messagebox.showwarning(cevir("Uyarı", "Warning"), cevir("Zaten bir kullanıcı kayıtlı, yeni kayıt yapılamaz!", "A user is already registered, no new registration allowed!"))
        return

    sifreli = cryptocode.encrypt(password, password)
    usersifreli = cryptocode.encrypt(username, password)
    emailsifreli = cryptocode.encrypt(email, password)

    a.execute("INSERT INTO Log (Username, Password, Email) VALUES(?, ?, ?)", (usersifreli, sifreli, emailsifreli))
    db.commit()
    db.close()

    messagebox.showinfo(cevir("Başarılı", "Success"), cevir("Kaydınız Başarılı Bir Şekilde Oluşturulmuştur!", "Your registration was created successfully!"))
    secim_ekrani()

#________________________________________________________________________________________________________________
#Veri tabanı oluşturma ve veri ekleme fonksiyonu

def create_data():
    username = entry_name.get()
    sitename = entry_sitename.get()
    password = entry_pass.get()

    if not (username and password and sitename):
        messagebox.showwarning(cevir("Uyarı", "Warning"),cevir("Lütfen tüm alanları doldurun!", "Please fill in all fields!"))
        return

    db = sqlite3.connect("pass.db")
    a = db.cursor()

    myEncryptedMessage = cryptocode.encrypt(password, ana_sifre)
    userpass = myEncryptedMessage
    myEncryptedMessage = cryptocode.encrypt(username, ana_sifre)
    nickname = myEncryptedMessage
    myEncryptedMessage = cryptocode.encrypt(sitename, ana_sifre)
    sittenname = myEncryptedMessage
    

    a.execute("CREATE TABLE IF NOT EXISTS pass (id INTEGER PRIMARY KEY, Username TEXT, Password TEXT, Sitename TEXT, Tarih TEXT)")
    a.execute("INSERT INTO pass (Username, Password, Sitename, Tarih) VALUES(?, ?, ?, ?)", (nickname, userpass, sittenname, tarih_info()))
    db.commit()
    db.close()

    messagebox.showinfo(cevir("Başarılı", "Success"), cevir(f"{sitename} bilgileri başarıyla kaydedildi!", f"{sitename} saved successfully!"))

    entry_name.delete(0, tk.END)
    entry_pass.delete(0, tk.END)
    entry_sitename.delete(0, tk.END)

#________________________________________________________________________________________________________________
# Not ekleme fonksiyonu

def create_notes():
    baslik = entry_baslik.get().strip()
    icerik = text_icerik.get("1.0", "end-1c").strip()

    if not (baslik and icerik):
        messagebox.showwarning(cevir("Uyarı", "Warning"),cevir("Lütfen tüm alanları doldurun!", "Please fill in all fields!"))
        return

    sifreli_baslik = cryptocode.encrypt(baslik, ana_sifre)
    sifreli_icerik = cryptocode.encrypt(icerik, ana_sifre)

    db = sqlite3.connect("pass.db")
    a = db.cursor()

    a.execute('CREATE TABLE IF NOT EXISTS notes ("ID" INTEGER, "Başlık" TEXT, "İçerik" TEXT, "Tarih" TEXT, PRIMARY KEY("ID"))')
    a.execute('INSERT INTO notes ("Başlık", "İçerik", "Tarih") VALUES(?, ?, ?)',
              (sifreli_baslik, sifreli_icerik, tarih_info()))
    db.commit()
    db.close()

    messagebox.showinfo(cevir("Başarılı", "Success"), cevir(f"{baslik} bilgileri başarıyla kaydedildi!", f"{baslik} saved successfully!"))


    entry_baslik.delete(0, tk.END)
    text_icerik.delete("1.0", tk.END)

#________________________________________________________________________________________________________________
# Not Görüntüleme fonksiyonu

def view_notes():
    for row in tree_notlar.get_children():
        tree_notlar.delete(row)

    db = sqlite3.connect("pass.db")
    a = db.cursor()

    a.execute('CREATE TABLE IF NOT EXISTS notes ("ID" INTEGER, "Başlık" TEXT, "İçerik" TEXT, "Tarih" TEXT, PRIMARY KEY("ID"))')
    a.execute('SELECT "ID", "Başlık", "Tarih" FROM notes ORDER BY "ID" DESC')

    for id_no, sifreli_baslik, tarih in a.fetchall():
        baslik = cryptocode.decrypt(sifreli_baslik, ana_sifre) or "______________"
        tree_notlar.insert("", tk.END, values=(id_no, baslik, tarih or "-"))

    db.close()

#________________________________________________________________________________________________________________
#Veri güncelleme fonksiyonu

def data_update():
    new_username = entry_name.get()
    new_password = entry_pass.get()
    new_sitename = entry_sitename.get()

    if not (new_username and new_password and new_sitename):
        messagebox.showwarning(cevir("Uyarı", "Warning"),cevir("Lütfen tüm alanları doldurun!", "Please fill in all fields!"))
        return

    nickname = cryptocode.encrypt(new_username, ana_sifre)
    userpass = cryptocode.encrypt(new_password, ana_sifre)
    sittenname = cryptocode.encrypt(new_sitename, ana_sifre)

    db = sqlite3.connect("pass.db")
    a = db.cursor()
    a.execute(
        "UPDATE pass SET Username=?, Password=?, Sitename=? WHERE id=?",
        (nickname, userpass, sittenname, duzenlenen_id),
    )
    db.commit()
    db.close()

    messagebox.showinfo(cevir("Başarılı", "Success"), cevir(f"{duzenlenen_id} id'li veri güncellendi.", f"Record {duzenlenen_id} updated."))
    veri_listele_ekrani()

#________________________________________________________________________________________________________________
#Veri silme fonksiyonu

def delete_pass():
    if secilen["satir"] is None:
        return

    degerler = tree.item(secilen["satir"], "values")
    deleted = int(degerler[0])  # ilk sütun ID

    yanit = messagebox.askyesno(cevir("Onay", "Confirm"), cevir(f"{deleted} id'li veriyi silmek istediğinize emin misiniz?", f"Are you sure you want to delete record {deleted}?"))

    if yanit:
        db = sqlite3.connect("pass.db")
        a = db.cursor()

        a.execute("DELETE FROM pass WHERE id=?", (deleted,))
        db.commit()
        db.close()

        messagebox.showinfo(cevir("Başarılı", "Success"), cevir(f"{deleted} id'li veri silindi.", f"Record {deleted} deleted."))
        secilen["satir"] = None
        view_data()
    else:
        messagebox.showinfo(cevir("İptal", "Cancelled"), cevir("Silme işlemi iptal ediliyor.", "Deletion cancelled."))

def delete_notes(kayit_id):
    yanit = messagebox.askyesno(
        cevir("Onay", "Confirm"),
        cevir(f"{kayit_id} id'li notu silmek istediğinize emin misiniz?",
              f"Are you sure you want to delete note {kayit_id}?")
    )

    if yanit:
        db = sqlite3.connect("pass.db")
        a = db.cursor()

        a.execute('DELETE FROM notes WHERE "ID"=?', (kayit_id,))
        db.commit()
        db.close()

        messagebox.showinfo(
            cevir("Başarılı", "Success"),
            cevir(f"{kayit_id} id'li not silindi.", f"Note {kayit_id} deleted.")
        )
        view_notes()
    else:
        messagebox.showinfo(
            cevir("İptal", "Cancelled"),
            cevir("Silme işlemi iptal ediliyor.", "Deletion cancelled.")
        )
#________________________________________________________________________________________________________________
#Şifreleri görüntüleme fonksiyonu

def view_data():
    for row in tree.get_children():
        tree.delete(row)

    filtre = tr_kucult(entry_ara.get().strip())

    db = sqlite3.connect("pass.db")
    a = db.cursor()

    a.execute("CREATE TABLE IF NOT EXISTS pass (id INTEGER PRIMARY KEY, Username TEXT, Password TEXT, Sitename TEXT, Tarih TEXT)")
    a.execute("SELECT id, Username, Password, Sitename FROM pass")

    for id_no, u, p, s in a.fetchall():
        cozulen_user = cryptocode.decrypt(u, ana_sifre) or "______________"
        cozulen_sifre = cryptocode.decrypt(p, ana_sifre) or "_____________"
        cozulen_site = cryptocode.decrypt(s, ana_sifre) or "______________"

        # kullanıcı adı veya site adında arar (şifrede aramaz)
        if filtre and filtre not in tr_kucult(cozulen_user) and filtre not in tr_kucult(cozulen_site):
            continue

        tree.insert("", tk.END, values=(id_no, cozulen_user, cozulen_site, cozulen_sifre))

    db.close()

#________________________________________________________________________________________________________________
#Kayıt Ve giriş seçim arayüzü

def secim_ekrani():
    temizle()
    root.title("Pass Manager")
    root.geometry(ekran_boyutu)
    root.iconbitmap("app_icon/close.ico")
    tr = (dil == "TR")

    label_title = tk.Label(root, text="")
    label_title.pack(pady=10)


    btn_login = tk.Button(root, text="Giriş Yap" if tr else "Login", width=20, height=2, command=giris_ekrani)
    btn_login.pack(pady=10)

    btn_register = tk.Button(root, text="Kayıt Ol" if tr else "Register", width=20, height=2, command=kayit_ekrani)
    btn_register.pack(pady=10)

    label_info = tk.Label(root, text=f"{'Versiyon' if tr else 'Version'}: {versiyon}", fg="gray")
    label_info.pack(side=tk.BOTTOM, pady=10)

    btn_dil = tk.Button(root, text=dil, command=dil_degistir , width=4)
    btn_dil.place(x=10, y=10)

    ikon = " ⏾ " if tema == "acik" else " ☀ "
    btn_black = tk.Button(root, text=f" {ikon} ", width=4, command=tema_degistir)
    btn_black.place(relx=1.0, x=-10, y=10, anchor="ne")

#________________________________________________________________________________________________________________
# Kullanıcı Giriş arayüzü

def giris_ekrani():
    global entry_name, entry_pass

    temizle()
    root.title("Pass Manager - Giriş Ekranı")
    root.geometry(ekran_boyutu)
    root.iconbitmap("app_icon/close.ico")
    tr = (dil == "TR")

    label_title = tk.Label(root, text="")
    label_title.pack(pady=10)

    label_name = tk.Label(root, text="Kullanıcı Adı"if tr else "User Name")
    label_name.pack()
    entry_name = tk.Entry(root)
    entry_name.pack()

    label_pass = tk.Label(root, text="Şifre" if tr else "Password")
    label_pass.pack()
    entry_pass = tk.Entry(root, show="*")
    entry_pass.pack()

    btn_login = tk.Button(root, text="Giriş Yap"if tr else "Login", command=login)
    btn_login.pack(pady=10)

    btn_back = tk.Button(root, text=backemoji,width=3, command=secim_ekrani)
    btn_back.place(x=10, y=10)

#________________________________________________________________________________________________________________
# Kullanıcı kayıt arayüzü

def kayit_ekrani():
    global entry_name, entry_pass, entry_email

    temizle()
    root.title("Pass Manager - Kullanıcı Kaydı")
    root.geometry(ekran_boyutu)
    root.iconbitmap("app_icon/close.ico")
    tr = (dil == "TR")

    label_title = tk.Label(root, text="")
    label_title.pack(pady=10)

    label_name = tk.Label(root, text="Kullanıcı Adı"if tr else "User Name")
    label_name.pack()
    entry_name = tk.Entry(root)
    entry_name.pack()

    label_pass = tk.Label(root, text="Şifre"if tr else "Password")
    label_pass.pack()
    entry_pass = tk.Entry(root, show="*")
    entry_pass.pack()

    label_email = tk.Label(root, text="E-posta"if tr else "E-mail")
    label_email.pack()
    entry_email = tk.Entry(root)
    entry_email.pack()

    btn_login = tk.Button(root, text="Kayıt Ol"if tr else "Sing Up", command=register)
    btn_login.pack(pady=10)

    btn_back = tk.Button(root, text=backemoji,width=3, command=secim_ekrani)
    btn_back.place(x=10, y=10)

#________________________________________________________________________________________________________________
#Ana Menü arayüzü

def ana_menu_ekrani():
    temizle()
    root.title("Pass Manager")
    root.geometry(ekran_boyutu)
    root.iconbitmap("app_icon/open.ico")
    tr = (dil == "TR")

    btn_create = tk.Button(root, text="Veri Ekle "if tr else "Create Data", width=20, height=2, command=veri_ekle_ekrani)
    btn_create.pack(pady=10)

    btn_create = tk.Button(root, text="Not Ekle "if tr else "Create Note", width=20, height=2, command=not_ekranı)
    btn_create.pack(pady=10)

    btn_list = tk.Button(root, text="Verileri Listele"if tr else "List Data", width=20, height=2, command=veri_secim_ekrani)
    btn_list.pack(pady=10)

    def guvenli_cikis():
        global ana_sifre
        ana_sifre = None
        secim_ekrani()
    
    btn_exit = tk.Button(root, text="Güvenli Çıkış"if tr else "Safe Exit", width=20, height=2, command=guvenli_cikis)
    btn_exit.pack(pady=10)

def veri_secim_ekrani():
    temizle()
    root.title("Pass Manager")
    root.geometry(ekran_boyutu)
    root.iconbitmap("app_icon/open.ico")
    tr = (dil == "TR")

    btn_create = tk.Button(root, text="Veri Ekle "if tr else "Create Data", width=20, height=2, command=veri_ekle_ekrani)
    btn_create.pack(pady=10)

    btn_create = tk.Button(root, text="Not Ekle "if tr else "Create Note", width=20, height=2, command=not_ekranı)
    btn_create.pack(pady=10)

    btn_login_frame = tk.Frame(root)
    btn_login_frame.pack(pady=10)

    btn_sol = tk.Button(btn_login_frame, text="Şifreler" if tr else "Passwords", width=9, height=2,command=veri_listele_ekrani)
    btn_sol.pack(side="left")

    btn_sag = tk.Button(btn_login_frame, text="Notlar"if tr else "Notes", width=9, height=2, command=notları_goster)
    btn_sag.pack(side="left")

    def guvenli_cikis():
        global ana_sifre
        ana_sifre = None
        secim_ekrani()
    
    btn_exit = tk.Button(root, text="Güvenli Çıkış"if tr else "Safe Exit", width=20, height=2, command=guvenli_cikis)
    btn_exit.pack(pady=10)

#________________________________________________________________________________________________________________
# Şifre ekleme arayüzü

def veri_ekle_ekrani():
    global entry_name, entry_pass, entry_sitename

    temizle()
    root.title("Pass Manager - Veri Ekle")
    root.geometry(ekran_boyutu)
    root.iconbitmap("app_icon/open.ico")
    tr = (dil == "TR")

    label_title = tk.Label(root, text="")
    label_title.pack(pady=10)
    
    
    label_name = tk.Label(root, text="Kullanıcı Adı"if tr else "User Name")
    label_name.pack()
    entry_name = tk.Entry(root)
    entry_name.pack()

    label_pass = tk.Label(root, text="Şifre"if tr else "Password")
    label_pass.pack()
    entry_pass = tk.Entry(root)
    entry_pass.pack()

    label_sitename = tk.Label(root, text="Site Adı/Url"if tr else "Site Name/Url")
    label_sitename.pack()
    entry_sitename = tk.Entry(root)
    entry_sitename.pack()

    btn_login = tk.Button(root, text="Kayıt Et"if tr else "Create", command=create_data)
    btn_login.pack(pady=10)

    btn_back = tk.Button(root, text=backemoji,width=3, command=ana_menu_ekrani)
    btn_back.place(x=10, y=10)

#________________________________________________________________________________________________________________
# Şifre düzenleme arayüzü

def veri_duzenle_ekrani(degerler):
    global entry_name, entry_pass, entry_sitename, duzenlenen_id

    duzenlenen_id = int(degerler[0])

    temizle()
    root.title("Pass Manager - Veri Düzenle")
    root.geometry(ekran_boyutu)
    root.iconbitmap("app_icon/open.ico")
    tr = (dil == "TR")

    label_title = tk.Label(root, text=f"{duzenlenen_id} Numaralı Kayıt" if tr else f"Record number {duzenlenen_id}")
    label_title.pack(pady=10)

    label_name = tk.Label(root, text="Kullanıcı Adı"if tr else "User Name")
    label_name.pack()
    entry_name = tk.Entry(root)
    entry_name.insert(0, degerler[1])
    entry_name.pack()

    label_pass = tk.Label(root, text="Şifre"if tr else "Password")
    label_pass.pack()
    entry_pass = tk.Entry(root)
    entry_pass.insert(0, degerler[3])
    entry_pass.pack()

    label_sitename = tk.Label(root, text="Site Adı/Url"if tr else "Site Name/Url")
    label_sitename.pack()
    entry_sitename = tk.Entry(root)
    entry_sitename.insert(0, degerler[2])
    entry_sitename.pack()

    btn_login = tk.Button(root, text="Güncelle"if tr else "Update", command=data_update)
    btn_login.pack(pady=10)

    btn_back = tk.Button(root, text=backemoji, command=veri_listele_ekrani)
    btn_back.place(x=10, y=10)

#________________________________________________________________________________________________________________
# Şifreleri listeleme arayüzü

def veri_listele_ekrani():
    global tree, secilen, entry_ara

    temizle()
    root.title("Pass Manager - Kayıtlar")
    root.geometry(ekran_boyutu)
    root.iconbitmap("app_icon/open.ico")
    tr = (dil == "TR")


    ust_frame = tk.Frame(root)
    ust_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=(10, 0))

    btn_back = tk.Button(ust_frame, text=backemoji,width=3, command=ana_menu_ekrani)
    btn_back.pack(side=tk.LEFT)

    btn_back = tk.Button(ust_frame, text=" + ",width=3, command=veri_ekle_ekrani)
    btn_back.pack(side=tk.RIGHT)

    entry_ara = tk.Entry(ust_frame, justify="center")
    entry_ara.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10, ipady=1)
    entry_ara.bind("<Return>", lambda e: view_data())

    columns = ("ID", "Kullanıcı Adı","Site Adı")
    tree = ttk.Treeview(root, columns=columns, show="headings")

    secilen = {"satir": None, "sutun": None}

    def sag_tik(event):
        satir = tree.identify_row(event.y)
        sutun = tree.identify_column(event.x)
        if not satir:
            return
        tree.selection_set(satir)
        tree.focus(satir)
        secilen["satir"] = satir
        secilen["sutun"] = int(sutun.replace("#", "")) - 1
        mymenu.post(event.x_root, event.y_root)

    def duzenle_sagtik():
        if secilen["satir"] is None:
            return
        degerler = tree.item(secilen["satir"], "values")
        veri_duzenle_ekrani(degerler)

    def ayrinti_sagtik():
        if secilen["satir"] is None:
            return
        ayrintilar(tree.item(secilen["satir"], "values"))

    mymenu = tk.Menu(root, tearoff=0)
    mymenu.add_command(label="Düzenle"if tr else "Edit", command=duzenle_sagtik)
    tree.bind("<Button-3>", sag_tik)
    mymenu.add_separator()
    mymenu.add_command(label="Sil"if tr else "Delete", command=delete_pass)
    mymenu.add_separator()
    mymenu.add_command(label="Ayrıntılar"if tr else "Details", command=ayrinti_sagtik)

    tree.heading("ID", text="ID")
    tree.column("ID", width=10, anchor="center")

    tree.heading("Kullanıcı Adı", text="Kullanıcı Adı"if tr else "User Name")
    tree.column("Kullanıcı Adı", width=75)

    tree.heading("Site Adı", text="Site Adı/Url"if tr else "Site Name/Url")
    tree.column("Site Adı", width=75)

    tree.pack(padx=10, pady=(10, 10), fill=tk.BOTH, expand=True)

    view_data()

#________________________________________________________________________________________________________________
# Şifre Ayrıntılar arayüzü

def ayrintilar(degerler):
    kayit_id = degerler[0]

    db = sqlite3.connect("pass.db")
    a = db.cursor()
    a.execute("SELECT Tarih FROM pass WHERE id=?", (kayit_id,))
    satir = a.fetchone()
    db.close()

    tarih = satir[0] if satir and satir[0] else "-"
    
    temizle()
    root.title("Pass Manager - Ayrıntılar")
    root.geometry(ekran_boyutu)
    tr = (dil == "TR")
    
    alanlar = [
        ("Kullanıcı Adı" if tr else "User Name", degerler[1]),
        ("Şifre" if tr else "Password", degerler[3]),
        ("Site Adı/Url" if tr else "Site Name/Url", degerler[2]),
        ("Tarih" if tr else "History", tarih),
    ]
    
    for etiket, deger in alanlar:
        tk.Label(root, text=etiket, font=("Segoe UI", 9, "bold")).pack(pady=(8, 0))
        
        entry = tk.Entry(root, font=("Segoe UI", 9), justify="center", relief="flat")
        entry.insert(0, str(deger))
        entry.configure(state="readonly", readonlybackground="white")
        entry.pack(pady=2)

    btn_back = tk.Button(root, text=backemoji, command=veri_listele_ekrani)
    btn_back.place(x=10, y=10)

    site = str(degerler[2]).strip()
    def siteye_git():
        url = site if site.startswith(("http://", "https://")) else "https://" + site
        webbrowser.open(url)
    
    buton = tk.Button(root, text="  Adrese Git  " if tr else "Visit Site" ,font=("Segoe UI", 8, "bold"), command=siteye_git, fg="white", bg="blue")
    uzantilar = (".com", ".org", ".gov", ".net", ".edu", ".tr")
    if not any(u in site.lower() for u in uzantilar):
        buton.config(state="disabled")
    else:
        buton.pack(pady=10)

#________________________________________________________________________________________________________________
# Not ekleme arayüzü

def not_ekranı():
    global entry_baslik, text_icerik

    temizle()
    root.title("Pass Manager - Not Ekle")
    root.geometry(ekran_boyutu)
    root.iconbitmap("app_icon/open.ico")
    tr = (dil == "TR")

    ust = tk.Frame(root)
    ust.pack(fill="x", padx=10, pady=(10, 0))
    ust.columnconfigure(1, weight=1)

    btn_back = tk.Button(ust, text=backemoji, width=3, command=ana_menu_ekrani)
    btn_back.grid(row=0, column=0, sticky="w")

    tk.Label(ust, text="Başlık" if tr else "Title").grid(row=0, column=1)

    btn_kaydet = tk.Button(ust, text=" 💾 ", width=3, command=create_notes)
    btn_kaydet.grid(row=0, column=2, sticky="e")

    entry_baslik = tk.Entry(root, justify="center")
    entry_baslik.pack(fill="x", padx=60, pady=(5, 0))

    tk.Label(root, text="İçerik" if tr else "Contents").pack(pady=(10, 0))

    alt = tk.Frame(root)
    alt.pack(fill="both", expand=True, padx=15, pady=(0, 15))

    text_icerik = tk.Text(alt, width=1, height=1, wrap="word", font=("Segoe UI", 10))
    text_icerik.tag_configure("sag", justify="right")
    text_icerik.bind("<KeyRelease>", lambda e: text_icerik.tag_add("orta", "1.0", "end"))
    text_icerik.pack(fill="both", expand=True)

#________________________________________________________________________________________________________________
# Not Listeleme Arayüzü

def notları_goster():
    global tree_notlar

    temizle()
    root.title("Pass Manager - Notlar")
    root.geometry("350x250+600+300")
    tr = (dil == "TR")

    ust_frame = tk.Frame(root)
    ust_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=(10, 0))

    btn_back = tk.Button(ust_frame, text=backemoji, width=3, command=ana_menu_ekrani)
    btn_back.pack(side=tk.LEFT)

    btn_add = tk.Button(ust_frame, text="+", width=3, command=not_ekranı)
    btn_add.pack(side=tk.RIGHT)

    columns = ("ID", "Başlık", "Tarih")
    tree_notlar = ttk.Treeview(root, columns=columns, show="headings")

    secilen_not = {"satir": None}

    def not_sag_tik(event):
        satir = tree_notlar.identify_row(event.y)
        if not satir:
            return
        tree_notlar.selection_set(satir)
        tree_notlar.focus(satir)
        secilen_not["satir"] = satir
        not_menu.post(event.x_root, event.y_root)

    def not_id_al():
        if secilen_not["satir"] is None:
            return None
        return int(tree_notlar.item(secilen_not["satir"], "values")[0])

    def not_ayrinti_sagtik():
        kayit_id = not_id_al()
        if kayit_id is not None:
            not_duzenle_ekrani(kayit_id)

    def not_sil_sagtik():
        kayit_id = not_id_al()
        if kayit_id is not None:
            delete_notes(kayit_id)
            secilen_not["satir"] = None

    not_menu = tk.Menu(root, tearoff=0)
    not_menu.add_command(label=cevir("Sil", "Delete") ,command=not_sil_sagtik)
    not_menu.add_separator()
    not_menu.add_command(label=cevir("Ayrıntılar", "Details"), command=not_ayrinti_sagtik)
    tree_notlar.bind("<Button-3>", not_sag_tik)

    tree_notlar.heading("ID", text="ID")
    tree_notlar.column("ID", width=30, anchor="center")
    tree_notlar.heading("Başlık", text="Başlık" if tr else "Title")
    tree_notlar.column("Başlık", width=120)
    tree_notlar.heading("Tarih", text="Tarih" if tr else "History")
    tree_notlar.column("Tarih", width=100)

    tree_notlar.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    view_notes()

#________________________________________________________________________________________________________________
# Not düzenleme arayüzü

def not_duzenle_ekrani(kayit_id):
    db = sqlite3.connect("pass.db")
    a = db.cursor()
    a.execute('SELECT "Başlık", "İçerik" FROM notes WHERE "ID"=?', (kayit_id,))
    satir = a.fetchone()
    db.close()

    if not satir:
        return

    baslik = cryptocode.decrypt(satir[0], ana_sifre) or ""
    icerik = cryptocode.decrypt(satir[1], ana_sifre) or ""

    temizle()
    root.title("Pass Manager - Not Düzenle")
    root.geometry(ekran_boyutu)
    root.iconbitmap("app_icon/open.ico")
    tr = (dil == "TR")

    def not_guncelle():
        yeni_baslik = entry_baslik.get().strip()
        yeni_icerik = text_icerik.get("1.0", "end-1c").strip()

        if not (yeni_baslik and yeni_icerik):
            messagebox.showwarning(cevir("Uyarı", "Warning"),cevir("Lütfen tüm alanları doldurun!", "Please fill in all fields!"))
            return

        db = sqlite3.connect("pass.db")
        a = db.cursor()
        a.execute('UPDATE notes SET "Başlık"=?, "İçerik"=? WHERE "ID"=?',
                  (cryptocode.encrypt(yeni_baslik, ana_sifre),
                   cryptocode.encrypt(yeni_icerik, ana_sifre),
                   kayit_id))
        db.commit()
        db.close()

        messagebox.showinfo(cevir("Başarılı", "Success"),cevir(f"{kayit_id} id'li not güncellendi.", f"Note {kayit_id} updated."))
        notları_goster()

    ust = tk.Frame(root)
    ust.pack(fill="x", padx=10, pady=(10, 0))
    ust.columnconfigure(1, weight=1)

    btn_back = tk.Button(ust, text=backemoji, width=4, command=notları_goster)
    btn_back.grid(row=0, column=0, sticky="w")

    tk.Label(ust, text="Başlık" if tr else "Title").grid(row=0, column=1)

    btn_kaydet = tk.Button(ust, text=" 💾 ", width=4, command=not_guncelle)
    btn_kaydet.grid(row=0, column=2, sticky="e")

    # ── Başlık kutusu ──
    entry_baslik = tk.Entry(root, justify="center")
    entry_baslik.insert(0, baslik)
    entry_baslik.pack(fill="x", padx=60, pady=(5, 0))

    # ── İçerik ──
    tk.Label(root, text="İçerik" if tr else "Contents").pack(pady=(10, 0))

    alt = tk.Frame(root)
    alt.pack(fill="both", expand=True, padx=15, pady=(0, 15))

    text_icerik = tk.Text(alt, width=1, height=1, wrap="word", font=("Segoe UI", 10))
    text_icerik.tag_configure("sag", justify="right")
    text_icerik.insert("1.0", icerik, "orta")
    text_icerik.bind("<KeyRelease>", lambda e: text_icerik.tag_add("orta", "1.0", "end"))
    text_icerik.pack(fill="both", expand=True)

#________________________________________________________________________________________________________________

root = tk.Tk()
secim_ekrani()
root.mainloop()


#________________________________________________________________________________________________________________

# (.exe olarak çıkartmak için)
# python -m PyInstaller --onefile --windowed --name PassManager --icon=app_icon\security.ico --add-data "app_icon;app_icon" main.py

#________________________________________________________________________________________________________________
