import sqlite3
import cryptocode
import tkinter as tk
from tkinter import messagebox, ttk


#________________________________________________________________________________________________________________
# Ekranları temizleme fonksiyonu

def temizle():
    for widget in root.winfo_children():
        widget.destroy()


#________________________________________________________________________________________________________________
#Giriş fonksiyonu
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
    

    a.execute("CREATE TABLE IF NOT EXISTS pass (id INTEGER PRIMARY KEY, Username TEXT, Password TEXT, Sitename TEXT)")
    a.execute("INSERT INTO pass (Username, Password, Sitename) VALUES(?, ?, ?)", (nickname, userpass, sittenname))
    db.commit()
    db.close()

    messagebox.showinfo("Başarılı", f"{sitename} bilgileri başarıyla kaydedildi!")

    entry_name.delete(0, tk.END)
    entry_pass.delete(0, tk.END)
    entry_sitename.delete(0, tk.END)


#________________________________________________________________________________________________________________
#Veri silme fonksiyonu

def delete_data():
    raw_id = entry_delete_id.get()

    try:
        deleted = int(raw_id)
    except ValueError:
        messagebox.showerror("Hata", "Lütfen geçerli bir ID giriniz.")
        return

    yanit = messagebox.askyesno(
        "Onay", f"{deleted} id'li veriyi silmek istediğinize emin misiniz?")

    if yanit:
        db = sqlite3.connect("pass.db")
        a = db.cursor()

        a.execute("DELETE FROM pass WHERE id=?", (deleted,))
        db.commit()
        db.close()

        messagebox.showinfo("Başarılı", f"{deleted} id'li veri silindi.")
        entry_delete_id.delete(0, tk.END)
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

    a.execute("CREATE TABLE IF NOT EXISTS pass (id INTEGER PRIMARY KEY, Username TEXT, Password TEXT, Sitename TEXT)")
    a.execute("SELECT * FROM pass")
    data = a.fetchall()

    for row in data:
        id_no = row[0]

        cozulen_user = cryptocode.decrypt(row[1], ana_sifre)
        cozulen_sifre = cryptocode.decrypt(row[2], ana_sifre)
        cozulen_site = cryptocode.decrypt(row[3], ana_sifre)

        if not cozulen_user:
            cozulen_user = "[Çözülemedi]"
        if not cozulen_sifre:
            cozulen_sifre = "[Çözülemedi]"
        if not cozulen_site:
            cozulen_site = "[Çözülemedi]"

        tree.insert(
            "",
            tk.END,
            values=(id_no, cozulen_user, cozulen_sifre, cozulen_site),
        )

    db.close()

#________________________________________________________________________________________________________________
#Kayıt Ve giriş ekranları arasında ekranı

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

#________________________________________________________________________________________________________________
# Giriş ekranı

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

    btn_back = tk.Button(root, text="\u2190", command=secim_ekrani)
    btn_back.place(x=10, y=10)

#________________________________________________________________________________________________________________
#kayıt ekranı

def kayit_ekrani():
    global entry_name, entry_pass, entry_email

    temizle()
    root.title("Pass Manager - Kullanıcı Kaydı")
    root.geometry("350x250+600+300")
    root.iconbitmap("app_icon/close.ico")

    label_title = tk.Label(root, text="")
    label_title.pack(pady=10)

    label_name = tk.Label(root, text="Kullanıcı Adı:")
    label_name.pack()
    entry_name = tk.Entry(root)
    entry_name.pack()

    label_pass = tk.Label(root, text="Şifre:")
    label_pass.pack()
    entry_pass = tk.Entry(root, show="*")
    entry_pass.pack()

    label_email = tk.Label(root, text="E-posta:")
    label_email.pack()
    entry_email = tk.Entry(root)
    entry_email.pack()

    btn_login = tk.Button(root, text="Kayıt Ol", command=register)
    btn_login.pack(pady=10)

    btn_back = tk.Button(root, text="\u2190", command=secim_ekrani)
    btn_back.place(x=10, y=10)

#________________________________________________________________________________________________________________
#Ana Menü ekranı

def ana_menu_ekrani():
    temizle()
    root.title("Pass Manager")
    root.geometry("350x250+600+300")
    root.iconbitmap("app_icon/open.ico")

    btn_create = tk.Button(root, text="Veri Ekle ", width=20, height=2, command=veri_ekle_ekrani)
    btn_create.pack(pady=15)

    btn_list = tk.Button(root, text="Verileri Listele", width=20, height=2, command=veri_listele_ekrani)
    btn_list.pack(pady=15)

    btn_exit = tk.Button(root, text="Güvenli Çıkış", width=20, height=2, command=secim_ekrani)
    btn_exit.pack(pady=15)


#________________________________________________________________________________________________________________
#veri kaydı ekranı

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
    entry_pass = tk.Entry(root, show="*")
    entry_pass.pack()

    label_sitename = tk.Label(root, text="Site Adı")
    label_sitename.pack()
    entry_sitename = tk.Entry(root)
    entry_sitename.pack()

    btn_login = tk.Button(root, text="Kayıt Et", command=create_data)
    btn_login.pack(pady=10)

    btn_back = tk.Button(root, text="\u2190", command=ana_menu_ekrani)
    btn_back.place(x=10, y=10)


#________________________________________________________________________________________________________________
#veri listeleme ekranı

def veri_listele_ekrani():
    global tree, entry_delete_id

    temizle()
    root.title("Pass Manager - Kayıtlar")
    root.geometry("350x250+600+300")
    root.iconbitmap("app_icon/open.ico")

    btn_back = tk.Button(root, text="\u2190", command=ana_menu_ekrani)
    btn_back.place(x=10, y=10)

    columns = ("ID", "Kullanıcı Adı", "Şifre", "Site Adı")
    tree = ttk.Treeview(root, columns=columns, show="headings")

    frame_delete = tk.Frame(root)
    frame_delete.pack(pady=(10, 0))

    tk.Label(frame_delete, text="Silmek için ID").pack(side=tk.LEFT, padx=5, pady=2)
    entry_delete_id = tk.Entry(frame_delete, width=10)
    entry_delete_id.pack(side=tk.LEFT, padx=5)

    btn_delete = tk.Button(
        frame_delete, text="Veriyi Sil", command=delete_data, fg="black"
    )
    btn_delete.pack(side=tk.LEFT, padx=5)

    tree.heading("ID", text="ID")
    tree.column("ID", width=10, anchor="center")

    tree.heading("Kullanıcı Adı", text="Kullanıcı Adı")
    tree.column("Kullanıcı Adı", width=75)

    tree.heading("Şifre", text="Şifre")
    tree.column("Şifre", width=100)

    tree.heading("Site Adı", text="Site Adı")
    tree.column("Site Adı", width=75)

    tree.pack(padx=10, pady=(10, 10), fill=tk.BOTH, expand=True)

    view_data()


root = tk.Tk()
secim_ekrani()
root.mainloop()