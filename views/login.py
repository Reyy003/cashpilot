import customtkinter as ctk
import os
from PIL import Image

from query import check_login
from views.notification import Notification
from views.dashboard import Dashboard


class LoginPage(ctk.CTk):

    def __init__(self):
        super().__init__()

        # ==========================
        # WINDOW
        # ==========================
        self.title("CashPilot - Login")
        self.geometry("450x570")
        self.resizable(False, False)
        ctk.set_appearance_mode("light")

        # Pasang Ikon Window Aplikasi (.ico)
        try:
            self.iconbitmap("cashpilot_logo.ico")
        except Exception:
            pass

        self.bind("<Return>", lambda event: self.login())

        # ==========================
        # BACKGROUND & CARD LOGIN
        # ==========================
        self.configure(fg_color="#f8fafc")

        self.card = ctk.CTkFrame(
            self,
            width=360,
            height=500,
            corner_radius=20,
            fg_color="white",
            border_width=1,
            border_color="#e2e8f0"
        )
        self.card.place(relx=0.5, rely=0.5, anchor="center")

        # ==========================
        # LOGO & HEADER
        # ==========================
        try:
            img_login_raw = Image.open("cashpilot_logo.png").resize((48, 48), Image.Resampling.LANCZOS)
            self.login_logo_img = ctk.CTkImage(light_image=img_login_raw, dark_image=img_login_raw, size=(48, 48))
            self.logo_label = ctk.CTkLabel(self.card, image=self.login_logo_img, text="")
            self.logo_label.pack(pady=(25, 5))
        except Exception:
            pass

        self.title_label = ctk.CTkLabel(
            self.card,
            text="CASHPILOT",
            font=("Arial", 30, "bold"),
            text_color="#2563eb"
        )
        self.title_label.pack(pady=(0, 2))

        self.subtitle = ctk.CTkLabel(
            self.card,
            text="Project & Finance Management",
            font=("Arial", 12),
            text_color="#64748b"
        )
        self.subtitle.pack(pady=(0, 20))

        # ==========================
        # USERNAME
        # ==========================
        self.username = ctk.CTkEntry(
            self.card,
            width=280,
            height=42,
            corner_radius=10,
            placeholder_text="Username"
        )
        self.username.pack(pady=8)

        # ==========================
        # PASSWORD AREA
        # ==========================
        self.password_container = ctk.CTkFrame(
            self.card,
            width=280,
            height=42,
            fg_color="transparent"
        )
        self.password_container.pack(pady=8)
        self.password_container.pack_propagate(False)

        self.password = ctk.CTkEntry(
            self.password_container,
            width=280,
            height=42,
            corner_radius=10,
            placeholder_text="Password",
            show="*"
        )
        self.password.pack(fill="both")

        self.show_password = False

        self.eye_button = ctk.CTkButton(
            self.password_container,
            text="👁",
            width=35,
            height=30,
            corner_radius=8,
            fg_color="transparent",
            hover_color="#e2e8f0",
            text_color="#64748b",
            command=self.toggle_password
        )
        self.eye_button.place(relx=0.89, rely=0.5, anchor="center")

        # ==========================
        # LOGIN BUTTON
        # ==========================
        self.btn_login = ctk.CTkButton(
            self.card,
            width=280,
            height=42,
            corner_radius=10,
            text="Login",
            font=("Arial", 14, "bold"),
            fg_color="#2563eb",
            hover_color="#1d4ed8",
            command=self.login
        )
        self.btn_login.pack(pady=(18, 12))

        # ==========================
        # REGISTER LINK
        # ==========================
        register_link_frame = ctk.CTkFrame(self.card, fg_color="transparent")
        register_link_frame.pack(pady=(0, 15))

        ctk.CTkLabel(
            register_link_frame,
            text="Belum memiliki akun? ",
            font=("Arial", 11),
            text_color="#64748b"
        ).pack(side="left")

        self.btn_go_register = ctk.CTkButton(
            register_link_frame,
            text="Klik disini untuk membuat",
            font=("Arial", 11, "bold"),
            text_color="#2563eb",
            fg_color="transparent",
            hover_color="#f1f5f9",
            width=100,
            command=self.open_register
        )
        self.btn_go_register.pack(side="left")

    # =================================
    # SHOW / HIDE PASSWORD
    # =================================
    def toggle_password(self):
        if self.show_password:
            self.password.configure(show="*")
            self.eye_button.configure(text="👁")
            self.show_password = False
        else:
            self.password.configure(show="")
            self.eye_button.configure(text="🙈")
            self.show_password = True

    # =================================
    # LOGIN PROCESS
    # =================================
    def login(self):
        username = self.username.get().strip()
        password = self.password.get()

        user = check_login(username, password)

        if user:
            Notification(self, "success", f"Selamat datang {user['nama']}")
            self.after(1400, lambda: self.open_dashboard(user["id"]))
        else:
            Notification(self, "failed", "Username atau password salah")

    # =================================
    # OPEN REGISTER PAGE
    # =================================
    def open_register(self):
        self.destroy()
        from views.register import RegisterPage
        register_app = RegisterPage()
        register_app.mainloop()

    # =================================
    # OPEN DASHBOARD
    # =================================
    def open_dashboard(self, user_id):
        self.destroy()
        dashboard = Dashboard(user_id)
        dashboard.mainloop()