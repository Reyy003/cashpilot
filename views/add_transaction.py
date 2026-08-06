import os
import shutil
from datetime import datetime
from tkinter import filedialog, messagebox

import customtkinter as ctk
from tkcalendar import DateEntry

from query import add_transaction


class DynamicItemRow(ctk.CTkFrame):
    """Komponen Card / Baris Input Barang Dinamis dengan Warna Serasi"""

    # Kategori khusus terpisah
    CATEGORIES_PENGELUARAN = ["Material", "Tenaga", "Alat Kerja", "Operasional", "Prive"]
    CATEGORIES_PEMASUKAN = ["Saldo Awal", "Saldo Masuk"]

    def __init__(self, parent, index, remove_callback, update_total_callback, project_id, get_jenis_callback):
        # Card Background Slate Navy (#1e293b)
        super().__init__(parent, fg_color="#1e293b", corner_radius=8, border_width=1, border_color="#334155")

        self.index = index
        self.remove_callback = remove_callback
        self.update_total_callback = update_total_callback
        self.project_id = project_id
        self.get_jenis_callback = get_jenis_callback
        self.nota_path = ""

        self.pack(fill="x", pady=6, padx=5)

        # Header Baris / Card Item
        self.lbl_title = ctk.CTkLabel(
            self,
            text=f"Item #{self.index}",
            font=("Arial", 11, "bold"),
            text_color="#94a3b8"
        )
        self.lbl_title.grid(row=0, column=0, columnspan=2, sticky="w", padx=10, pady=(6, 2))

        # Tombol Hapus Baris
        self.btn_delete = ctk.CTkButton(
            self,
            text="🗑",
            width=28,
            height=28,
            fg_color="#ef4444",
            hover_color="#dc2626",
            command=lambda: self.remove_callback(self)
        )
        self.btn_delete.grid(row=0, column=2, sticky="e", padx=10, pady=(6, 2))

        # Baris 1: Dropdown Kategori (Disesuaikan dengan Jenis awal)
        initial_categories = self.CATEGORIES_PEMASUKAN if self.get_jenis_callback() == "Pemasukan" else self.CATEGORIES_PENGELUARAN

        self.combo_kategori = ctk.CTkOptionMenu(
            self,
            values=initial_categories,
            width=130,
            fg_color="#0f172a",
            button_color="#334155",
            button_hover_color="#475569",
            text_color="#ffffff",
            dropdown_text_color="#ffffff",
            dropdown_fg_color="#1e293b"
        )
        self.combo_kategori.grid(row=1, column=0, padx=(10, 5), pady=4, sticky="w")
        self.combo_kategori.set(initial_categories[0])

        # Input Keterangan / Nama Barang
        self.entry_keterangan = ctk.CTkEntry(
            self,
            placeholder_text="Keterangan / Detail Item",
            placeholder_text_color="#64748b",
            fg_color="#0f172a",
            text_color="#ffffff",
            border_color="#334155",
            width=190
        )
        self.entry_keterangan.grid(row=1, column=1, padx=5, pady=4, sticky="ew")

        # Input Nominal / Harga
        self.entry_nominal = ctk.CTkEntry(
            self,
            placeholder_text="Nominal (Rp)",
            placeholder_text_color="#64748b",
            fg_color="#0f172a",
            text_color="#ffffff",
            border_color="#334155",
            width=120
        )
        self.entry_nominal.grid(row=1, column=2, padx=(5, 10), pady=4, sticky="e")
        self.entry_nominal.bind("<KeyRelease>", lambda e: self.update_total_callback())

        # Baris 2: Frame Upload Nota
        nota_frame = ctk.CTkFrame(self, fg_color="transparent")
        nota_frame.grid(row=2, column=0, columnspan=3, sticky="ew", padx=10, pady=(4, 8))

        self.btn_nota = ctk.CTkButton(
            nota_frame,
            text="📷 Upload Nota",
            width=110,
            height=26,
            font=("Arial", 11, "bold"),
            fg_color="#0284c7",
            hover_color="#0369a1",
            text_color="#ffffff",
            command=self.pilih_nota
        )
        self.btn_nota.pack(side="left", padx=(0, 8))

        self.lbl_nota_text = ctk.CTkLabel(
            nota_frame,
            text="Tanpa Nota (Opsional)",
            text_color="#94a3b8",
            font=("Arial", 10, "italic")
        )
        self.lbl_nota_text.pack(side="left")

        self.grid_columnconfigure(1, weight=1)

    def update_kategori_options(self, jenis):
        """Memperbarui opsi dropdown kategori berdasarkan jenis transaksi"""
        if jenis == "Pemasukan":
            options = self.CATEGORIES_PEMASUKAN
        else:
            options = self.CATEGORIES_PENGELUARAN

        self.combo_kategori.configure(values=options)
        self.combo_kategori.set(options[0])

    def pilih_nota(self):
        file = filedialog.askopenfilename(
            title="Pilih Nota Item",
            filetypes=[
                ("Gambar", "*.png *.jpg *.jpeg *.bmp"),
                ("PDF File", "*.pdf"),
                ("Semua File", "*.*")
            ]
        )
        if file:
            self.nota_path = file
            filename = os.path.basename(file)
            short_name = filename if len(filename) <= 20 else filename[:17] + "..."
            self.lbl_nota_text.configure(
                text=f"📄 {short_name}",
                text_color="#34d399"
            )

    def get_data(self):
        kategori = self.combo_kategori.get()
        keterangan = self.entry_keterangan.get().strip()
        nominal_raw = self.entry_nominal.get().strip().replace(".", "").replace(",", "")

        if not keterangan:
            return None, "Keterangan item tidak boleh kosong"

        try:
            nominal = float(nominal_raw)
            if nominal <= 0:
                return None, "Nominal harus lebih dari 0"
        except ValueError:
            return None, "Nominal harus berupa angka"

        # Proses salin nota jika diunggah
        saved_nota_path = ""
        if self.nota_path and os.path.exists(self.nota_path):
            os.makedirs("uploads/nota", exist_ok=True)
            ext = os.path.splitext(self.nota_path)[1]
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
            filename = f"nota_{self.project_id}_{timestamp}{ext}"
            saved_nota_path = os.path.join("uploads/nota", filename)
            shutil.copy(self.nota_path, saved_nota_path)

        return {
            "kategori": kategori,
            "keterangan": keterangan,
            "nominal": nominal,
            "nota": saved_nota_path
        }, None


class AddTransaction(ctk.CTkToplevel):

    def __init__(self, parent, project_id, callback):
        super().__init__(parent)

        self.project_id = project_id
        self.callback = callback
        self.item_rows = []

        self.title("Tambah Transaksi")
        self.geometry("580x680")
        self.resizable(False, False)
        
        # Modal Focus
        self.grab_set()

        self.build_ui()
        self.add_item_row()  # Otomatis menambahkan baris pertama

    def build_ui(self):
        # 1. Judul Header
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=15, pady=(15, 5))

        ctk.CTkLabel(
            header_frame,
            text="Tambah Transaksi Baru",
            font=("Arial", 20, "bold"),
            text_color="#32a127"
        ).pack(anchor="w")

        # 2. Section Tanggal & Jenis (Card Atas)
        info_card = ctk.CTkFrame(self, fg_color="#1e293b", corner_radius=10, border_width=1, border_color="#334155")
        info_card.pack(fill="x", padx=15, pady=10)

        # Tanggal (Kalender DateEntry)
        ctk.CTkLabel(info_card, text="Tanggal:", font=("Arial", 12, "bold"), text_color="#ffffff").grid(row=0, column=0, padx=12, pady=12, sticky="w")
        self.tanggal = DateEntry(
            info_card,
            width=12,
            background='#1e293b',
            foreground='white',
            bordercolor='#334155',
            headersbackground='#0f172a',
            date_pattern='yyyy-mm-dd'
        )
        self.tanggal.grid(row=0, column=1, padx=5, pady=12, sticky="w")

        # Jenis Transaksi
        ctk.CTkLabel(info_card, text="Jenis:", font=("Arial", 12, "bold"), text_color="#ffffff").grid(row=0, column=2, padx=(20, 5), pady=12, sticky="w")
        self.jenis_var = ctk.StringVar(value="Pengeluaran")

        rb_out = ctk.CTkRadioButton(
            info_card, text="Pengeluaran", variable=self.jenis_var, value="Pengeluaran",
            fg_color="#ef4444", hover_color="#dc2626", text_color="#ffffff",
            command=self.on_jenis_change
        )
        rb_out.grid(row=0, column=3, padx=5, pady=12)

        rb_in = ctk.CTkRadioButton(
            info_card, text="Pemasukan", variable=self.jenis_var, value="Pemasukan",
            fg_color="#10b981", hover_color="#059669", text_color="#ffffff",
            command=self.on_jenis_change
        )
        rb_in.grid(row=0, column=4, padx=5, pady=12)

        # 3. Dynamic Items Container (Scrollable Frame)
        ctk.CTkLabel(self, text="Daftar Item / Detail Barang:", font=("Arial", 12, "bold"), text_color="#94a3b8").pack(anchor="w", padx=15, pady=(5, 0))

        self.scroll_items = ctk.CTkScrollableFrame(self, fg_color="#0f172a", corner_radius=10, border_width=1, border_color="#1e293b")
        self.scroll_items.pack(fill="both", expand=True, padx=15, pady=5)

        # Tombol Tambah Baris
        self.btn_add_row = ctk.CTkButton(
            self,
            text="+ Tambah Item Barang",
            font=("Arial", 12, "bold"),
            fg_color="#2563eb",
            hover_color="#1d4ed8",
            text_color="#ffffff",
            command=self.add_item_row
        )
        self.btn_add_row.pack(anchor="w", padx=15, pady=5)

        # 4. Total Nominal (Card Bawah)
        bottom_card = ctk.CTkFrame(self, fg_color="#1e293b", corner_radius=10, border_width=1, border_color="#334155")
        bottom_card.pack(fill="x", padx=15, pady=10)

        ctk.CTkLabel(
            bottom_card,
            text="Ringkasan Total:",
            font=("Arial", 13, "bold"),
            text_color="#94a3b8"
        ).pack(side="left", padx=15, pady=12)

        self.lbl_total_sum = ctk.CTkLabel(
            bottom_card,
            text="Total: Rp 0",
            font=("Arial", 16, "bold"),
            text_color="#34d399"
        )
        self.lbl_total_sum.pack(side="right", padx=15, pady=12)

        # 5. Tombol Aksi (Simpan & Batal)
        action_frame = ctk.CTkFrame(self, fg_color="transparent")
        action_frame.pack(fill="x", padx=15, pady=(0, 15))

        ctk.CTkButton(
            action_frame,
            text="💾 Simpan Transaksi",
            fg_color="#10b981",
            hover_color="#059669",
            height=38,
            font=("Arial", 13, "bold"),
            text_color="#ffffff",
            command=self.save
        ).pack(side="right", padx=(5, 0))

        ctk.CTkButton(
            action_frame,
            text="Batal",
            fg_color="#475569",
            hover_color="#334155",
            height=38,
            font=("Arial", 12),
            text_color="#ffffff",
            command=self.destroy
        ).pack(side="right", padx=5)

    def on_jenis_change(self):
        """Memperbarui dropdown kategori di seluruh baris saat jenis transaksi diubah"""
        jenis = self.jenis_var.get()
        for row in self.item_rows:
            row.update_kategori_options(jenis)

    def add_item_row(self):
        index = len(self.item_rows) + 1
        row = DynamicItemRow(
            self.scroll_items,
            index,
            remove_callback=self.remove_item_row,
            update_total_callback=self.calculate_total,
            project_id=self.project_id,
            get_jenis_callback=self.jenis_var.get
        )
        self.item_rows.append(row)
        self.reindex_rows()
        self.calculate_total()

    def remove_item_row(self, row_obj):
        if len(self.item_rows) <= 1:
            messagebox.showwarning("Peringatan", "Minimal harus ada 1 item barang!")
            return

        row_obj.destroy()
        self.item_rows.remove(row_obj)
        self.reindex_rows()
        self.calculate_total()

    def reindex_rows(self):
        for idx, row in enumerate(self.item_rows, start=1):
            row.index = idx
            row.lbl_title.configure(text=f"Item #{idx}")

    def calculate_total(self):
        total = 0.0
        for row in self.item_rows:
            raw = row.entry_nominal.get().strip().replace(".", "").replace(",", "")
            try:
                if raw:
                    total += float(raw)
            except ValueError:
                pass

        self.lbl_total_sum.configure(text=f"Total: Rp {total:,.0f}")

    def save(self):
        tanggal = self.tanggal.get_date().strftime("%Y-%m-%d")
        jenis = self.jenis_var.get()

        # Validasi seluruh item row
        items_to_save = []
        for row in self.item_rows:
            data, err = row.get_data()
            if err:
                messagebox.showerror("Validasi Gagal", f"Error pada Item #{row.index}:\n{err}")
                return
            items_to_save.append(data)

        # Simpan seluruh item ke database
        try:
            for item in items_to_save:
                add_transaction(
                    self.project_id,
                    tanggal,
                    item["kategori"],
                    item["keterangan"],
                    jenis,
                    item["nominal"],
                    item["nota"]
                )

            messagebox.showinfo("Berhasil", f"Berhasil menyimpan {len(items_to_save)} transaksi!")
            self.callback()
            self.destroy()

        except Exception as e:
            messagebox.showerror("Error Database", f"Gagal menyimpan transaksi:\n{e}")