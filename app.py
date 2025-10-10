#!/usr/bin/env python3
"""
UltraOS v2.0 - OS moderne ultra-minimaliste en Python (amélioré)
Système d'exploitation graphique avec gestionnaire de tâches réel
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import os
import sys
import time
import threading
import subprocess
import webbrowser
from datetime import datetime
import psutil  # Pour le gestionnaire de tâches réel

# ------------- Classe principale UltraOS ------------- #
class UltraOS:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("UltraOS v2.0 (Fennec Fox)")
        self.root.geometry("1200x800")
        self.root.configure(bg="#0a0a0a")
        self.current_user = os.getenv("USERNAME") or os.getenv("USER") or "user"
        self.apps = {}

        self._configure_style()
        self._create_desktop()
        self._create_taskbar()
        self._create_start_menu()
        self._start_clock()

    # ------------------ STYLE ------------------ #
    def _configure_style(self):
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TButton', background='#2d2d2d', foreground='white', relief='flat')
        self.style.map('TButton', background=[('active', '#404040')])
        self.style.configure('TFrame', background='#1a1a1a')

    # ------------------ INTERFACE ------------------ #
    def _create_desktop(self):
        self.desktop = tk.Frame(self.root, bg="#0a0a0a")
        self.desktop.pack(fill=tk.BOTH, expand=True)
        title = tk.Label(self.desktop, text="UltraOS", font=("Arial", 48, "bold"), fg="#00ff88", bg="#0a0a0a")
        title.place(relx=0.5, rely=0.1, anchor="center")
        self._create_desktop_icons()

    def _create_desktop_icons(self):
        icons = [
            ("📁 Gestionnaire", self.open_file_manager, 100, 200),
            ("💻 Terminal", self.open_terminal, 100, 300),
            ("📝 Éditeur", self.open_text_editor, 100, 400),
            ("📊 Tâches", self.open_task_manager, 100, 500),
            ("⚙️ Paramètres", self.open_settings, 250, 200),
            ("🌐 Navigateur", self.open_browser, 250, 300),
        ]
        for text, command, x, y in icons:
            tk.Button(self.desktop, text=text, command=command,
                      bg="#2d2d2d", fg="white", width=14, height=2,
                      font=("Arial", 10, "bold")).place(x=x, y=y)

    def _create_taskbar(self):
        self.taskbar = tk.Frame(self.root, bg="#1a1a1a", height=40)
        self.taskbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.start_button = tk.Button(self.taskbar, text="⚡ Start", command=self.toggle_start_menu,
                                      bg="#00ff88", fg="black", font=("Arial", 10, "bold"), relief="flat")
        self.start_button.pack(side=tk.LEFT, padx=5)
        self.clock_label = tk.Label(self.taskbar, bg="#1a1a1a", fg="white", font=("Arial", 10))
        self.clock_label.pack(side=tk.RIGHT, padx=10)

    def _create_start_menu(self):
        self.start_menu = tk.Toplevel(self.root)
        self.start_menu.title("Menu")
        self.start_menu.geometry("250x400")
        self.start_menu.configure(bg="#1a1a1a")
        self.start_menu.overrideredirect(True)
        self.start_menu.withdraw()
        menu_items = [
            ("📁 Gestionnaire de fichiers", self.open_file_manager),
            ("💻 Terminal", self.open_terminal),
            ("📝 Éditeur de texte", self.open_text_editor),
            ("📊 Gestionnaire de tâches", self.open_task_manager),
            ("🌐 Navigateur web", self.open_browser),
            ("⚙️ Paramètres", self.open_settings),
        ]
        for name, action in menu_items:
            tk.Button(self.start_menu, text=name, command=lambda a=action: [self.start_menu.withdraw(), a()],
                      bg="#2d2d2d", fg="white", anchor="w", relief="flat").pack(fill=tk.X, padx=10, pady=2)

    def toggle_start_menu(self):
        if self.start_menu.winfo_viewable():
            self.start_menu.withdraw()
        else:
            x = self.root.winfo_x() + 10
            y = self.root.winfo_y() + self.root.winfo_height() - 450
            self.start_menu.geometry(f"+{x}+{y}")
            self.start_menu.deiconify()

    def _start_clock(self):
        def update():
            while True:
                now = datetime.now().strftime("%H:%M:%S")
                self.clock_label.config(text=now)
                time.sleep(1)
        threading.Thread(target=update, daemon=True).start()

    # ------------------ APPLICATIONS ------------------ #
    def open_terminal(self):
        win = tk.Toplevel(self.root)
        win.title("Terminal")
        win.geometry("800x500")
        text = scrolledtext.ScrolledText(win, bg="#0a0a0a", fg="#00ff88", font=("Consolas", 11),
                                         insertbackground="white")
        text.pack(fill=tk.BOTH, expand=True)
        text.insert(tk.END, f"UltraOS Terminal v2.0\n{self.current_user}@ultraos:~$ ")

        def execute(event):
            cmd = text.get("end-2l linestart", "end-1c").split("$")[-1].strip()
            if cmd:
                text.insert(tk.END, "\n")
                try:
                    if cmd == "clear":
                        text.delete("1.0", tk.END)
                    elif cmd == "help":
                        text.insert(tk.END, "Commandes: ls, pwd, whoami, date, exit, clear\n")
                    elif cmd == "ls":
                        text.insert(tk.END, "\n".join(os.listdir()) + "\n")
                    elif cmd == "pwd":
                        text.insert(tk.END, os.getcwd() + "\n")
                    elif cmd == "date":
                        text.insert(tk.END, datetime.now().strftime("%c") + "\n")
                    elif cmd == "whoami":
                        text.insert(tk.END, self.current_user + "\n")
                    elif cmd == "exit":
                        win.destroy()
                        return
                    else:
                        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                        text.insert(tk.END, result.stdout or result.stderr)
                except Exception as e:
                    text.insert(tk.END, f"Erreur: {e}\n")
                text.insert(tk.END, f"{self.current_user}@ultraos:~$ ")
                text.see(tk.END)
            return "break"

        text.bind("<Return>", execute)
        text.focus()

    def open_file_manager(self):
        win = tk.Toplevel(self.root)
        win.title("Gestionnaire de fichiers")
        win.geometry("800x600")
        path_var = tk.StringVar(value=os.getcwd())
        path_entry = tk.Entry(win, textvariable=path_var, bg="#333", fg="white")
        path_entry.pack(fill=tk.X)

        tree = ttk.Treeview(win, columns=("Taille", "Type", "Modifié"), show="headings")
        for col in tree["columns"]:
            tree.heading(col, text=col)
        tree.pack(fill=tk.BOTH, expand=True)

        def load_directory(path):
            tree.delete(*tree.get_children())
            try:
                for item in os.listdir(path):
                    p = os.path.join(path, item)
                    size = f"{os.path.getsize(p)} B" if os.path.isfile(p) else "Dossier"
                    ftype = "Fichier" if os.path.isfile(p) else "Dossier"
                    mod = datetime.fromtimestamp(os.path.getmtime(p)).strftime("%Y-%m-%d %H:%M")
                    tree.insert("", "end", values=(item, size, ftype, mod))
            except Exception as e:
                messagebox.showerror("Erreur", str(e))

        load_directory(path_var.get())

    def open_text_editor(self):
        win = tk.Toplevel(self.root)
        win.title("Éditeur de texte")
        win.geometry("900x700")
        text = scrolledtext.ScrolledText(win, wrap=tk.WORD, bg="#1e1e1e", fg="white", insertbackground="white")
        text.pack(fill=tk.BOTH, expand=True)

        def save_file():
            path = filedialog.asksaveasfilename(defaultextension=".txt")
            if path:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(text.get("1.0", tk.END))

        menubar = tk.Menu(win)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Enregistrer sous", command=save_file)
        menubar.add_cascade(label="Fichier", menu=file_menu)
        win.config(menu=menubar)

    def open_task_manager(self):
        win = tk.Toplevel(self.root)
        win.title("Gestionnaire de tâches")
        win.geometry("900x500")
        tree = ttk.Treeview(win, columns=("PID", "Nom", "CPU %", "Mémoire %"), show="headings")
        for col in tree["columns"]:
            tree.heading(col, text=col)
        tree.pack(fill=tk.BOTH, expand=True)

        def refresh():
            tree.delete(*tree.get_children())
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                try:
                    pinfo = proc.info
                    tree.insert("", "end", values=(pinfo['pid'], pinfo['name'],
                                                   f"{pinfo['cpu_percent']:.1f}",
                                                   f"{pinfo['memory_percent']:.1f}"))
                except psutil.NoSuchProcess:
                    continue

        def loop_refresh():
            while True:
                refresh()
                time.sleep(2)

        threading.Thread(target=loop_refresh, daemon=True).start()

    def open_browser(self):
        webbrowser.open("https://www.google.com")

    def open_settings(self):
        win = tk.Toplevel(self.root)
        win.title("Paramètres")
        win.geometry("400x300")
        tk.Label(win, text="Paramètres d'UltraOS", font=("Arial", 16)).pack(pady=20)
        tk.Label(win, text="(Personnalisation à venir)", fg="gray").pack()

    # ------------------ LANCEMENT ------------------ #
    def run(self):
        self.root.mainloop()


# ------------- Point d’entrée du système ------------- #
def main():
    os_system = UltraOS()
    os_system.run()

if __name__ == "__main__":
    main()
