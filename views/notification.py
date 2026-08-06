import customtkinter as ctk


class Notification(ctk.CTkToplevel):

    def __init__(self, parent, status, message):
        super().__init__(parent)

        self.status = status
        
        # Hilangkan title bar bawaan OS untuk efek toast modern
        self.overrideredirect(True)
        self.attributes("-topmost", True)

        # Ukuran & Posisi di Tengah Parent Window
        width, height = 340, 180
        self.geometry(f"{width}x{height}")
        self.resizable(False, False)

        # Posisikan otomatis tepat di tengah-tengah jendela parent
        self.center_to_parent(parent, width, height)

        # Skema Warna Modern (Emerald Success & Coral Failed)
        if status == "success":
            accent_color = "#10b981"      # Emerald Green
            badge_bg = "#dcfce7"          # Light Green
            text_color = "#065f46"
            icon = "✓"
            default_title = "Berhasil!"
        else:
            accent_color = "#ef4444"      # Coral Red
            badge_bg = "#fee2e2"          # Light Red
            text_color = "#991b1b"
            icon = "✕"
            default_title = "Gagal!"

        # Main Outer Card Container
        self.card = ctk.CTkFrame(
            self,
            fg_color="#ffffff",
            corner_radius=20,
            border_width=2,
            border_color=accent_color
        )
        self.card.pack(fill="both", expand=True)

        # 1. Badge Icon Lingkaran Modern
        self.icon_badge = ctk.CTkLabel(
            self.card,
            text=icon,
            font=("Arial", 28, "bold"),
            width=58,
            height=58,
            corner_radius=29,
            fg_color=badge_bg,
            text_color=accent_color
        )
        self.icon_badge.pack(pady=(20, 8))

        # 2. Judul Status
        self.title_label = ctk.CTkLabel(
            self.card,
            text=default_title,
            font=("Arial", 16, "bold"),
            text_color="#0f172a"
        )
        self.title_label.pack(pady=(0, 2))

        # 3. Pesan Notifikasi
        self.message_label = ctk.CTkLabel(
            self.card,
            text=message,
            font=("Arial", 12),
            text_color="#64748b",
            wraplength=290
        )
        self.message_label.pack(pady=(0, 15))

        # Tutup Otomatis setelah 1.5 detik
        self.after(1500, self.close)

    def center_to_parent(self, parent, width, height):
        """Menghitung koordinat agar pop-up selalu muncul tepat di tengah parent window"""
        try:
            parent.update_idletasks()
            px = parent.winfo_rootx()
            py = parent.winfo_rooty()
            pw = parent.winfo_width()
            ph = parent.winfo_height()

            x = px + (pw // 2) - (width // 2)
            y = py + (ph // 2) - (height // 2)
            self.geometry(f"{width}x{height}+{x}+{y}")
        except Exception:
            pass

    def close(self):
        self.destroy()