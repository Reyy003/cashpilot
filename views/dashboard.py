import customtkinter as ctk
import os

from PIL import Image, ImageDraw, ImageOps
from matplotlib.ticker import MultipleLocator, FuncFormatter
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from query import (
    get_dashboard_summary,
    get_cashflow_chart,
    get_user_profile
)


def make_circular_image(image_path_or_pil, size):
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


class Dashboard(ctk.CTk):

    def __init__(self, user_id):
        super().__init__()

        self.user_id = user_id
        self.sidebar = None
        self.content = None
        self.active_menu = "Dashboard"

        # Variabel Kontrol Status Sidebar
        self.is_sidebar_expanded = False
        self.collapse_timer = None

        # Mode Tampilan Default (Light)
        ctk.set_appearance_mode("light")

        # ==============================
        # WINDOW CONFIGURATION
        # ==============================
        self.title("CashPilot Dashboard")
        self.geometry("1200x700")
        self.minsize(1050, 650)
        
        # Pasang Ikon Window Aplikasi (.ico)
        try:
            self.iconbitmap("cashpilot_logo.ico")
        except Exception:
            pass

        self.resizable(True, True)
        self.after(0, lambda: self.state('zoomed'))

        # Latar belakang jendela utama (Nuansa Modern Slate)
        self.configure(fg_color=("#f1f5f9", "#0f172a"))

        # ==============================
        # SIDEBAR & CONTENT CONTAINER
        # ==============================
        self.content = ctk.CTkFrame(
            self,
            fg_color=("#ffffff", "#1e293b"),
            corner_radius=20,
            border_width=1,
            border_color=("#e2e8f0", "#334155")
        )

        self.build_sidebar()
        self.show_dashboard()

    # ==================================
    # SIDEBAR ULTIMATE UI (FIXED LAYOUT ORDER)
    # ==================================
    def build_sidebar(self):
        if self.content is not None:
            try:
                self.content.pack_forget()
            except Exception:
                pass

        if self.sidebar is not None:
            try:
                self.sidebar.destroy()
            except Exception:
                pass

        self.sidebar = ctk.CTkFrame(
            self,
            width=80,
            corner_radius=24,
            fg_color=("#ffffff", "#181825"),
            border_width=1,
            border_color=("#e2e8f0", "#27273a")
        )
        self.sidebar.pack_propagate(False)
        self.sidebar.pack(side="left", fill="y", padx=(20, 0), pady=20)

        if self.content is not None:
            self.content.pack(
                side="right",
                fill="both",
                expand=True,
                padx=(10, 20),
                pady=20
            )

        self.sidebar.bind("<Enter>", self.on_sidebar_enter)
        self.sidebar.bind("<Leave>", self.on_sidebar_leave)

        user = None
        try:
            user = get_user_profile(self.user_id)
        except Exception as e:
            print("Profile Error :", e)

        # 1. Logo Brand
        self.logo_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.logo_frame.pack(fill="x", padx=15, pady=(20, 15))
        self.logo_frame.bind("<Enter>", self.on_sidebar_enter)

        try:
            img_logo_raw = Image.open("cashpilot_logo.png").resize((28, 28), Image.Resampling.LANCZOS)
            self.sidebar_logo_img = ctk.CTkImage(light_image=img_logo_raw, dark_image=img_logo_raw, size=(28, 28))
            self.logo_icon = ctk.CTkLabel(self.logo_frame, image=self.sidebar_logo_img, text="")
        except Exception:
            self.logo_icon = ctk.CTkLabel(self.logo_frame, text="🛍️", font=("Arial", 22))

        self.logo_icon.pack(side="left", padx=(2, 0))

        self.logo_text = ctk.CTkLabel(
            self.logo_frame,
            text="CASHPILOT",
            font=("Arial", 15, "bold"),
            text_color=("#0f172a", "#ffffff")
        )

        # 2. User Profile Box
        self.user_card = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.user_card.pack(fill="x", padx=10, pady=(0, 20))
        self.user_card.bind("<Enter>", self.on_sidebar_enter)

        if user and user.get("foto"):
            foto_path = user["foto"]
            if not os.path.exists(foto_path):
                foto_path = os.path.join("assets", "profile", user["foto"])

            if os.path.exists(foto_path):
                circular_img = make_circular_image(foto_path, (46, 46))
                self.profile_img = ctk.CTkImage(light_image=circular_img, dark_image=circular_img, size=(46, 46))
                self.profile_avatar = ctk.CTkLabel(self.user_card, image=self.profile_img, text="")
            else:
                self.profile_avatar = ctk.CTkLabel(self.user_card, text="👤", font=("Arial", 24), text_color="#a855f7")
        else:
            self.profile_avatar = ctk.CTkLabel(self.user_card, text="👤", font=("Arial", 24), text_color="#a855f7")

        self.profile_avatar.pack(side="left", padx=(8, 0))

        self.user_info_frame = ctk.CTkFrame(self.user_card, fg_color="transparent")
        nama_user = user["nama"] if user else "Pengguna"

        self.lbl_user_name = ctk.CTkLabel(
            self.user_info_frame,
            text=nama_user if len(nama_user) <= 12 else nama_user[:10] + "..",
            font=("Arial", 13, "bold"),
            text_color=("#0f172a", "#ffffff"),
            anchor="w"
        )
        self.lbl_user_name.pack(fill="x")

        self.lbl_user_role = ctk.CTkLabel(
            self.user_info_frame,
            text="Project Manager",
            font=("Arial", 10),
            text_color=("#64748b", "#94a3b8"),
            anchor="w"
        )
        self.lbl_user_role.pack(fill="x")

        # 3. Navigation Menu Items
        menu = [
            ("⊞", "Dashboard", "⊞    Dashboard", self.show_dashboard),
            ("📁", "Proyek", "📁    Proyek", self.open_project),
            ("⚙️", "Edit Profil", "⚙️    Edit Profil", self.open_profile),
            ("ℹ️", "Version", "ℹ️    Version", self.show_version),
            ("🚪", "Logout", "🚪    Logout", self.confirm_logout)
        ]

        self.menu_buttons = {}

        for icon, key, full_text, command in menu:
            is_active = (key == self.active_menu)
            
            item_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent", height=42)
            item_frame.pack(fill="x", pady=3)
            item_frame.bind("<Enter>", self.on_sidebar_enter)

            pill = ctk.CTkFrame(
                item_frame,
                width=4,
                height=28,
                corner_radius=2,
                fg_color="#7c3aed" if is_active else "transparent"
            )
            pill.pack(side="right", padx=(0, 2))

            btn = ctk.CTkButton(
                item_frame,
                text=icon,
                width=54,
                height=42,
                corner_radius=12,
                fg_color=("#f3e8ff", "#2e1065") if is_active else "transparent",
                hover_color=("#f3e8ff", "#2e1065") if is_active else ("#f8fafc", "#27273a"),
                text_color="#7c3aed" if is_active else ("#64748b", "#94a3b8"),
                font=("Arial", 16, "bold" if is_active else "normal"),
                anchor="center",
                command=lambda k=key, cmd=command: self.handle_menu_click(k, cmd)
            )
            btn.pack(side="left", fill="both", expand=True, padx=(8, 4))
            btn.bind("<Enter>", self.on_sidebar_enter)
            
            self.menu_buttons[key] = {
                "btn": btn,
                "pill": pill,
                "icon": icon,
                "full_text": full_text
            }

        # 4. DARK MODE TOGGLE
        self.dark_mode_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.dark_mode_frame.pack(side="bottom", fill="x", padx=12, pady=20)
        self.dark_mode_frame.bind("<Enter>", self.on_sidebar_enter)

        self.dark_icon = ctk.CTkLabel(
            self.dark_mode_frame,
            text="🌙",
            font=("Arial", 16)
        )
        self.dark_icon.pack(side="left", padx=(5, 0))

        self.dark_label = ctk.CTkLabel(
            self.dark_mode_frame,
            text="Dark Mode",
            font=("Arial", 12, "bold"),
            text_color=("#64748b", "#94a3b8")
        )

        self.dark_switch = ctk.CTkSwitch(
            self.dark_mode_frame,
            text="",
            width=42,
            progress_color="#7c3aed",
            command=self.toggle_dark_mode
        )
        self.dark_switch.bind("<Enter>", self.on_sidebar_enter)

    def on_sidebar_enter(self, event=None):
        if self.collapse_timer:
            try:
                self.after_cancel(self.collapse_timer)
            except Exception:
                pass
            self.collapse_timer = None

        if not self.is_sidebar_expanded:
            self.is_sidebar_expanded = True
            if self.sidebar.winfo_exists():
                self.sidebar.configure(width=220)

            self.logo_text.pack(side="left", padx=(10, 0))
            self.user_info_frame.pack(side="left", fill="both", expand=True, padx=(10, 0))
            self.dark_label.pack(side="left", padx=(10, 0))
            self.dark_switch.pack(side="right", padx=(0, 5))

            for key, data in self.menu_buttons.items():
                data["btn"].configure(
                    text=data["full_text"],
                    anchor="w",
                    font=("Arial", 13, "bold" if key == self.active_menu else "normal")
                )

    def on_sidebar_leave(self, event=None):
        if self.collapse_timer:
            try:
                self.after_cancel(self.collapse_timer)
            except Exception:
                pass
        self.collapse_timer = self.after(80, self._collapse_sidebar_instant)

    def _collapse_sidebar_instant(self):
        if self.is_sidebar_expanded and self.winfo_exists():
            self.is_sidebar_expanded = False
            if self.sidebar and self.sidebar.winfo_exists():
                self.sidebar.configure(width=80)

            try:
                self.logo_text.pack_forget()
                self.user_info_frame.pack_forget()
                self.dark_label.pack_forget()
                self.dark_switch.pack_forget()
            except Exception:
                pass

            for key, data in self.menu_buttons.items():
                try:
                    data["btn"].configure(
                        text=data["icon"],
                        anchor="center",
                        font=("Arial", 16)
                    )
                except Exception:
                    pass

    def toggle_dark_mode(self):
        if self.dark_switch.get() == 1:
            ctk.set_appearance_mode("dark")
        else:
            ctk.set_appearance_mode("light")

        if self.active_menu == "Dashboard":
            self.create_chart()
            
        for widget in self.content.winfo_children():
            if hasattr(widget, "load_data"):
                try:
                    widget.load_data()
                except Exception:
                    pass

    def handle_menu_click(self, key, command):
        if key != "Logout":
            self.active_menu = key
            for k, data in self.menu_buttons.items():
                is_act = (k == key)
                data["pill"].configure(fg_color="#7c3aed" if is_act else "transparent")
                data["btn"].configure(
                    fg_color=("#f3e8ff", "#2e1065") if is_act else "transparent",
                    text_color="#7c3aed" if is_act else ("#64748b", "#94a3b8")
                )
        command()

    def show_dashboard(self):
        self.clear_content()

        # ==========================================
        # DEKORATIF HEADER BANNER (Gaya Modern Card)
        # ==========================================
        header_banner = ctk.CTkFrame(
            self.content,
            fg_color=("#f8fafc", "#162032"),
            corner_radius=16,
            border_width=1,
            border_color=("#e2e8f0", "#2a3950")
        )
        header_banner.pack(fill="x", padx=25, pady=(20, 15))

        banner_inner = ctk.CTkFrame(header_banner, fg_color="transparent")
        banner_inner.pack(fill="both", expand=True, padx=20, pady=16)

        # Kiri: Judul & Subjudul
        title_box = ctk.CTkFrame(banner_inner, fg_color="transparent")
        title_box.pack(side="left", fill="x", expand=True)

        ctk.CTkLabel(
            title_box,
            text="🚀 Dashboard Overview",
            font=("Arial", 22, "bold"),
            text_color=("#0f172a", "#ffffff")
        ).pack(anchor="w")

        ctk.CTkLabel(
            title_box,
            text="Pantau statistik keuangan dan performa proyek kamu dalam satu kendali.",
            font=("Arial", 12),
            text_color=("#64748b", "#94a3b8")
        ).pack(anchor="w", pady=(2, 0))

        # Kanan: Badge Status / Indikator Aktif
        status_badge = ctk.CTkFrame(
            banner_inner,
            fg_color=("#f3e8ff", "#2e1065"),
            corner_radius=10,
            border_width=1,
            border_color=("#d8b4fe", "#581c87")
        )
        status_badge.pack(side="right", padx=(10, 0))

        ctk.CTkLabel(
            status_badge,
            text="⚡ Live Active",
            font=("Arial", 11, "bold"),
            text_color=("#7c3aed", "#c084fc")
        ).pack(padx=12, pady=6)

        # Ambil data ringkasan
        data = get_dashboard_summary(self.user_id)

        # ==========================================
        # CARD GRID STATISTIK
        # ==========================================
        card_grid = ctk.CTkFrame(self.content, fg_color="transparent")
        card_grid.pack(fill="x", padx=20, pady=(5, 15))

        for i in range(4):
            card_grid.grid_columnconfigure(i, weight=1, uniform="card")

        self.card(card_grid, 0, "Total Project", str(data["project"]), "📁", "#3b82f6", ("#eff6ff", "#1e3a8a"))
        self.card(card_grid, 1, "Pemasukan", self.rupiah(data["income"]), "📈", "#10b981", ("#ecfdf5", "#064e3b"))
        self.card(card_grid, 2, "Pengeluaran", self.rupiah(data["expense"]), "📉", "#ef4444", ("#fef2f2", "#7f1d1d"))
        self.card(card_grid, 3, "Saldo", self.rupiah(data["balance"]), "💰", "#059669", ("#d1fae5", "#065f46"))

        self.create_chart()

    def card(self, parent, col, title, value, icon, accent_color, badge_bg):
        # Kartu Statistik dengan Border Halus & Aksen Garis di Samping/Atas
        frame = ctk.CTkFrame(
            parent,
            corner_radius=16,
            fg_color=("#ffffff", "#162032"),
            border_width=1,
            border_color=("#e2e8f0", "#2a3950")
        )
        frame.grid(row=0, column=col, padx=8, pady=5, sticky="ew")

        # Indikator garis warna tipis di bagian atas kartu sebagai hiasan modern
        top_accent_line = ctk.CTkFrame(frame, height=4, fg_color=accent_color, corner_radius=2)
        top_accent_line.pack(fill="x", padx=12, pady=(12, 0))

        card_inner = ctk.CTkFrame(frame, fg_color="transparent")
        card_inner.pack(fill="both", expand=True, padx=15, pady=(10, 15))

        top_frame = ctk.CTkFrame(card_inner, fg_color="transparent")
        top_frame.pack(fill="x")

        ctk.CTkLabel(
            top_frame,
            text=title,
            font=("Arial", 12, "bold"),
            text_color=("#64748b", "#94a3b8")
        ).pack(side="left")

        icon_badge = ctk.CTkLabel(
            top_frame,
            text=icon,
            font=("Arial", 14),
            width=32,
            height=32,
            corner_radius=16,
            fg_color=badge_bg,
            text_color=accent_color
        )
        icon_badge.pack(side="right")

        ctk.CTkLabel(
            card_inner,
            text=value,
            font=("Arial", 18, "bold"),
            text_color=("#0f172a", "#ffffff"),
            anchor="w"
        ).pack(fill="x", pady=(10, 0))

    def create_chart(self):
        for widget in self.content.winfo_children():
            if isinstance(widget, ctk.CTkFrame) and getattr(widget, "_is_chart_container", False):
                try:
                    widget.destroy()
                except Exception:
                    pass

        data = get_cashflow_chart(self.user_id)

        bulan = []
        pemasukan = []
        pengeluaran = []
        temp = {}

        for row in data:
            b = row["bulan"]
            if b not in temp:
                temp[b] = {"Pemasukan": 0, "Pengeluaran": 0}

            if row["jenis"] == "Pemasukan":
                temp[b]["Pemasukan"] = row["total"]
            elif row["jenis"] == "Pengeluaran":
                temp[b]["Pengeluaran"] = row["total"]

        for b, value in temp.items():
            bulan.append(b)
            pemasukan.append(float(value["Pemasukan"]))
            pengeluaran.append(float(value["Pengeluaran"]))

        chart_frame = ctk.CTkFrame(
            self.content,
            fg_color=("#ffffff", "#162032"),
            corner_radius=18,
            border_width=1,
            border_color=("#e2e8f0", "#2a3950")
        )
        chart_frame._is_chart_container = True
        chart_frame.pack(padx=20, pady=(5, 15), fill="both", expand=True)

        is_dark = ctk.get_appearance_mode().lower() == "dark"
        bg_color = "#162032" if is_dark else "#ffffff"
        text_color = "#ffffff" if is_dark else "#0f172a"

        fig = Figure(figsize=(8.6, 3.5), dpi=100)
        fig.patch.set_facecolor(bg_color)
        ax = fig.add_subplot(111)
        ax.set_facecolor(bg_color)

        if bulan:
            ax.plot(bulan, pemasukan, marker="o", linewidth=2.5, color="#10b981", label="Pemasukan")
            ax.plot(bulan, pengeluaran, marker="o", linewidth=2.5, color="#ef4444", label="Pengeluaran")

            nilai_maks = max(max(pemasukan, default=0), max(pengeluaran, default=0))
            nilai_min = min(min(pemasukan, default=0), min(pengeluaran, default=0))

            if nilai_maks <= 1000000:
                jarak = 100000
            elif nilai_maks <= 10000000:
                jarak = 500000
            elif nilai_maks <= 100000000:
                jarak = 5000000
            else:
                jarak = 10000000

            batas_atas = max(100000, nilai_maks * 1.2)
            batas_bawah = max(0, nilai_min * 0.8)

            ax.set_ylim(batas_bawah, batas_atas)
            ax.yaxis.set_major_locator(MultipleLocator(jarak))
            ax.yaxis.set_major_formatter(
                FuncFormatter(lambda x, pos: f"Rp {int(x):,}".replace(",", "."))
            )
        else:
            ax.text(0.5, 0.5, "Belum Ada Data Cashflow", horizontalalignment='center', verticalalignment='center', transform=ax.transAxes, fontsize=12, color='#94a3b8')

        ax.tick_params(colors=text_color)
        for spine in ax.spines.values():
            spine.set_color("#334155" if is_dark else "#e2e8f0")

        ax.grid(linestyle="--", alpha=0.25, color="#94a3b8")
        ax.set_title("Grafik Arus Kas (Cashflow)", fontsize=13, fontweight="bold", color=text_color, pad=12)
        ax.set_ylabel("Nominal (Rp)", fontsize=10, color="#94a3b8")
        
        legend = ax.legend(frameon=False)
        if legend:
            for t in legend.get_texts():
                t.set_color(text_color)

        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=15, pady=15)

    def rupiah(self, angka):
        return "Rp {:,}".format(angka or 0).replace(",", ".")

    def open_project(self):
        self.clear_content()
        from views.project import ProjectPage
        ProjectPage(self.content, self.user_id)

    def open_profile(self):
        self.clear_content()
        from views.profile import ProfilePage
        ProfilePage(self.content, self.user_id)

    def clear_content(self):
        for widget in self.content.winfo_children():
            try:
                widget.destroy()
            except Exception:
                pass

    def show_version(self):
        version_window = ctk.CTkToplevel(self)
        version_window.title("Version Information")
        version_window.geometry("460x520")
        version_window.resizable(False, False)
        version_window.configure(fg_color=("#f8fafc", "#0f172a"))
        version_window.grab_set()
        version_window.focus()

        card = ctk.CTkFrame(
            version_window,
            width=400,
            height=460,
            corner_radius=18,
            fg_color=("#ffffff", "#181825"),
            border_width=1,
            border_color=("#e2e8f0", "#27273a")
        )
        card.place(relx=0.5, rely=0.5, anchor="center")

        try:
            img_ver_raw = Image.open("cashpilot_logo.png").resize((52, 52), Image.Resampling.LANCZOS)
            self.version_logo_img = ctk.CTkImage(light_image=img_ver_raw, dark_image=img_ver_raw, size=(52, 52))
            ctk.CTkLabel(card, image=self.version_logo_img, text="").pack(pady=(20, 5))
        except Exception:
            ctk.CTkLabel(card, text="🛍️", font=("Arial", 32)).pack(pady=(20, 5))

        ctk.CTkLabel(card, text="CASHPILOT", font=("Arial", 24, "bold"), text_color="#7c3aed").pack(pady=(0, 2))
        ctk.CTkLabel(card, text="Project & Finance Management", font=("Arial", 11), text_color=("#64748b", "#94a3b8")).pack()

        ctk.CTkFrame(card, width=320, height=1, fg_color=("#e2e8f0", "#27273a")).pack(pady=14)
        ctk.CTkLabel(card, text="Application Version", font=("Arial", 11, "bold"), text_color=("#475569", "#cbd5e1")).pack()
        ctk.CTkLabel(card, text="v1.0.0", font=("Arial", 20, "bold"), text_color="#10b981").pack(pady=(3, 14))

        ctk.CTkLabel(card, text="Developer Contact", font=("Arial", 11, "bold"), text_color=("#475569", "#cbd5e1")).pack()
        ctk.CTkLabel(card, text="Email\nreyhann003@gmail.com", justify="center", font=("Arial", 11), text_color=("#334155", "#94a3b8")).pack(pady=(8, 4))
        ctk.CTkLabel(card, text="WhatsApp\n081234535307", justify="center", font=("Arial", 11), text_color=("#334155", "#94a3b8")).pack()

        ctk.CTkFrame(card, width=320, height=1, fg_color=("#e2e8f0", "#27273a")).pack(pady=14)
        ctk.CTkLabel(card, text="© 2026 CashPilot\nAll Rights Reserved", justify="center", font=("Arial", 10), text_color=("#64748b", "#94a3b8")).pack()

        ctk.CTkButton(
            card, text="Tutup", width=160, height=36, corner_radius=10,
            fg_color="#7c3aed", hover_color="#6d28d9", command=version_window.destroy
        ).pack(pady=15)

    def confirm_logout(self):
        modal = ctk.CTkToplevel(self)
        modal.title("Konfirmasi Logout")
        modal.geometry("380x220")
        modal.resizable(False, False)
        modal.configure(fg_color=("#f8fafc", "#0f172a"))

        modal.grab_set()
        modal.focus()
        modal.attributes("-topmost", True)

        try:
            px = self.winfo_rootx()
            py = self.winfo_rooty()
            pw = self.winfo_width()
            ph = self.winfo_height()
            x = px + (pw // 2) - (380 // 2)
            y = py + (ph // 2) - (220 // 2)
            modal.geometry(f"380x220+{x}+{y}")
        except Exception:
            pass

        card = ctk.CTkFrame(
            modal,
            fg_color=("#ffffff", "#181825"),
            corner_radius=18,
            border_width=1,
            border_color=("#e2e8f0", "#27273a")
        )
        card.pack(fill="both", expand=True, padx=12, pady=12)

        ctk.CTkLabel(
            card,
            text="🚪",
            font=("Arial", 26),
            width=50,
            height=50,
            corner_radius=25,
            fg_color="#fef2f2",
            text_color="#ef4444"
        ).pack(pady=(15, 8))

        ctk.CTkLabel(
            card,
            text="Apakah Anda yakin ingin keluar?",
            font=("Arial", 15, "bold"),
            text_color=("#0f172a", "#ffffff")
        ).pack()

        ctk.CTkLabel(
            card,
            text="Sesi login kamu akan diakhiri.",
            font=("Arial", 12),
            text_color=("#64748b", "#94a3b8")
        ).pack(pady=(2, 15))

        btn_frame = ctk.CTkFrame(card, fg_color="transparent")
        btn_frame.pack(fill="x", padx=20)

        ctk.CTkButton(
            btn_frame,
            text="Batal",
            width=140,
            height=36,
            corner_radius=8,
            fg_color=("#f1f5f9", "#27273a"),
            hover_color=("#e2e8f0", "#3f3f5a"),
            text_color=("#475569", "#cbd5e1"),
            font=("Arial", 12, "bold"),
            command=modal.destroy
        ).pack(side="left", padx=(0, 5), expand=True)

        ctk.CTkButton(
            btn_frame,
            text="Ya, Keluar",
            width=140,
            height=36,
            corner_radius=8,
            fg_color="#ef4444",
            hover_color="#dc2626",
            text_color="#ffffff",
            font=("Arial", 12, "bold"),
            command=lambda: [modal.destroy(), self.logout()]
        ).pack(side="right", padx=(5, 0), expand=True)

    def logout(self):
        self.destroy()
        from views.login import LoginPage
        login = LoginPage()
        login.mainloop()