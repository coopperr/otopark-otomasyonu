import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime


toplam_kapasite = 3
otoparktaki_arac_sayisi = 1
saatlik_ucret = 20
sabit_ucret = 50
saniye_basi_ucret = 10



def create_db():
    conn = sqlite3.connect("otopark.db")
    cursor = conn.cursor()


    cursor.execute("DROP TABLE IF EXISTS arac_kayitlari")
    cursor.execute("""
    CREATE TABLE arac_kayitlari (
        plaka TEXT,
        arac_tipi TEXT,
        kullanici_adi TEXT,
        giris_zamani TEXT,
        cikis_zamani TEXT,
        otoparkta INTEGER
    )
    """)


    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        kullanici_adi TEXT PRIMARY KEY,
        sifre TEXT
    )
    """)

    conn.commit()
    conn.close()

def uye_ol():
    uye_penceresi = tk.Toplevel()
    uye_penceresi.title("Üye Ol")
    uye_penceresi.geometry("400x300")
    uye_penceresi.configure(bg='#333')

    def kayit_uye():
        kullanici_adi = entry_kullanici_adi.get().strip()
        sifre = entry_sifre.get().strip()

        if not kullanici_adi or not sifre:
            messagebox.showerror("Hata", "Lütfen tüm alanları doldurun.")
            return

        conn = sqlite3.connect("otopark.db")
        cursor = conn.cursor()

        try:
            cursor.execute("INSERT INTO users (kullanici_adi, sifre) VALUES (?, ?)", (kullanici_adi, sifre))
            conn.commit()
            messagebox.showinfo("Başarılı", "Kayıt başarıyla tamamlandı.")
        except sqlite3.IntegrityError:
            messagebox.showerror("Hata", "Bu kullanıcı adı zaten kayıtlı.")
        finally:
            conn.close()

        uye_penceresi.destroy()

    tk.Label(uye_penceresi, text="Üye Ol", font=("Helvetica", 16, "bold"), bg="#333", fg="white").pack(pady=20)
    form_frame = tk.Frame(uye_penceresi, bg="#333")
    form_frame.pack(pady=10)

    tk.Label(form_frame, text="Kullanıcı Adı:", bg="#333", fg="white").grid(row=0, column=0, sticky="w", pady=5)
    entry_kullanici_adi = tk.Entry(form_frame)
    entry_kullanici_adi.grid(row=0, column=1, pady=5)

    tk.Label(form_frame, text="Şifre:", bg="#333", fg="white").grid(row=1, column=0, sticky="w", pady=5)
    entry_sifre = tk.Entry(form_frame, show="*")
    entry_sifre.grid(row=1, column=1, pady=5)

    tk.Button(uye_penceresi, text="Kaydol", bg="#28a745", fg="white", font=("Helvetica", 12), command=kayit_uye).pack(pady=20)


def arac_girisi():
    arac_penceresi = tk.Toplevel()
    arac_penceresi.title("Araç Girişi")
    arac_penceresi.geometry("400x400")
    arac_penceresi.configure(bg='#333')

    def arac_giris_kayit():
        global otoparktaki_arac_sayisi
        kullanici_adi = entry_kullanici_adi.get().strip()
        plaka = entry_plaka.get().strip().upper()
        arac_tipi = combo_arac_tipi.get()

        if not kullanici_adi or not plaka or not arac_tipi:
            messagebox.showerror("Hata", "Lütfen tüm alanları doldurun.")
            return

        conn = sqlite3.connect("otopark.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE kullanici_adi = ?", (kullanici_adi,))
        user = cursor.fetchone()

        if not user:
            messagebox.showerror("Hata", "Kullanıcı adı geçersiz.")
            conn.close()
            return

        if otoparktaki_arac_sayisi >= toplam_kapasite:
            messagebox.showerror("Hata", "Otopark dolu.")
        else:
            try:
                giris_zamani = datetime.now().strftime('%Y-%m-%d %H:%M:%S')


                cursor.execute("UPDATE arac_kayitlari SET giris_zamani = ?, cikis_zamani = NULL, otoparkta = 1 WHERE plaka = ?",
                               (giris_zamani, plaka))

                cursor.execute(
                    "INSERT INTO arac_kayitlari (plaka, arac_tipi, kullanici_adi, giris_zamani, otoparkta) VALUES (?, ?, ?, ?, 1)",
                    (plaka, arac_tipi, kullanici_adi, giris_zamani))

                conn.commit()
                otoparktaki_arac_sayisi += 1
                messagebox.showinfo("Başarılı", f"{plaka} plakalı araç giriş yaptı.")
            except sqlite3.IntegrityError:
                messagebox.showerror("Hata", "Bu araç zaten otoparkta.")
            finally:
                conn.close()

            arac_penceresi.destroy()

    tk.Label(arac_penceresi, text="Araç Girişi", font=("Helvetica", 16, "bold"), bg="#333", fg="white").pack(pady=20)
    form_frame = tk.Frame(arac_penceresi, bg="#333")
    form_frame.pack(pady=10)

    tk.Label(form_frame, text="Kullanıcı Adı:", bg="#333", fg="white").grid(row=0, column=0, sticky="w", pady=5)
    entry_kullanici_adi = tk.Entry(form_frame)
    entry_kullanici_adi.grid(row=0, column=1, pady=5)

    tk.Label(form_frame, text="Araç Plakası:", bg="#333", fg="white").grid(row=1, column=0, sticky="w", pady=5)
    entry_plaka = tk.Entry(form_frame)
    entry_plaka.grid(row=1, column=1, pady=5)

    tk.Label(form_frame, text="Araç Tipi:", bg="#333", fg="white").grid(row=2, column=0, sticky="w", pady=5)
    combo_arac_tipi = ttk.Combobox(form_frame, values=["Araba", "Tır", "Motor"])
    combo_arac_tipi.grid(row=2, column=1, pady=5)

    tk.Button(arac_penceresi, text="Araç Girişi Yap", bg="#28a745", fg="white", font=("Helvetica", 12), command=arac_giris_kayit).pack(pady=20)


def arac_cikisi():
    cikis_penceresi = tk.Toplevel()
    cikis_penceresi.title("Araç Çıkışı")
    cikis_penceresi.geometry("400x300")
    cikis_penceresi.configure(bg='#333')

    def arac_cikis_kayit():
        global otoparktaki_arac_sayisi
        plaka = entry_plaka.get().strip().upper()

        if not plaka:
            messagebox.showerror("Hata", "Lütfen plaka bilgisini girin.")
            return

        conn = sqlite3.connect("otopark.db")
        cursor = conn.cursor()

        cikis_zamani = datetime.now()

        try:

            cursor.execute("SELECT giris_zamani, COUNT(*) FROM arac_kayitlari WHERE plaka = ?", (plaka,))
            sonuc = cursor.fetchone()

            if not sonuc[0]:
                messagebox.showerror("Hata", "Bu plakaya ait aktif bir otopark kaydı bulunamadı.")
                return

            giris_zamani = datetime.strptime(sonuc[0], '%Y-%m-%d %H:%M:%S')
            giris_sayisi = sonuc[1]
            gecen_sure = (cikis_zamani - giris_zamani).total_seconds()


            if giris_sayisi == 1:
                indirim_orani = 0
            elif giris_sayisi == 2:
                indirim_orani = 0.05
            elif giris_sayisi == 3:
                indirim_orani = 0.10
            elif giris_sayisi == 4:
                indirim_orani = 0.15
            else:
                indirim_orani = 0.20

            ek_ucret = int(gecen_sure) * saniye_basi_ucret
            toplam_ucret = sabit_ucret + ek_ucret
            indirim_miktari = toplam_ucret * indirim_orani
            toplam_ucret -= indirim_miktari


            cursor.execute(
                "UPDATE arac_kayitlari SET cikis_zamani = NULL, otoparkta = 1 WHERE plaka = ?",
                (plaka,))

            conn.commit()

            otoparktaki_arac_sayisi -= 1

            messagebox.showinfo(
                "Çıkış Yapıldı",
                f"Araç çıkışı başarıyla yapıldı.\nGeçirilen süre: {int(gecen_sure)} saniye\nİndirim Oranı: %{int(indirim_orani * 100)}\nToplam Ücret: {toplam_ucret:.2f} TL"
            )
        except Exception as e:
            messagebox.showerror("Hata", f"Bir hata oluştu: {e}")
        finally:
            conn.close()
            cikis_penceresi.destroy()

    tk.Label(cikis_penceresi, text="Araç Çıkışı", font=("Helvetica", 16, "bold"), bg="#333", fg="white").pack(pady=20)
    form_frame = tk.Frame(cikis_penceresi, bg="#333")
    form_frame.pack(pady=10)

    tk.Label(form_frame, text="Plaka:", bg="#333", fg="white").grid(row=0, column=0, sticky="w", pady=5)
    entry_plaka = tk.Entry(form_frame)
    entry_plaka.grid(row=0, column=1, pady=5)

    tk.Button(cikis_penceresi, text="Araç Çıkışı Yap", bg="#28a745", fg="white", font=("Helvetica", 12), command=arac_cikis_kayit).pack(pady=20)


root = tk.Tk()
root.title("Otopark Otomasyonu")
root.geometry("400x400")
root.configure(bg='#2d2d2d')

create_db()

tk.Label(root, text="Otopark Otomasyonu", font=("Helvetica", 20, "bold"), fg="green", bg="#2d2d2d").pack(pady=20)

btn_uye_ol = tk.Button(root, text="Üye Ol", font=("Helvetica", 14), bg="blue", fg="white", command=uye_ol)
btn_uye_ol.pack(pady=10, fill='x', padx=50)

btn_arac_girisi = tk.Button(root, text="Araç Girişi", font=("Helvetica", 14), bg="blue", fg="white", command=arac_girisi)
btn_arac_girisi.pack(pady=10, fill='x', padx=50)

btn_arac_cikisi = tk.Button(root, text="Araç Çıkışı", font=("Helvetica", 14), bg="blue", fg="white", command=arac_cikisi)
btn_arac_cikisi.pack(pady=10, fill='x', padx=50)

root.mainloop()