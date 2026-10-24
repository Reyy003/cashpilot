import os
import sys
import shutil
from datetime import datetime
from PIL import Image, ImageDraw, ImageOps
from tkinter import filedialog
import customtkinter as ctk
import bcrypt

# Import query register & notifikasi
from query import register_user
from views.notification import Notification


def make_circular_image(image_path_or_pil, size):
    """Fungsi helper untuk membuat gambar berbentuk lingkaran sempurna"""
    if isinstance(image_path_or_pil, str):
        img = Image.open(image_path_or_pil).convert("RGBA")
    else:
        img = image_path_or_pil.convert("RGBA")

    # Fit image ke ukuran persegi tanpa merusak rasio
    img = ImageOps.fit(img, size, Image.Resampling.LANCZOS)

    # Buat mask lingkaran
    mask = Image.new("L", size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, size[0], size[1]), fill=255)

    # Terapkan mask ke gambar transparan
    output = Image.new("RGBA", size, (0, 0, 0, 0))
    output.paste(img, (0, 0), mask=mask)
    return output


class RegisterPage(ctk.CTk):

    def __init__(self):
        super().__init__()

        # ==========================
        # WINDOW CONFIGURATION
        # ==========================
        self.title("CashPilot - Buat Akun Baru")
        self.geometry("460x650")
        self.resizable(False, False)
        ctk.set_appearance_mode("light")

        self.configure(fg_color="#f8fafc")
        self.bind("<Return>", lambda event: self.register())

        self.profile_pic_path = ""
        self.show_password = False
        self.show_confirm_password = False

        self.build_ui()

    def build_ui(self):
        # Card Main Container
        self.card = ctk.CTkFrame(
            self,
            width=390,
            height=590,
            corner_radius=20,
            fg_color="white",
            border_width=1,
            border_color="#e2e8f0"
        )
        self.card.place(relx=0.5, rely=0.5, anchor="center")

        # Header Title
        ctk.CTkLabel(
            self.card,
            text="DAFTAR AKUN",
            font=("Arial", 24, "bold"),
            text_color="#2563eb"
        ).pack(pady=(25, 2))

        ctk.CTkLabel(
            self.card,
            text="Lengkapi data untuk membuat akun CashPilot",
            font=("Arial", 12),
            text_color="#64748b"
        ).pack(pady=(0, 15))

        # ==========================
        # UPLOAD FOTO PROFIL (OPSIONAL)
        # ==========================
        profile_frame = ctk.CTkFrame(self.card, fg_color="transparent")
        profile_frame.pack(pady=(0, 15))

        self.avatar_label = ctk.CTkLabel(
            profile_frame,
            text="👤",
            font=("Arial", 32),
            width=65,
            height=65,
            corner_radius=35,
            fg_color="#f1f5f9",
            text_color="#94a3b8"
        )
        self.avatar_label.pack(side="left", padx=(0, 10))

        btn_upload = ctk.CTkButton(
            profile_frame,
            text="📷 Pilih Foto Profil",
            font=("Arial", 11, "bold"),
            fg_color="#3b82f6",
            hover_color="#2563eb",
            height=32,
            corner_radius=8,
            command=self.choose_profile_pic
        )
        btn_upload.pack(side="left")

        # ==========================
        # INPUT FIELDS
        # ==========================
        # 1. Nama Lengkap
        self.nama_lengkap = ctk.CTkEntry(
            self.card,
            width=300,
            height=40,
            corner_radius=10,
            placeholder_text="Nama Lengkap"
        )
        self.nama_lengkap.pack(pady=6)

        # 2. Username
        self.username = ctk.CTkEntry(
            self.card,
            width=300,
            height=40,
            corner_radius=10,
            placeholder_text="Username"
        )
        self.username.pack(pady=6)

        # 3. Password Box + Eye Button
        pass_container = ctk.CTkFrame(self.card, width=300, height=40, fg_color="transparent")
        pass_container.pack(pady=6)
        pass_container.pack_propagate(False)

        self.password = ctk.CTkEntry(
            pass_container,
            width=300,
            height=40,
            corner_radius=10,
            placeholder_text="Password (Min. 8 Karakter)",
            show="*"
        )
        self.password.pack(fill="both")

        self.eye_pass = ctk.CTkButton(
            pass_container,
            text="👁",
            width=35,
            height=30,
            corner_radius=8,
            fg_color="transparent",
            hover_color="#e2e8f0",
            text_color="#64748b",
            command=self.toggle_password
        )
        self.eye_pass.place(relx=0.9, rely=0.5, anchor="center")

        # 4. Confirm Password Box + Eye Button
        conf_pass_container = ctk.CTkFrame(self.card, width=300, height=40, fg_color="transparent")
        conf_pass_container.pack(pady=6)
        conf_pass_container.pack_propagate(False)

        self.confirm_password = ctk.CTkEntry(
            conf_pass_container,
            width=300,
            height=40,
            corner_radius=10,
            placeholder_text="Konfirmasi Password",
            show="*"
        )
        self.confirm_password.pack(fill="both")

        self.eye_conf = ctk.CTkButton(
            conf_pass_container,
            text="👁",
            width=35,
            height=30,
            corner_radius=8,
            fg_color="transparent",
            hover_color="#e2e8f0",
            text_color="#64748b",
            command=self.toggle_confirm_password
        )
        self.eye_conf.place(relx=0.9, rely=0.5, anchor="center")

        # ==========================
        # REGISTER BUTTON
        # ==========================
        self.btn_register = ctk.CTkButton(
            self.card,
            width=300,
            height=42,
            corner_radius=10,
            text="Daftar Sekarang",
            font=("Arial", 14, "bold"),
            fg_color="#10b981",
            hover_color="#059669",
            command=self.register
        )
        self.btn_register.pack(pady=(20, 10))

        # ==========================
        # LINK KE LOGIN
        # ==========================
        login_link_frame = ctk.CTkFrame(self.card, fg_color="transparent")
        login_link_frame.pack(pady=(5, 10))

        ctk.CTkLabel(
            login_link_frame,
            text="Sudah memiliki akun? ",
            font=("Arial", 12),
            text_color="#64748b"
        ).pack(side="left")

        btn_go_login = ctk.CTkButton(
            login_link_frame,
            text="Login disini",
            font=("Arial", 12, "bold"),
            text_color="#2563eb",
            fg_color="transparent",
            hover_color="#f1f5f9",
            width=70,
            command=self.open_login
        )
        btn_go_login.pack(side="left")

    # =================================
    # TOGGLE SHOW / HIDE PASSWORDS
    # =================================
    def toggle_password(self):
        if self.show_password:
            self.password.configure(show="*")
            self.eye_pass.configure(text="👁")
            self.show_password = False
        else:
            self.password.configure(show="")
            self.eye_pass.configure(text="🙈")
            self.show_password = True

    def toggle_confirm_password(self):
        if self.show_confirm_password:
            self.confirm_password.configure(show="*")
            self.eye_conf.configure(text="👁")
            self.show_confirm_password = False
        else:
            self.confirm_password.configure(show="")
            self.eye_conf.configure(text="🙈")
            self.show_confirm_password = True

    # =================================
    # CHOOSE PROFILE PIC
    # =================================
    def choose_profile_pic(self):
        file_path = filedialog.askopenfilename(
            title="Pilih Foto Profil",
            filetypes=[("Gambar", "*.png *.jpg *.jpeg *.bmp")]
        )
        if file_path:
            self.profile_pic_path = file_path
            try:
                # Membuat foto yang di-upload menjadi lingkaran sempurna
                circular_img = make_circular_image(file_path, (65, 65))
                ctk_img = ctk.CTkImage(light_image=circular_img, dark_image=circular_img, size=(65, 65))
                self.avatar_label.configure(image=ctk_img, text="", fg_color="transparent")
            except Exception as e:
                print("Error cropping image:", e)

    # =================================
    # REGISTER PROCESS
    # =================================
    def register(self):
        nama = self.nama_lengkap.get().strip()
        username = self.username.get().strip()
        password = self.password.get()
        confirm_pass = self.confirm_password.get()

        # Validasi Kelengkapan Data
        if not nama or not username or not password or not confirm_pass:
            Notification(self, "failed", "Mohon isi semua bidang formulir")
            return

        # Validasi Panjang Password (Min. 8 Karakter)
        if len(password) < 8:
            Notification(self, "failed", "Password minimal harus 8 karakter")
            return

        # Validasi Konfirmasi Password
        if password != confirm_pass:
            Notification(self, "failed", "Konfirmasi password tidak cocok")
            return

        # Proses Foto Profil jika di-upload
        saved_pic_path = ""
        if self.profile_pic_path and os.path.exists(self.profile_pic_path):
            os.makedirs("uploads/profiles", exist_ok=True)
            ext = os.path.splitext(self.profile_pic_path)[1]
            filename = f"profile_{username}_{datetime.now().strftime('%Y%m%d_%H%M%S')}{ext}"
            saved_pic_path = os.path.join("uploads/profiles", filename)
            shutil.copy(self.profile_pic_path, saved_pic_path)

        # Simpan ke Database melalui query.py
        try:
            # Hash password sebelum dikirim untuk disimpan ke database
            password_hash = bcrypt.hashpw(
                password.encode("utf-8"),
                bcrypt.gensalt()
            ).decode("utf-8")

            success, msg = register_user(
                username,
                password_hash,
                nama,
                saved_pic_path
            )
            if success:
                Notification(self, "success", "Registrasi berhasil! Silahkan login.")
                self.after(1500, self.open_login)
            else:
                Notification(self, "failed", msg or "Username sudah terdaftar")
        except Exception as e:
            Notification(self, "failed", f"Terjadi kesalahan: {e}")

    # =================================
    # REDIRECT TO LOGIN
    # =================================
    def open_login(self):
        self.destroy()
        from views.login import LoginPage
        login_app = LoginPage()
        login_app.mainloop()