#________________________________________________________________________________________________________________
# Kullanılan kütüphaneler
import sqlite3
import webbrowser
import cryptocode
import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime

#________________________________________________________________________________________________________________

# Veri Arama modülü kutucuğu eklenecek.

#________________________________________________________________________________________________________________
# Ara fonksiyonlar

versiyon = "1.2.1"
backemoji = " \u2190 "

def temizle():
    for widget in root.winfo_children():
        widget.destroy()

def tarih_info():
    now = datetime.now()
    tarih = now.strftime("%d/%m/%Y %H:%M:%S")
    return tarih

#________________________________________________________________________________________________________________
#Giriş ve şifremi unuttum fonksiyonu

yanlis = 0
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
            messagebox.showinfo("Başarılı", "Giriş Başarılı!")
            ana_menu_ekrani()
        else:
            yanlis += 1
            messagebox.showerror("Hata", "Kullanıcı adı veya şifre hatalı!")
            if yanlis >= 3:
                messagebox.showerror("Hata", "3 kez hatalı giriş yaptınız.")
                yanlis = 0
                root.destroy()

    else:
        messagebox.showwarning(
            "Uyarı", "Lütfen kullanıcı adı ve şifre girin!")

#________________________________________________________________________________________________________________
#kullanıcı kayıt Fonksiyonu 

def register():

    username = entry_name.get()
    password = entry_pass.get()
    email = entry_email.get()

    if not (username and password and email):
        messagebox.showwarning("Uyarı", "Lütfen tüm alanları doldurun!")
        return

    elif len(password) < 6:
        messagebox.showwarning("Uyarı", "Şifre en az 6 karakter uzunluğunda olmalıdır!")
        return

    db = sqlite3.connect("Log.db")
    a = db.cursor()

    a.execute("CREATE TABLE IF NOT EXISTS Log (id INTEGER PRIMARY KEY, Username TEXT, Password TEXT, Email TEXT)")

    a.execute("SELECT COUNT(*) FROM Log")
    if a.fetchone()[0] > 0:
        db.close()
        messagebox.showwarning("Uyarı", "Zaten bir kullanıcı kayıtlı, yeni kayıt yapılamaz!")
        return

    sifreli = cryptocode.encrypt(password, password)
    usersifreli = cryptocode.encrypt(username, password)
    emailsifreli = cryptocode.encrypt(email, password)

    a.execute("INSERT INTO Log (Username, Password, Email) VALUES(?, ?, ?)", (usersifreli, sifreli, emailsifreli))
    db.commit()
    db.close()

    messagebox.showinfo("Başarılı", "Kaydınız Başarılı Bir Şekilde Oluşturulmuştur!")
    secim_ekrani()

#________________________________________________________________________________________________________________
#Veri tabanı oluşturma ve veri ekleme fonksiyonu

def create_data():
    username = entry_name.get()
    sitename = entry_sitename.get()
    password = entry_pass.get()

    if not (username and password and sitename):
        messagebox.showwarning("Uyarı", "Lütfen tüm alanları doldurun!")
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

    messagebox.showinfo("Başarılı", f"{sitename} bilgileri başarıyla kaydedildi!")

    entry_name.delete(0, tk.END)
    entry_pass.delete(0, tk.END)
    entry_sitename.delete(0, tk.END)

#________________________________________________________________________________________________________________
#Veri güncelleme fonksiyonu

def data_update():
    new_username = entry_name.get()
    new_password = entry_pass.get()
    new_sitename = entry_sitename.get()

    if not (new_username and new_password and new_sitename):
        messagebox.showwarning("Uyarı", "Lütfen tüm alanları doldurun!")
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

    messagebox.showinfo("Başarılı", f"{duzenlenen_id} id'li veri güncellendi.")
    veri_listele_ekrani()
#________________________________________________________________________________________________________________
#Veri silme fonksiyonu

def delete_data():
    if secilen["satir"] is None:
        return

    degerler = tree.item(secilen["satir"], "values")
    deleted = int(degerler[0])  # ilk sütun ID

    yanit = messagebox.askyesno(
       "Onay", f"{deleted} id'li veriyi silmek istediğinize emin misiniz?"
        )

    if yanit:
        db = sqlite3.connect("pass.db")
        a = db.cursor()

        a.execute("DELETE FROM pass WHERE id=?", (deleted,))
        db.commit()
        db.close()

        messagebox.showinfo("Başarılı", f"{deleted} id'li veri silindi.")
        secilen["satir"] = None
        view_data()
    else:
        messagebox.showinfo("İptal", "Silme işlemi iptal ediliyor.")

#________________________________________________________________________________________________________________
#verileri görüntüleme fonksiyonu

def view_data():

    for row in tree.get_children():
        tree.delete(row)

    db = sqlite3.connect("pass.db")
    a = db.cursor()

    a.execute("CREATE TABLE IF NOT EXISTS pass (id INTEGER PRIMARY KEY, Username TEXT, Password TEXT, Sitename TEXT, Tarih TEXT)")
    a.execute("SELECT * FROM pass")
    data = a.fetchall()

    for row in data:
        id_no = row[0]

        cozulen_user = cryptocode.decrypt(row[1], ana_sifre)
        cozulen_sifre = cryptocode.decrypt(row[2], ana_sifre)
        cozulen_site = cryptocode.decrypt(row[3], ana_sifre)

        if not cozulen_user:
            cozulen_user = "______________"
        if not cozulen_sifre:
            cozulen_sifre = "_____________"
        if not cozulen_site:
            cozulen_site = "______________"

        tree.insert(
            "",
            tk.END,
            values=(id_no, cozulen_user, cozulen_site, cozulen_sifre),
        )

    db.close()

#________________________________________________________________________________________________________________
#Kayıt Ve giriş seçim ara yüzü

def secim_ekrani():
    temizle()
    root.title("Pass Manager")
    root.geometry("350x250+600+300")
    root.iconbitmap("app_icon/close.ico")

    label_title = tk.Label(root, text="")
    label_title.pack(pady=10)

    # Seçim Ekranı
    btn_login = tk.Button(root, text="Giriş Yap", width=20, height=2, command=giris_ekrani)
    btn_login.pack(pady=10)

    btn_register = tk.Button(root, text="Kayıt Ol", width=20, height=2, command=kayit_ekrani)
    btn_register.pack(pady=10)

    label_info = tk.Label(root, text=f"Versiyon: {versiyon}", fg="gray")
    label_info.pack(side=tk.BOTTOM, pady=10)

#________________________________________________________________________________________________________________
# Giriş ara yüzü

def giris_ekrani():
    global entry_name, entry_pass

    temizle()
    root.title("Pass Manager - Giriş Ekranı")
    root.geometry("350x250+600+300")
    root.iconbitmap("app_icon/close.ico")

    label_title = tk.Label(root, text="")
    label_title.pack(pady=10)

    label_name = tk.Label(root, text="Kullanıcı Adı")
    label_name.pack()
    entry_name = tk.Entry(root)
    entry_name.pack()

    label_pass = tk.Label(root, text="Şifre")
    label_pass.pack()
    entry_pass = tk.Entry(root, show="*")
    entry_pass.pack()

    btn_login = tk.Button(root, text="Giriş Yap", command=login)
    btn_login.pack(pady=10)

    btn_back = tk.Button(root, text=backemoji, command=secim_ekrani)
    btn_back.place(x=10, y=10)

#________________________________________________________________________________________________________________
#kayıt ara yüzü

def kayit_ekrani():
    global entry_name, entry_pass, entry_email

    temizle()
    root.title("Pass Manager - Kullanıcı Kaydı")
    root.geometry("350x250+600+300")
    root.iconbitmap("app_icon/close.ico")

    label_title = tk.Label(root, text="")
    label_title.pack(pady=10)

    label_name = tk.Label(root, text="Kullanıcı Adı")
    label_name.pack()
    entry_name = tk.Entry(root)
    entry_name.pack()

    label_pass = tk.Label(root, text="Şifre")
    label_pass.pack()
    entry_pass = tk.Entry(root, show="*")
    entry_pass.pack()

    label_email = tk.Label(root, text="E-posta")
    label_email.pack()
    entry_email = tk.Entry(root)
    entry_email.pack()

    btn_login = tk.Button(root, text="Kayıt Ol", command=register)
    btn_login.pack(pady=10)

    btn_back = tk.Button(root, text=backemoji, command=secim_ekrani)
    btn_back.place(x=10, y=10)

#________________________________________________________________________________________________________________
#Ana Menü ara yüzü

def ana_menu_ekrani():
    temizle()
    root.title("Pass Manager")
    root.geometry("350x250+600+300")
    root.iconbitmap("app_icon/open.ico")

    btn_create = tk.Button(root, text="Veri Ekle ", width=20, height=2, command=veri_ekle_ekrani)
    btn_create.pack(pady=15)

    btn_list = tk.Button(root, text="Verileri Listele", width=20, height=2, command=veri_listele_ekrani)
    btn_list.pack(pady=15)

    def guvenli_cikis():
        global ana_sifre
        ana_sifre = None
        secim_ekrani()
    
    btn_exit = tk.Button(root, text="Güvenli Çıkış", width=20, height=2, command=guvenli_cikis)
    btn_exit.pack(pady=15)

#________________________________________________________________________________________________________________
#veri kaydı ara yüzü

def veri_ekle_ekrani():
    global entry_name, entry_pass, entry_sitename

    temizle()
    root.title("Pass Manager - Veri Ekle")
    root.geometry("350x250+600+300")
    root.iconbitmap("app_icon/open.ico")

    label_title = tk.Label(root, text="")
    label_title.pack(pady=10)

    label_name = tk.Label(root, text="Kullanıcı Adı")
    label_name.pack()
    entry_name = tk.Entry(root)
    entry_name.pack()

    label_pass = tk.Label(root, text="Şifre")
    label_pass.pack()
    entry_pass = tk.Entry(root)
    entry_pass.pack()

    label_sitename = tk.Label(root, text="Site Adı/Url")
    label_sitename.pack()
    entry_sitename = tk.Entry(root)
    entry_sitename.pack()

    btn_login = tk.Button(root, text="Kayıt Et", command=create_data)
    btn_login.pack(pady=10)

    btn_back = tk.Button(root, text=backemoji, command=ana_menu_ekrani)
    btn_back.place(x=10, y=10)

#________________________________________________________________________________________________________________
#veri düzenleme arayüzü

def veri_duzenle_ekrani(degerler):
    global entry_name, entry_pass, entry_sitename, duzenlenen_id

    duzenlenen_id = int(degerler[0])

    temizle()
    root.title("Pass Manager - Veri Düzenle")
    root.geometry("350x250+600+300")
    root.iconbitmap("app_icon/open.ico")

    label_title = tk.Label(root, text=f"{duzenlenen_id} Numaralı Kayıt")
    label_title.pack(pady=10)

    label_name = tk.Label(root, text="Kullanıcı Adı")
    label_name.pack()
    entry_name = tk.Entry(root)
    entry_name.insert(0, degerler[1])
    entry_name.pack()

    label_pass = tk.Label(root, text="Şifre")
    label_pass.pack()
    entry_pass = tk.Entry(root)
    entry_pass.insert(0, degerler[3])
    entry_pass.pack()

    label_sitename = tk.Label(root, text="Site Adı/Url")
    label_sitename.pack()
    entry_sitename = tk.Entry(root)
    entry_sitename.insert(0, degerler[2])
    entry_sitename.pack()

    btn_login = tk.Button(root, text="Güncelle", command=data_update)
    btn_login.pack(pady=10)

    btn_back = tk.Button(root, text=backemoji, command=veri_listele_ekrani)
    btn_back.place(x=10, y=10)

#________________________________________________________________________________________________________________
#veri listeleme ara yüzü

def veri_listele_ekrani():
    global tree, entry_delete_id, secilen

    temizle()
    root.title("Pass Manager - Kayıtlar")
    root.geometry("350x250+600+300")
    root.iconbitmap("app_icon/open.ico")

    ust_frame = tk.Frame(root)
    ust_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=(10, 0))

    btn_back = tk.Button(ust_frame, text=backemoji, command=ana_menu_ekrani)
    btn_back.pack(side=tk.LEFT)

    btn_back = tk.Button(ust_frame, text=" \u002B ", command=veri_ekle_ekrani)
    btn_back.pack(side=tk.RIGHT)

    # entry_ara = tk.Entry(ust_frame, justify="center")
    # entry_ara.pack(side=tk.LEFT, fill="x", expand=True, padx=10, ipady=1)
    # entry_ara.insert(0, "Arama Modülü Geliştirme Aşamasında")

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

    def hucreyi_kopyala():
        if secilen["satir"] is None:
            return
        degerler = tree.item(secilen["satir"], "values")
        root.clipboard_clear()
        root.clipboard_append(str(degerler[secilen["sutun"]]))

    def ayrinti_sagtik():
        if secilen["satir"] is None:
            return
        ayrintilar(tree.item(secilen["satir"], "values"))

    mymenu = tk.Menu(root, tearoff=0)
    # mymenu.add_command(label="Kopyala", command=hucreyi_kopyala)
    # mymenu.add_separator()
    mymenu.add_command(label="Düzenle", command=duzenle_sagtik)
    tree.bind("<Button-3>", sag_tik)
    mymenu.add_separator()
    mymenu.add_command(label="Sil", command=delete_data)
    mymenu.add_separator()
    mymenu.add_command(label="Ayrıntılar", command=ayrinti_sagtik)

    tree.heading("ID", text="ID")
    tree.column("ID", width=10, anchor="center")

    tree.heading("Kullanıcı Adı", text="Kullanıcı Adı")
    tree.column("Kullanıcı Adı", width=75)

    tree.heading("Site Adı", text="Site Adı/Url")
    tree.column("Site Adı", width=75)

    tree.pack(padx=10, pady=(10, 10), fill=tk.BOTH, expand=True)

    view_data()

#________________________________________________________________________________________________________________
# Ayrıntılar ara yüzü

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
    root.geometry("350x250+600+300")
    
    alanlar = [
        ("Kullanıcı Adı", degerler[1]),
        ("Şifre", degerler[3]),
        ("Site Adı/Url", degerler[2]),
        ("Tarih", tarih),
    ]
    
    for etiket, deger in alanlar:
        tk.Label(root, text=etiket, font=("Segoe UI", 9, "bold")).pack(pady=(8, 0))
        
        entry = tk.Entry(root, font=("Segoe UI", 9), justify="center", relief="flat")
        entry.insert(0, str(deger))
        entry.configure(state="readonly", readonlybackground="#f0f0f0")
        entry.pack(pady=2)

    btn_back = tk.Button(root, text=backemoji, command=veri_listele_ekrani)
    btn_back.place(x=10, y=10)

    site = str(degerler[2]).strip()
    def siteye_git():
        url = site if site.startswith(("http://", "https://")) else "https://" + site
        webbrowser.open(url)
    
    buton = tk.Button(root, text="  Adrese Git  ",font=("Segoe UI", 8, "bold"), command=siteye_git, fg="white", bg="blue")
    uzantilar = (".com", ".org", ".gov", ".net", ".edu", ".tr")
    if not any(u in site.lower() for u in uzantilar):
        buton.config(state="disabled")
    else:
        buton.pack(pady=10)

#________________________________________________________________________________________________________________





root = tk.Tk()
secim_ekrani()
root.mainloop()