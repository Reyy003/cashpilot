import customtkinter as ctk
from tkinter import messagebox
from tkcalendar import DateEntry

from query import (
    get_transaction_by_id,
    update_transaction
)


class EditTransaction(ctk.CTkToplevel):

    def __init__(self, parent, transaction_id, callback):
        super().__init__(parent)

        self.transaction_id = transaction_id
        self.callback = callback

        self.title("Edit Transaksi")
        self.geometry("420x520")
        self.configure(fg_color="#0f172a")  # Dark Slate Background
        self.resizable(False, False)
        self.grab_set()

        # Ambil data transaksi dari database
        data = get_transaction_by_id(transaction_id)

        # Header Title
        ctk.CTkLabel(
            self,
            text="✏ Edit Detail Transaksi",
            font=("Arial", 16, "bold"),
            text_color="#38bdf8"
        ).pack(pady=(20, 15))

        form_frame = ctk.CTkFrame(self, fg_color="#1e293b", corner_radius=10)
        form_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # 1. Input Tanggal
        ctk.CTkLabel(form_frame, text="Tanggal Transaksi:", font=("Arial", 11, "bold"), text_color="#e2e8f0").pack(anchor="w", padx=20, pady=(15, 2))
        self.tanggal = DateEntry(
            form_frame,
            width=26,
            background='darkblue',
            foreground='white',
            date_pattern="yyyy-mm-dd"
        )
        self.tanggal.pack(anchor="w", padx=20, pady=(0, 10))
        if data.get("tanggal"):
            self.tanggal.set_date(data["tanggal"])

        # 2. Input Keterangan / Detail Barang
        ctk.CTkLabel(form_frame, text="Keterangan / Detail Barang:", font=("Arial", 11, "bold"), text_color="#e2e8f0").pack(anchor="w", padx=20, pady=(5, 2))
        self.keterangan = ctk.CTkEntry(
            form_frame,
            width=340,
            placeholder_text="Masukkan detail barang/keterangan"
        )
        self.keterangan.pack(anchor="w", padx=20, pady=(0, 10))
        self.keterangan.insert(0, data.get("keterangan", ""))

        # 3. Option Menu Jenis Transaksi
        ctk.CTkLabel(form_frame, text="Jenis Transaksi:", font=("Arial", 11, "bold"), text_color="#e2e8f0").pack(anchor="w", padx=20, pady=(5, 2))
        self.jenis = ctk.CTkOptionMenu(
            form_frame,
            width=340,
            values=["Pemasukan", "Pengeluaran"],
            fg_color="#334155",
            button_color="#475569"
        )
        self.jenis.pack(anchor="w", padx=20, pady=(0, 10))
        self.jenis.set(data.get("jenis", "Pengeluaran"))

        # 4. Input Nominal
        ctk.CTkLabel(form_frame, text="Nominal (Rp):", font=("Arial", 11, "bold"), text_color="#e2e8f0").pack(anchor="w", padx=20, pady=(5, 2))
        self.nominal = ctk.CTkEntry(
            form_frame,
            width=340,
            placeholder_text="Contoh: 50000"
        )
        self.nominal.pack(anchor="w", padx=20, pady=(0, 15))
        self.nominal.insert(0, str(data.get("nominal", 0)))

        # Tombol Aksi
        btn_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        btn_frame.pack(fill="x", padx=20, pady=(5, 15))

        btn_save = ctk.CTkButton(
            btn_frame,
            text="Simpan Perubahan",
            fg_color="#f59e0b",
            hover_color="#d97706",
            font=("Arial", 12, "bold"),
            command=self.save
        )
        btn_save.pack(side="right")

        btn_cancel = ctk.CTkButton(
            btn_frame,
            text="Batal",
            fg_color="#64748b",
            hover_color="#475569",
            command=self.destroy
        )
        btn_cancel.pack(side="right", padx=8)

    def save(self):
        # Validasi nominal angka
        try:
            nominal_val = float(self.nominal.get().replace(",", "").replace(".", ""))
            if nominal_val <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Format Salah", "Masukkan jumlah nominal angka yang valid!")
            return

        if not self.keterangan.get().strip():
            messagebox.showwarning("Peringatan", "Keterangan transaksi tidak boleh kosong!")
            return

        # Update data transaksi di database
        update_transaction(
            self.transaction_id,
            self.tanggal.get(),
            self.keterangan.get().strip(),
            self.jenis.get(),
            nominal_val
        )

        messagebox.showinfo("Berhasil", "Transaksi berhasil diperbarui")

        # Panggil callback untuk merefresh data tabel utama
        if self.callback:
            self.callback()

        self.destroy()