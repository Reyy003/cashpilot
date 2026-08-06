import customtkinter as ctk
from tkinter import messagebox

from query import (
    get_projects,
    delete_project
)

from views.edit_project import EditProject
from views.add_project import AddProject


class ProjectPage(ctk.CTkFrame):

    def __init__(self, parent, user_id):
        super().__init__(parent, fg_color="transparent")

        self.user_id = user_id
        self.search_text = ""

        self.pack(
            fill="both",
            expand=True
        )

        self.build_ui()
        self.load_projects()

    def build_ui(self):
        header = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        header.pack(
            fill="x",
            padx=25,
            pady=(20, 10)
        )

        title = ctk.CTkLabel(
            header,
            text="Daftar Proyek",
            font=("Arial", 30, "bold"),
            text_color=("#0f172a", "#ffffff")
        )
        title.pack(side="left")

        # SEARCH BAR
        self.search_entry = ctk.CTkEntry(
            header,
            width=300,
            height=40,
            corner_radius=10,
            placeholder_text="Cari proyek / client..."
        )
        self.search_entry.pack(
            side="right",
            padx=10
        )
        self.search_entry.bind(
            "<KeyRelease>",
            self.search_project
        )

        # REFRESH
        btn_refresh = ctk.CTkButton(
            header,
            text="↻",
            width=45,
            height=40,
            corner_radius=10,
            fg_color="#10b981",
            hover_color="#059669",
            command=self.refresh_projects
        )
        btn_refresh.pack(
            side="right",
            padx=5
        )

        # TAMBAH
        btn_add = ctk.CTkButton(
            header,
            text="+ Tambah Proyek",
            width=160,
            height=40,
            corner_radius=10,
            font=("Arial", 14, "bold"),
            fg_color="#7c3aed",
            hover_color="#6d28d9",
            command=self.open_add_project
        )
        btn_add.pack(
            side="right",
            padx=5
        )

        # CONTAINER DENGAN DUKUNGAN DARK MODE
        self.container = ctk.CTkScrollableFrame(
            self,
            fg_color=("#ffffff", "#0f172a"),
            corner_radius=15,
            border_width=1,
            border_color=("#e2e8f0", "#1e293b")
        )
        self.container.pack(
            padx=20,
            pady=20,
            fill="both",
            expand=True
        )

    def load_projects(self):
        for widget in self.container.winfo_children():
            widget.destroy()

        projects = get_projects(self.user_id)

        if self.search_text:
            projects = [
                project
                for project in projects
                if self.search_text in project["nama_proyek"].lower()
                or self.search_text in (project["nama_client"] or "").lower()
                or self.search_text in project["kode_proyek"].lower()
            ]

        if not projects:
            label = ctk.CTkLabel(
                self.container,
                text="Belum ada data proyek",
                font=("Arial", 16),
                text_color=("#64748b", "#94a3b8")
            )
            label.pack(pady=30)
            return

        for project in projects:
            self.create_project_card(project)

    def search_project(self, event=None):
        self.search_text = (
            self.search_entry.get()
            .lower()
            .strip()
        )
        self.load_projects()

    def create_project_card(self, project):
        card = ctk.CTkFrame(
            self.container,
            corner_radius=15,
            fg_color=("#f8fafc", "#181825"),
            border_width=1,
            border_color=("#e2e8f0", "#27273a")
        )
        card.pack(
            pady=10,
            padx=20,
            fill="x"
        )

        info = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )
        info.pack(
            side="left",
            padx=20,
            pady=15
        )

        nama = ctk.CTkLabel(
            info,
            text=project["nama_proyek"],
            font=("Arial", 20, "bold"),
            text_color=("#0f172a", "#ffffff")
        )
        nama.pack(anchor="w")

        client_display = project['nama_client'] if project['nama_client'] else "-"
        detail = ctk.CTkLabel(
            info,
            text=f"Kode  : {project['kode_proyek']}\nClient : {client_display}",
            font=("Arial", 14),
            text_color=("#64748b", "#94a3b8")
        )
        detail.pack(
            anchor="w",
            pady=5
        )

        button_frame = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )
        button_frame.pack(
            side="right",
            padx=15
        )

        btn_edit = ctk.CTkButton(
            button_frame,
            text="Edit",
            width=80,
            height=35,
            corner_radius=8,
            fg_color="#f59e0b",
            hover_color="#d97706",
            command=lambda p=project: self.edit_project(p)
        )
        btn_edit.pack(
            side="left",
            padx=5
        )

        btn_delete = ctk.CTkButton(
            button_frame,
            text="Hapus",
            width=80,
            height=35,
            corner_radius=8,
            fg_color="#dc2626",
            hover_color="#b91c1c",
            command=lambda id=project["id"]: self.remove_project(id)
        )
        btn_delete.pack(
            side="left",
            padx=5
        )

        btn_open = ctk.CTkButton(
            button_frame,
            text="Buka →",
            width=90,
            height=35,
            corner_radius=8,
            fg_color="#0f766e",
            hover_color="#115e59",
            command=lambda id=project["id"]: self.open_project(id)
        )
        btn_open.pack(
            side="left",
            padx=5
        )

    def open_add_project(self):
        AddProject(
            self,
            self.user_id,
            self.load_projects
        )

    def edit_project(self, project):
        EditProject(
            self,
            project,
            self.load_projects
        )

    def remove_project(self, project_id):
        confirm = messagebox.askyesno(
            "Hapus Project",
            "Yakin ingin menghapus project ini?"
        )
        if confirm:
            delete_project(project_id)
            self.load_projects()

    def refresh_projects(self):
        self.search_entry.delete(0, "end")
        self.search_text = ""
        self.load_projects()

    def open_project(self, project_id):
        self.destroy()
        from views.transaction import TransactionPage
        TransactionPage(
            self.master,
            project_id
        )