import os
import shutil
from PIL import Image, ImageDraw, ImageOps
from tkinter import filedialog, messagebox
import customtkinter as ctk

from query import (
    get_user_profile,
    update_profile,
    check_login
)


def make_circular_image(image_path_or_pil, size=(120, 120)):
    """Fungsi helper untuk membuat gambar berbentuk lingkaran sempurna"""
    if isinstance(image_path_or_pil, str):
        img = Image.open(image_path_or_pil).convert("RGBA")
    else:
        img = image_path_or_pil.convert("RGBA")

    img = ImageOps.fit(img, size, Image.Resampling.LANCZOS)

    mask = Image.new("L", size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, size[0], size[1]), fill=255)

    output = Image.new("RGBA", size, (0, 0, 0, 0))
    output.paste(img, (0, 0), mask=mask)
    return output


class ProfilePage:

    def __init__(self, parent, user_id):
        self.parent = parent
        self.user_id = user_id
        self.photo_path = None

        self.show_old_pass = False
        self.show_new_pass = False
        self.show_conf_pass = False

        self.frame = ctk.CTkFrame(parent, fg_color="transparent")
        self.frame.pack(fill="both", expand=True, padx=20, pady=20)

        self.build()

    def build(self):
        data = get_user_profile(self.user_id)

        # Card Main Container dengan Dukungan Dark Mode
        self.card = ctk.CTkScrollableFrame(
            self.frame,
            fg_color=("#ffffff", "#0f172a"),
            corner_radius=18,
            border_width=1,
            border_color=("#e2e8f0", "#1e293b")
        )
        self.card.pack(fill="both", expand=True, padx=10, pady=10)

        # Title
        ctk.CTkLabel(
            self.card,
            text="Pengaturan Profil & Keamanan",
            font=("Arial", 24, "bold"),
            text_color=("#0f172a", "#ffffff")
        ).pack(pady=(20, 15))

        # Foto Profil Label
        self.photo_label = ctk.CTkLabel(
            self.card,
            text="👤",
            font=("Arial", 50),
            width=120,
            height=120,
            corner_radius=60,
            fg_color=("#f1f5f9", "#1e293b"),
            text_color=("#94a3b8", "#64748b")
        )
        self.photo_label.pack(pady=(5, 10))

        if data and data.get("foto"):
            foto_path = data["foto"]
            if not os.path.exists(foto_path):
                foto_path = os.path.join("assets", "profile", data["foto"])
            
            if os.path.exists(foto_path):
                self.load_image(foto_path)

        btn_photo = ctk.CTkButton(
            self.card,
            text="📷 Ganti Foto Profil",
            font=("Arial", 12, "bold"),
            fg_color="#7c3aed",
            hover_color="#6d28d9",
            height=34,
            corner_radius=8,
            command=self.choose_photo
        )
        btn_photo.pack(pady=(0, 20))

        # Input Nama & Username
        ctk.CTkLabel(self.card, text="Informasi Pengguna", font=("Arial", 14, "bold"), text_color=("#334155", "#cbd5e1")).pack(anchor="w", padx=35, pady=(5, 5))

        self.nama = ctk.CTkEntry(
            self.card,
            width=360,
            height=42,
            corner_radius=10,
            placeholder_text="Nama Lengkap"
        )
        self.nama.insert(0, data["nama"] if data else "")
        self.nama.pack(pady=6)

        self.username = ctk.CTkEntry(
            self.card,
            width=360,
            height=42,
            corner_radius=10,
            placeholder_text="Username"
        )
        self.username.insert(0, data["username"] if data else "")
        self.username.pack(pady=6)

        # Divider
        ctk.CTkFrame(self.card, width=360, height=1, fg_color=("#e2e8f0", "#1e293b")).pack(pady=15)

        # Keamanan Password
        ctk.CTkLabel(self.card, text="Ubah Password (Opsional)", font=("Arial", 14, "bold"), text_color=("#334155", "#cbd5e1")).pack(anchor="w", padx=35, pady=(0, 5))
        ctk.CTkLabel(self.card, text="Kosongkan bagian ini jika tidak ingin mengubah password", font=("Arial", 11), text_color=("#64748b", "#94a3b8")).pack(anchor="w", padx=35, pady=(0, 10))

        # 1. Password Lama
        old_pass_container = ctk.CTkFrame(self.card, width=360, height=42, fg_color="transparent")
        old_pass_container.pack(pady=6)
        old_pass_container.pack_propagate(False)

        self.old_password = ctk.CTkEntry(
            old_pass_container,
            width=360,
            height=42,
            corner_radius=10,
            placeholder_text="Password Saat Ini",
            show="*"
        )
        self.old_password.pack(fill="both")

        # Menggunakan CTkLabel agar 100% tanpa background/hover box
        self.lbl_eye_old = ctk.CTkLabel(
            old_pass_container, text="👁", font=("Arial", 14),
            text_color=("#64748b", "#94a3b8"), cursor="hand2"
        )
        self.lbl_eye_old.place(relx=0.91, rely=0.5, anchor="center")
        self.lbl_eye_old.bind("<Button-1>", lambda e: self.toggle_pass("old"))

        # 2. Password Baru
        new_pass_container = ctk.CTkFrame(self.card, width=360, height=42, fg_color="transparent")
        new_pass_container.pack(pady=6)
        new_pass_container.pack_propagate(False)

        self.new_password = ctk.CTkEntry(
            new_pass_container,
            width=360,
            height=42,
            corner_radius=10,
            placeholder_text="Password Baru (Min. 8 Karakter)",
            show="*"
        )
        self.new_password.pack(fill="both")

        self.lbl_eye_new = ctk.CTkLabel(
            new_pass_container, text="👁", font=("Arial", 14),
            text_color=("#64748b", "#94a3b8"), cursor="hand2"
        )
        self.lbl_eye_new.place(relx=0.91, rely=0.5, anchor="center")
        self.lbl_eye_new.bind("<Button-1>", lambda e: self.toggle_pass("new"))

        # 3. Konfirmasi Password Baru
        conf_pass_container = ctk.CTkFrame(self.card, width=360, height=42, fg_color="transparent")
        conf_pass_container.pack(pady=6)
        conf_pass_container.pack_propagate(False)

        self.conf_password = ctk.CTkEntry(
            conf_pass_container,
            width=360,
            height=42,
            corner_radius=10,
            placeholder_text="Konfirmasi Password Baru",
            show="*"
        )
        self.conf_password.pack(fill="both")

        self.lbl_eye_conf = ctk.CTkLabel(
            conf_pass_container, text="👁", font=("Arial", 14),
            text_color=("#64748b", "#94a3b8"), cursor="hand2"
        )
        self.lbl_eye_conf.place(relx=0.91, rely=0.5, anchor="center")
        self.lbl_eye_conf.bind("<Button-1>", lambda e: self.toggle_pass("conf"))

        # Simpan Button
        save_btn = ctk.CTkButton(
            self.card,
            text="💾 Simpan Perubahan",
            font=("Arial", 14, "bold"),
            width=360,
            height=44,
            corner_radius=10,
            fg_color="#10b981",
            hover_color="#059669",
            command=self.save
        )
        save_btn.pack(pady=(25, 20))

    def toggle_pass(self, target):
        if target == "old":
            self.show_old_pass = not self.show_old_pass
            self.old_password.configure(show="" if self.show_old_pass else "*")
            self.lbl_eye_old.configure(text="🙈" if self.show_old_pass else "👁")
        elif target == "new":
            self.show_new_pass = not self.show_new_pass
            self.new_password.configure(show="" if self.show_new_pass else "*")
            self.lbl_eye_new.configure(text="🙈" if self.show_new_pass else "👁")
        elif target == "conf":
            self.show_conf_pass = not self.show_conf_pass
            self.conf_password.configure(show="" if self.show_conf_pass else "*")
            self.lbl_eye_conf.configure(text="🙈" if self.show_conf_pass else "👁")

    def choose_photo(self):
        file = filedialog.askopenfilename(
            title="Pilih Foto Profil Baru",
            filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp")]
        )
        if file:
            self.photo_path = file
            self.load_image(file)

    def load_image(self, path):
        try:
            circular_img = make_circular_image(path, (120, 120))
            self.img = ctk.CTkImage(
                light_image=circular_img,
                dark_image=circular_img,
                size=(120, 120)
            )
            self.photo_label.configure(image=self.img, text="", fg_color="transparent")
        except Exception as e:
            print("Gagal memuat gambar profil:", e)

    def save(self):
        nama = self.nama.get().strip()
        username = self.username.get().strip()
        old_pass = self.old_password.get()
        new_pass = self.new_password.get()
        conf_pass = self.conf_password.get()

        if not nama or not username:
            messagebox.showwarning("Peringatan", "Nama dan Username tidak boleh kosong!")
            return

        user = get_user_profile(self.user_id)
        if not user:
            messagebox.showerror("Error", "Data user tidak ditemukan!")
            return

        foto_filename = user["foto"]
        final_password_to_save = ""

        if old_pass or new_pass or conf_pass:
            if not old_pass or not new_pass or not conf_pass:
                messagebox.showwarning("Keamanan Profil", "Lengkapi Password Saat Ini, Password Baru, dan Konfirmasi Password!")
                return

            if not check_login(user["username"], old_pass):
                messagebox.showerror("Validasi Gagal", "Password saat ini tidak cocok/salah!")
                return

            if len(new_pass) < 8:
                messagebox.showwarning("Keamanan Profil", "Password baru minimal harus 8 karakter!")
                return

            if new_pass != conf_pass:
                messagebox.showwarning("Keamanan Profil", "Konfirmasi password baru tidak cocok!")
                return

            final_password_to_save = new_pass

        if self.photo_path and os.path.exists(self.photo_path):
            folder = "uploads/profiles"
            os.makedirs(folder, exist_ok=True)
            
            filename = f"profile_{self.user_id}_{os.urandom(3).hex()}.png"
            save_path = os.path.join(folder, filename)

            circular_img = make_circular_image(self.photo_path, (200, 200))
            circular_img.save(save_path, format="PNG")
            foto_filename = save_path

        try:
            update_profile(
                self.user_id,
                nama,
                username,
                final_password_to_save,
                foto_filename
            )

            messagebox.showinfo("Berhasil", "Profil berhasil diperbarui!")

            self.old_password.delete(0, "end")
            self.new_password.delete(0, "end")
            self.conf_password.delete(0, "end")

            main_window = self.frame.winfo_toplevel()
            if hasattr(main_window, "build_sidebar"):
                main_window.build_sidebar()

        except Exception as e:
            messagebox.showerror("Error", f"Gagal memperbarui profil: {e}")