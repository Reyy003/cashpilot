import customtkinter as ctk
from tkinter import messagebox

from query import update_project


class EditProject(ctk.CTkToplevel):

    def __init__(self, parent, project, callback):
        super().__init__(parent)

        self.project = project
        self.callback = callback

        self.title("Edit Project")
        self.geometry("400x320")
        self.resizable(False, False)

        # Background Adaptif Modal
        self.configure(fg_color=("#f8fafc", "#0f172a"))

        self.grab_set()
        self.focus()

        self.build_ui()

    def build_ui(self):
        card = ctk.CTkFrame(
            self,
            fg_color=("#ffffff", "#181825"),
            corner_radius=18,
            border_width=1,
            border_color=("#e2e8f0", "#27273a")
        )
        card.pack(fill="both", expand=True, padx=15, pady=15)

        ctk.CTkLabel(
            card,
            text="Edit Project",
            font=("Arial", 22, "bold"),
            text_color=("#0f172a", "#ffffff")
        ).pack(pady=(15, 10))

        self.nama_project = ctk.CTkEntry(
            card,
            width=300,
            height=40,
            corner_radius=10,
            placeholder_text="Nama Project"
        )
        self.nama_project.pack(pady=8)
        self.nama_project.insert(0, self.project["nama_proyek"])

        self.nama_client = ctk.CTkEntry(
            card,
            width=300,
            height=40,
            corner_radius=10,
            placeholder_text="Nama Client"
        )
        self.nama_client.pack(pady=8)
        self.nama_client.insert(0, self.project["nama_client"] or "")

        btn = ctk.CTkButton(
            card,
            text="Simpan Perubahan",
            font=("Arial", 13, "bold"),
            width=300,
            height=40,
            corner_radius=10,
            fg_color="#7c3aed",
            hover_color="#6d28d9",
            command=self.save
        )
        btn.pack(pady=(15, 10))

    def save(self):
        update_project(
            self.project["id"],
            self.nama_project.get(),
            self.nama_client.get()
        )

        messagebox.showinfo(
            "Berhasil",
            "Project berhasil diperbarui"
        )

        self.callback()
        self.destroy()