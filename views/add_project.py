import customtkinter as ctk
from tkinter import messagebox

from query import add_project


class AddProject(ctk.CTkToplevel):

    def __init__(self, parent, user_id, callback):
        super().__init__(parent)

        self.user_id = user_id
        self.callback = callback

        self.title("Tambah Proyek")
        self.geometry("400x350")
        self.resizable(False, False)
        self.grab_set()

        self.build_ui()

    # ======================
    # UI
    # ======================
    def build_ui(self):
        title = ctk.CTkLabel(
            self,
            text="Tambah Proyek Baru",
            font=("Arial", 24, "bold")
        )
        title.pack(pady=25)

        self.nama_proyek = ctk.CTkEntry(
            self,
            width=300,
            height=40,
            placeholder_text="Nama Proyek (Wajib)"
        )
        self.nama_proyek.pack(pady=10)

        self.nama_client = ctk.CTkEntry(
            self,
            width=300,
            height=40,
            placeholder_text="Nama Client (Opsional)"
        )
        self.nama_client.pack(pady=10)

        btn = ctk.CTkButton(
            self,
            text="Simpan",
            width=200,
            height=40,
            command=self.save
        )
        btn.pack(pady=30)

    # ======================
    # SIMPAN
    # ======================
    def save(self):
        nama_proyek = self.nama_proyek.get().strip()
        nama_client = self.nama_client.get().strip()

        if not nama_proyek:
            messagebox.showwarning(
                "Data Kosong",
                "Nama proyek harus diisi!"
            )
            return

        # Nama client opsional (jika kosong diisi "-")
        if not nama_client:
            nama_client = "-"

        try:
            kode = add_project(
                self.user_id,
                nama_proyek,
                nama_client
            )

            messagebox.showinfo(
                "Berhasil",
                f"Proyek berhasil dibuat\nKode : {kode}"
            )

            if self.callback:
                self.callback()

            self.destroy()

        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Gagal menambah proyek: {str(e)}"
            )