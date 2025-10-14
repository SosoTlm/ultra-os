#!/usr/bin/env python3
"""
UltraOS v2.237 - Sunsettling Preview
Requires: pip install customtkinter pillow psutil tkhtmlview
"""

import customtkinter as ctk
from tkinter import messagebox, filedialog, scrolledtext
import tkinter as tk
import os
import time
import threading
import subprocess
import webbrowser
from datetime import datetime
import psutil
from PIL import Image, ImageDraw
import io

# Color scheme
COLORS = {
    "bg": "#0a0404",
    "surface": "#1a0f0f",
    "accent": "#ff5c33",
    "accent_hover": "#ff3c00",
    "text": "#ffffff",
    "text_dim": "#ffaa66",
}

# Set appearance
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


def create_wallpaper(width=1920, height=1080):
    """Generate animated graph wallpaper"""
    img = Image.new('RGB', (width, height), COLORS["bg"])
    draw = ImageDraw.Draw(img)
    
    # Draw grid
    grid_spacing = 60
    for x in range(0, width, grid_spacing):
        draw.line([(x, 0), (x, height)], fill="#1a0808", width=1)
    for y in range(0, height, grid_spacing):
        draw.line([(0, y), (width, y)], fill="#1a0808", width=1)
    
    # Draw wave patterns
    import math
    for wave in range(3):
        points = []
        for x in range(0, width, 5):
            y = height // 2 + math.sin(x * 0.01 + wave * 2) * 100 + wave * 50
            points.append((x, int(y)))
        draw.line(points, fill=f"#{['ff5c33', 'ff3300', 'cc2200'][wave]}", width=2)
    
    # Draw nodes
    import random
    random.seed(42)
    for _ in range(30):
        x, y = random.randint(0, width), random.randint(0, height)
        r = random.randint(3, 8)
        draw.ellipse([x-r, y-r, x+r, y+r], fill=COLORS["accent"])
    
    return img


class UltraOS:
    def __init__(self, mode="normal"):
        self.root = ctk.CTk()
        self.root.title(f"UltraOS v2.023 - {mode.capitalize()}")
        self.root.attributes('-fullscreen', False)
        self.mode = mode
        self.current_user = os.getenv("USER") or "user"
        self.start_menu_visible = False
        
        self._setup_ui()
        self._start_clock()
    
    def _setup_ui(self):
        # Main container
        self.main = ctk.CTkFrame(self.root, fg_color=COLORS["bg"])
        self.main.pack(fill="both", expand=True)
        
        # Wallpaper canvas
        self.canvas = tk.Canvas(self.main, bg=COLORS["bg"], highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        
        # Generate and display wallpaper
        threading.Thread(target=self._load_wallpaper, daemon=True).start()
        
        # Desktop title
        self.title_label = ctk.CTkLabel(
            self.canvas, text="UltraOS", 
            font=("Inter", 64, "bold"),
            text_color=COLORS["accent"]
        )
        self.title_label.place(relx=0.5, rely=0.1, anchor="center")
        
        # Desktop icons
        self._create_desktop_icons()
        
        # Taskbar
        self._create_taskbar()
        
        # Start menu
        self._create_start_menu()
    
    def _load_wallpaper(self):
        """Load wallpaper in background"""
        try:
            wall = create_wallpaper(1920, 1080)
            # Convert to PhotoImage
            import io
            bio = io.BytesIO()
            wall.save(bio, format='PNG')
            bio.seek(0)
            self.wallpaper = tk.PhotoImage(data=bio.read())
            self.canvas.create_image(0, 0, image=self.wallpaper, anchor="nw")
        except Exception as e:
            print(f"Wallpaper error: {e}")
    
    def _create_desktop_icons(self):
        icons_data = [
            ("📁 Fichiers", self.open_file_manager),
            ("💻 Terminal", self.open_terminal),
            ("📝 Editeur", self.open_text_editor),
            ("📊 Taches", self.open_task_manager),
            ("⚙️ Parametres", self.open_settings),
            ("🌐 Web", self.open_browser),
        ]
        
        for i, (text, cmd) in enumerate(icons_data):
            x, y = 50 + (i // 3) * 150, 200 + (i % 3) * 100
            btn = ctk.CTkButton(
                self.canvas, text=text, command=cmd,
                width=120, height=70,
                fg_color=COLORS["surface"],
                hover_color=COLORS["accent"],
                font=("Inter", 12, "bold")
            )
            self.canvas.create_window(x, y, window=btn)
    
    def _create_taskbar(self):
        self.taskbar = ctk.CTkFrame(self.root, height=50, fg_color=COLORS["surface"])
        self.taskbar.pack(side="bottom", fill="x")
        
        self.start_btn = ctk.CTkButton(
            self.taskbar, text="⚡ Démmarer", command=self.toggle_start,
            width=100, fg_color=COLORS["accent"],
            hover_color=COLORS["accent_hover"],
            font=("Inter", 14, "bold")
        )
        self.start_btn.pack(side="left", padx=10, pady=5)
        
        self.clock = ctk.CTkLabel(
            self.taskbar, text="00:00",
            font=("Inter", 14), text_color=COLORS["text"]
        )
        self.clock.pack(side="right", padx=20)
    
    def _create_start_menu(self):
        self.start_menu = ctk.CTkToplevel(self.root)
        self.start_menu.title("Start")
        self.start_menu.geometry("250x350")
        self.start_menu.overrideredirect(True)
        self.start_menu.withdraw()
        self.start_menu.configure(fg_color=COLORS["surface"])
        
        items = [
            ("📁 Fichiers", self.open_file_manager),
            ("💻 Terminal", self.open_terminal),
            ("📝 Editeur", self.open_text_editor),
            ("📊 Taches", self.open_task_manager),
            ("🌐 Web", self.open_browser),
            ("⚙️ Paramètres", self.open_settings),
            ("🚪 Eteindre", self.root.quit),
        ]
        
        for name, action in items:
            btn = ctk.CTkButton(
                self.start_menu, text=name,
                command=lambda a=action: [self.start_menu.withdraw(), a()],
                fg_color="transparent", hover_color=COLORS["accent"],
                anchor="w", height=40
            )
            btn.pack(fill="x", padx=10, pady=2)
    
    def toggle_start(self):
        if self.start_menu.winfo_viewable():
            self.start_menu.withdraw()
        else:
            x = self.root.winfo_x() + 10
            y = self.root.winfo_y() + self.root.winfo_height() - 400
            self.start_menu.geometry(f"+{x}+{y}")
            self.start_menu.deiconify()
    
    def _start_clock(self):
        def update():
            while True:
                self.clock.configure(text=datetime.now().strftime("%H:%M:%S"))
                time.sleep(1)
        threading.Thread(target=update, daemon=True).start()
    
    # Applications
    
    def open_terminal(self):
        win = ctk.CTkToplevel(self.root)
        win.title("Terminal")
        win.geometry("900x600")
        
        frame = ctk.CTkFrame(win, fg_color=COLORS["surface"])
        frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        text = scrolledtext.ScrolledText(
            frame, bg="#0a0a0a", fg="#00ff00",
            font=("Consolas", 11), insertbackground="#00ff00"
        )
        text.pack(fill="both", expand=True)
        text.insert("end", f"UltraOS Terminal v2.023\n{self.current_user}@ultraos:~$ ")
        
        def execute(event):
            cmd = text.get("end-2l linestart", "end-1c").split("$")[-1].strip()
            if cmd:
                text.insert("end", "\n")
                try:
                    if cmd == "clear":
                        text.delete("1.0", "end")
                    elif cmd == "help":
                        text.insert("end", "Commands: ls, pwd, whoami, date, clear, exit\n")
                    elif cmd == "ls":
                        text.insert("end", "\n".join(os.listdir()) + "\n")
                    elif cmd == "pwd":
                        text.insert("end", os.getcwd() + "\n")
                    elif cmd == "date":
                        text.insert("end", datetime.now().strftime("%c") + "\n")
                    elif cmd == "whoami":
                        text.insert("end", self.current_user + "\n")
                    elif cmd == "exit":
                        win.destroy()
                        return
                    else:
                        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=5)
                        text.insert("end", result.stdout or result.stderr or "Command executed\n")
                except Exception as e:
                    text.insert("end", f"Error: {e}\n")
                text.insert("end", f"{self.current_user}@ultraos:~$ ")
                text.see("end")
            return "break"
        
        text.bind("<Return>", execute)
        text.focus()
    
    def open_file_manager(self):
        win = ctk.CTkToplevel(self.root)
        win.title("File Manager")
        win.geometry("900x650")
        
        frame = ctk.CTkFrame(win)
        frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        path_frame = ctk.CTkFrame(frame)
        path_frame.pack(fill="x", pady=5)
        
        path_var = tk.StringVar(value=os.getcwd())
        path_entry = ctk.CTkEntry(path_frame, textvariable=path_var)
        path_entry.pack(side="left", fill="x", expand=True, padx=5)
        
        tree_frame = ctk.CTkFrame(frame)
        tree_frame.pack(fill="both", expand=True)
        
        import tkinter.ttk as ttk
        tree = ttk.Treeview(tree_frame, columns=("Name", "Size", "Modified"), show="headings")
        tree.heading("Name", text="Name")
        tree.heading("Size", text="Size")
        tree.heading("Modified", text="Modified")
        tree.pack(fill="both", expand=True)
        
        def load_dir():
            tree.delete(*tree.get_children())
            try:
                for item in os.listdir(path_var.get()):
                    p = os.path.join(path_var.get(), item)
                    size = f"{os.path.getsize(p)} B" if os.path.isfile(p) else "DIR"
                    mod = datetime.fromtimestamp(os.path.getmtime(p)).strftime("%Y-%m-%d %H:%M")
                    tree.insert("", "end", values=(item, size, mod))
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
        load_dir()
        ctk.CTkButton(path_frame, text="⟳", width=50, command=load_dir).pack(side="right", padx=5)
    
    def open_text_editor(self):
        win = ctk.CTkToplevel(self.root)
        win.title("Text Editor")
        win.geometry("950x700")
        
        frame = ctk.CTkFrame(win)
        frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        text = scrolledtext.ScrolledText(
            frame, wrap="word", bg=COLORS["surface"],
            fg=COLORS["text"], insertbackground="white",
            font=("Consolas", 11)
        )
        text.pack(fill="both", expand=True)
        
        def save_file():
            path = filedialog.asksaveasfilename(defaultextension=".txt")
            if path:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(text.get("1.0", "end"))
                messagebox.showinfo("Saved", f"File saved: {path}")
        
        btn_frame = ctk.CTkFrame(frame)
        btn_frame.pack(fill="x", pady=5)
        ctk.CTkButton(btn_frame, text="💾 Save", command=save_file).pack(side="left", padx=5)
    
    def open_task_manager(self):
        win = ctk.CTkToplevel(self.root)
        win.title("Task Manager")
        win.geometry("950x600")
        
        frame = ctk.CTkFrame(win)
        frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        import tkinter.ttk as ttk
        tree = ttk.Treeview(frame, columns=("PID", "Name", "CPU%", "Memory%"), show="headings")
        for col in tree["columns"]:
            tree.heading(col, text=col)
        tree.pack(fill="both", expand=True)
        
        def refresh():
            tree.delete(*tree.get_children())
            for proc in list(psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']))[:50]:
                try:
                    info = proc.info
                    tree.insert("", "end", values=(
                        info['pid'], info['name'][:30],
                        f"{info['cpu_percent']:.1f}",
                        f"{info['memory_percent']:.1f}"
                    ))
                except:
                    continue
        
        def loop_refresh():
            while win.winfo_exists():
                refresh()
                time.sleep(3)
        
        threading.Thread(target=loop_refresh, daemon=True).start()
    
    def open_browser(self):
        try:
            from tkhtmlview import HTMLLabel
        except ImportError:
            messagebox.showerror("Missing", "tkhtmlview not installed.\nRun: pip install tkhtmlview")
            return
        win = ctk.CTkToplevel(self.root)
        win.title("UltraWeB")
        win.geometry("900x600")
        frame = ctk.CTkFrame(win)
        frame.pack(fill="both", expand=True)
        ctk.CTkLabel(frame, text="Browser (0.0.2341)", font=("Inter", 14, "bold")).pack(pady=10)
        html = """
        <h1 style='color:#ff3c00'>Web</h1>
        <p>La fonction web est actuellement en phase de <b>développement<b> et n'est pas 100% publier au publique.</p>
        <p><i>[Dévelopement: Beta bientot finis]</i></p>
        """
        view = HTMLLabel(frame, html=html, background=COLORS["surface"])
        view.pack(fill="both", expand=True, padx=10, pady=10)
    
    def open_settings(self):
        win = ctk.CTkToplevel(self.root)
        win.title("Settings")
        win.geometry("500x400")
        
        frame = ctk.CTkFrame(win)
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(
            frame, text="UltraOS Settings",
            font=("Inter", 24, "bold"),
            text_color=COLORS["accent"]
        ).pack(pady=20)
        
        info_text = """UltraOS Version 2.023 Sunsettling
Build: 0783
License: ULTFRee™ (Limited)

⚠️ BETA PREVIEW VERSION ⚠️
"""
        ctk.CTkLabel(frame, text=info_text, justify="left").pack(pady=10)
    
    def run(self):
        self.root.mainloop()


def boot_menu():
    """Boot menu with modern design"""
    boot = ctk.CTk()
    boot.title("GRuLTRA Bootloader")
    boot.geometry("600x400")
    
    ctk.CTkLabel(
        boot, text="Boot Options",
        font=("Inter", 32, "bold"),
        text_color=COLORS["accent"]
    ).pack(pady=40)
    
    def launch(mode):
        boot.destroy()
        os_sys = UltraOS(mode=mode)
        os_sys.run()
    
    for text, mode in [("🔆 Normal", "normal"), ("🛠 Safe Mode", "safe"), ("🧯 Recovery", "recovery")]:
        ctk.CTkButton(
            boot, text=text, command=lambda m=mode: launch(m),
            width=300, height=50,
            fg_color=COLORS["accent"],
            hover_color=COLORS["accent_hover"],
            font=("Inter", 16, "bold")
        ).pack(pady=10)
    
    boot.mainloop()


if __name__ == "__main__":
    boot_menu()