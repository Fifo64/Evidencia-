import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import sqlite3
from PIL import Image, ImageTk

DB_FILE = "evidencia.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS osoby (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        meno TEXT,
                        priezvisko TEXT,
                        trestny_cin TEXT,
                        fotka TEXT)''')
    conn.commit()
    conn.close()

def pridaj_osobu():
    meno = meno_entry.get()
    priezvisko = priezvisko_entry.get()
    trestny_cin = trestny_cin_entry.get()
    fotka = fotka_path.get()
    if not meno or not priezvisko or not trestny_cin or not fotka:
        messagebox.showerror("Chyba", "Vyplň všetky údaje!")
        return
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO osoby (meno, priezvisko, trestny_cin, fotka) VALUES (?, ?, ?, ?)",
                   (meno, priezvisko, trestny_cin, fotka))
    conn.commit()
    conn.close()
    messagebox.showinfo("Úspech", "Osoba bola pridaná.")
    refresh_table()

def vyber_fotku():
    file_path = filedialog.askopenfilename(filetypes=[("Obrázky", "*.png;*.jpg;*.jpeg")])
    if file_path:
        fotka_path.set(file_path)

def refresh_table():
    for row in tree.get_children():
        tree.delete(row)
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM osoby")
    rows = cursor.fetchall()
    for row in rows:
        tree.insert("", tk.END, values=row)
    conn.close()

def vyhladaj_osobu():
    query = search_entry.get()
    for row in tree.get_children():
        tree.delete(row)
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM osoby WHERE meno LIKE ? OR trestny_cin LIKE ?", 
                   (f"%{query}%", f"%{query}%"))
    rows = cursor.fetchall()
    for row in rows:
        tree.insert("", tk.END, values=row)
    conn.close()

def vymaz_osobu():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Chyba", "Vyber osobu na vymazanie!")
        return
    osoba_id = tree.item(selected_item[0])['values'][0]
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM osoby WHERE id = ?", (osoba_id,))
    conn.commit()
    conn.close()
    messagebox.showinfo("Úspech", "Osoba bola vymazaná.")
    refresh_table()

def edituj_osobu():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Chyba", "Vyber osobu na editáciu!")
        return
    osoba_id = tree.item(selected_item[0])['values'][0]
    meno = meno_entry.get()
    priezvisko = priezvisko_entry.get()
    trestny_cin = trestny_cin_entry.get()
    fotka = fotka_path.get()
    if not meno or not priezvisko or not trestny_cin or not fotka:
        messagebox.showerror("Chyba", "Vyplň všetky údaje!")
        return
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("UPDATE osoby SET meno = ?, priezvisko = ?, trestny_cin = ?, fotka = ? WHERE id = ?",
                   (meno, priezvisko, trestny_cin, fotka, osoba_id))
    conn.commit()
    conn.close()
    messagebox.showinfo("Úspech", "Osoba bola upravená.")
    refresh_table()

# Hlavné okno
app = tk.Tk()
app.title("Evidencia osôb")
app.geometry("900x600")
app.configure(bg="black")  # Nastavenie čierneho pozadia

# Logo v každom rohu
logo_image = Image.open("logo.png").resize((50, 50))  # Nahraď "logo.png" cestou k tvojmu logu
logo_photo = ImageTk.PhotoImage(logo_image)
tk.Label(app, image=logo_photo, bg="black").grid(row=0, column=0, sticky="nw")
tk.Label(app, image=logo_photo, bg="black").grid(row=0, column=2, sticky="ne")
tk.Label(app, image=logo_photo, bg="black").grid(row=7, column=0, sticky="sw")
tk.Label(app, image=logo_photo, bg="black").grid(row=7, column=2, sticky="se")

# Formulár
tk.Label(app, text="Meno:", bg="black", fg="white").grid(row=1, column=0, sticky=tk.W)
meno_entry = tk.Entry(app)
meno_entry.grid(row=1, column=1)

tk.Label(app, text="Priezvisko:", bg="black", fg="white").grid(row=2, column=0, sticky=tk.W)
priezvisko_entry = tk.Entry(app)
priezvisko_entry.grid(row=2, column=1)

tk.Label(app, text="Trestný čin:", bg="black", fg="white").grid(row=3, column=0, sticky=tk.W)
trestny_cin_entry = tk.Entry(app)
trestny_cin_entry.grid(row=3, column=1)

tk.Label(app, text="Fotka:", bg="black", fg="white").grid(row=4, column=0, sticky=tk.W)
fotka_path = tk.StringVar()
fotka_entry = tk.Entry(app, textvariable=fotka_path, state='readonly')
fotka_entry.grid(row=4, column=1)
tk.Button(app, text="Vybrať...", command=vyber_fotku).grid(row=4, column=2)

# Tabuľka
columns = ("ID", "Meno", "Priezvisko", "Trestný čin", "Fotka")
tree = ttk.Treeview(app, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
tree.grid(row=6, column=0, columnspan=3, sticky="nsew")

# Spustenie
init_db()
refresh_table()
app.mainloop()
