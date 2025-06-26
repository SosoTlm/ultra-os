#!/usr/bin/env python3
"""
UltraOS - Un OS moderne ultra-minimaliste en Python
Système d'exploitation avec interface graphique moderne et applications intégrées
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import os
import json
import time
import threading
import subprocess
import sys
from datetime import datetime
import webbrowser
from pathlib import Path

class UltraOS:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("UltraOS")
        self.root.geometry("1200x800")
        self.root.configure(bg="#0a0a0a")
        
        # Variables système
        self.current_user = "user"
        self.system_time = datetime.now()
        self.running_apps = []
        self.desktop_files = []
        
        # Style moderne
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.configure_modern_style()
        
        # Création de l'interface
        self.create_desktop()
        self.create_taskbar()
        self.create_start_menu()
        
        # Démarrer le système
        self.start_system_clock()
        
    def configure_modern_style(self):
        """Configure un style moderne sombre"""
        self.style.configure('Modern.TFrame', background='#1a1a1a', relief='flat')
        self.style.configure('Modern.TButton', 
                           background='#2d2d2d', 
                           foreground='white',
                           borderwidth=0,
                           focuscolor='none')
        self.style.map('Modern.TButton',
                      background=[('active', '#404040')])
        
    def create_desktop(self):
        """Crée le bureau avec fond moderne"""
        self.desktop = tk.Frame(self.root, bg="#0a0a0a")
        self.desktop.pack(fill=tk.BOTH, expand=True)
        
        # Titre du système
        title = tk.Label(self.desktop, text="UltraOS", 
                        font=("Arial", 48, "bold"),
                        fg="#00ff88", bg="#0a0a0a")
        title.place(relx=0.5, rely=0.1, anchor="center")
        
        # Icônes du bureau
        self.create_desktop_icons()
        
    def create_desktop_icons(self):
        """Crée les icônes sur le bureau"""
        icons = [
            ("📁 Gestionnaire", self.open_file_manager, 100, 200),
            ("💻 Terminal", self.open_terminal, 100, 300),
            ("📝 Editeur", self.open_text_editor, 100, 400),
            ("🌐 Navigateur", self.open_browser, 100, 500),
            ("⚙️ Paramètres", self.open_settings, 250, 200),
            ("📊 Moniteur", self.open_system_monitor, 250, 300),
            ("🎵 Lecteur", self.open_media_player, 250, 400),
            ("🔧 Utilitaires", self.open_utilities, 250, 500),
        ]
        
        for text, command, x, y in icons:
            btn = tk.Button(self.desktop, text=text,
                          command=command,
                          bg="#2d2d2d", fg="white",
                          font=("Arial", 10, "bold"),
                          width=12, height=2,
                          relief="flat", bd=0)
            btn.place(x=x, y=y)
            
    def create_taskbar(self):
        """Crée la barre des tâches moderne"""
        self.taskbar = tk.Frame(self.root, bg="#1a1a1a", height=40)
        self.taskbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.taskbar.pack_propagate(False)
        
        # Bouton démarrer
        self.start_btn = tk.Button(self.taskbar, text="⚡ Start",
                                 command=self.toggle_start_menu,
                                 bg="#00ff88", fg="black",
                                 font=("Arial", 10, "bold"),
                                 relief="flat", bd=0)
        self.start_btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Zone des applications ouvertes
        self.app_frame = tk.Frame(self.taskbar, bg="#1a1a1a")
        self.app_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Horloge système
        self.clock_label = tk.Label(self.taskbar, text="",
                                  bg="#1a1a1a", fg="white",
                                  font=("Arial", 10))
        self.clock_label.pack(side=tk.RIGHT, padx=10, pady=5)
        
    def create_start_menu(self):
        """Crée le menu démarrer moderne"""
        self.start_menu = tk.Toplevel(self.root)
        self.start_menu.title("Menu Démarrer")
        self.start_menu.geometry("300x400")
        self.start_menu.configure(bg="#1a1a1a")
        self.start_menu.withdraw()
        self.start_menu.overrideredirect(True)
        
        # Applications dans le menu
        apps = [
            "📁 Gestionnaire de fichiers", "💻 Terminal", "📝 Éditeur de texte",
            "🌐 Navigateur web", "⚙️ Paramètres système", "📊 Moniteur système",
            "🎵 Lecteur multimédia", "🔧 Utilitaires", "📷 Capture d'écran",
            "🔍 Recherche", "📧 Messages", "🎮 Jeux"
        ]
        
        for i, app in enumerate(apps):
            btn = tk.Button(self.start_menu, text=app,
                          command=lambda a=app: self.launch_app(a),
                          bg="#2d2d2d", fg="white",
                          font=("Arial", 10),
                          relief="flat", bd=0,
                          anchor="w")
            btn.pack(fill=tk.X, padx=5, pady=2)
            
    def start_system_clock(self):
        """Démarre l'horloge système"""
        def update_clock():
            while True:
                current_time = datetime.now().strftime("%H:%M:%S")
                self.clock_label.config(text=current_time)
                time.sleep(1)
                
        clock_thread = threading.Thread(target=update_clock, daemon=True)
        clock_thread.start()
        
    def toggle_start_menu(self):
        """Affiche/cache le menu démarrer"""
        if self.start_menu.winfo_viewable():
            self.start_menu.withdraw()
        else:
            # Position du menu
            x = self.root.winfo_x() + 10
            y = self.root.winfo_y() + self.root.winfo_height() - 450
            self.start_menu.geometry(f"300x400+{x}+{y}")
            self.start_menu.deiconify()
            
    def launch_app(self, app_name):
        """Lance une application depuis le menu"""
        self.start_menu.withdraw()
        if "Gestionnaire" in app_name:
            self.open_file_manager()
        elif "Terminal" in app_name:
            self.open_terminal()
        elif "Éditeur" in app_name:
            self.open_text_editor()
        elif "Navigateur" in app_name:
            self.open_browser()
        elif "Paramètres" in app_name:
            self.open_settings()
        elif "Moniteur" in app_name:
            self.open_system_monitor()
        elif "Lecteur" in app_name:
            self.open_media_player()
        elif "Utilitaires" in app_name:
            self.open_utilities()
            
    def open_file_manager(self):
        """Ouvre le gestionnaire de fichiers moderne"""
        fm_window = tk.Toplevel(self.root)
        fm_window.title("Gestionnaire de fichiers - UltraOS")
        fm_window.geometry("800x600")
        fm_window.configure(bg="#1a1a1a")
        
        # Barre d'outils
        toolbar = tk.Frame(fm_window, bg="#2d2d2d", height=40)
        toolbar.pack(fill=tk.X)
        toolbar.pack_propagate(False)
        
        tk.Button(toolbar, text="← Retour", bg="#404040", fg="white",
                 relief="flat", bd=0).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(toolbar, text="↻ Actualiser", bg="#404040", fg="white",
                 relief="flat", bd=0).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(toolbar, text="📁 Nouveau dossier", bg="#404040", fg="white",
                 relief="flat", bd=0).pack(side=tk.LEFT, padx=5, pady=5)
        
        # Chemin actuel
        path_var = tk.StringVar(value=os.getcwd())
        path_entry = tk.Entry(toolbar, textvariable=path_var,
                            bg="#404040", fg="white", relief="flat")
        path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)
        
        # Liste des fichiers
        file_frame = tk.Frame(fm_window, bg="#1a1a1a")
        file_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Treeview pour les fichiers
        columns = ("Nom", "Taille", "Type", "Modifié")
        tree = ttk.Treeview(file_frame, columns=columns, show="tree headings")
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)
            
        tree.pack(fill=tk.BOTH, expand=True)
        
        # Charger les fichiers du répertoire courant
        self.load_directory(tree, os.getcwd())
        
    def load_directory(self, tree, path):
        """Charge les fichiers d'un répertoire"""
        tree.delete(*tree.get_children())
        
        try:
            for item in os.listdir(path):
                item_path = os.path.join(path, item)
                if os.path.isdir(item_path):
                    icon = "📁"
                    size = "Dossier"
                    type_file = "Dossier"
                else:
                    icon = "📄"
                    size = f"{os.path.getsize(item_path)} bytes"
                    type_file = item.split('.')[-1] if '.' in item else "Fichier"
                
                modified = datetime.fromtimestamp(os.path.getmtime(item_path)).strftime("%d/%m/%Y %H:%M")
                
                tree.insert("", "end", text=f"{icon} {item}",
                          values=(item, size, type_file, modified))
        except PermissionError:
            messagebox.showerror("Erreur", "Accès refusé au répertoire")
            
    def open_terminal(self):
        """Ouvre un terminal moderne"""
        term_window = tk.Toplevel(self.root)
        term_window.title("Terminal - UltraOS")
        term_window.geometry("800x500")
        term_window.configure(bg="#0a0a0a")
        
        # Zone de texte pour le terminal
        terminal_text = scrolledtext.ScrolledText(
            term_window,
            bg="#0a0a0a", fg="#00ff88",
            font=("Consolas", 11),
            insertbackground="white"
        )
        terminal_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Prompt initial
        terminal_text.insert(tk.END, f"UltraOS Terminal v1.0\n")
        terminal_text.insert(tk.END, f"Utilisateur: {self.current_user}\n")
        terminal_text.insert(tk.END, f"Répertoire: {os.getcwd()}\n\n")
        terminal_text.insert(tk.END, f"{self.current_user}@ultraos:~$ ")
        
        def execute_command(event):
            # Récupérer la commande
            line = terminal_text.get("end-2l linestart", "end-1c")
            command = line.split("$ ")[-1].strip()
            
            if command:
                terminal_text.insert(tk.END, f"\n")
                
                # Commandes intégrées
                if command == "clear":
                    terminal_text.delete(1.0, tk.END)
                elif command == "help":
                    help_text = """
Commandes disponibles:
- ls : Lister les fichiers
- pwd : Répertoire courant
- date : Date et heure
- whoami : Utilisateur actuel
- clear : Effacer l'écran
- exit : Fermer le terminal
- help : Afficher cette aide
"""
                    terminal_text.insert(tk.END, help_text)
                elif command == "ls":
                    try:
                        files = os.listdir(".")
                        for f in files:
                            terminal_text.insert(tk.END, f"{f}\n")
                    except Exception as e:
                        terminal_text.insert(tk.END, f"Erreur: {e}\n")
                elif command == "pwd":
                    terminal_text.insert(tk.END, f"{os.getcwd()}\n")
                elif command == "date":
                    terminal_text.insert(tk.END, f"{datetime.now()}\n")
                elif command == "whoami":
                    terminal_text.insert(tk.END, f"{self.current_user}\n")
                elif command == "exit":
                    term_window.destroy()
                    return
                else:
                    # Essayer d'exécuter la commande système
                    try:
                        result = subprocess.run(command, shell=True, 
                                              capture_output=True, text=True)
                        if result.stdout:
                            terminal_text.insert(tk.END, result.stdout)
                        if result.stderr:
                            terminal_text.insert(tk.END, f"Erreur: {result.stderr}")
                    except Exception as e:
                        terminal_text.insert(tk.END, f"Commande non reconnue: {command}\n")
                
                terminal_text.insert(tk.END, f"{self.current_user}@ultraos:~$ ")
                terminal_text.see(tk.END)
            
            return "break"
        
        terminal_text.bind("<Return>", execute_command)
        terminal_text.focus()
        
    def open_text_editor(self):
        """Ouvre un éditeur de texte moderne"""
        editor_window = tk.Toplevel(self.root)
        editor_window.title("Éditeur de texte - UltraOS")
        editor_window.geometry("900x700")
        editor_window.configure(bg="#1a1a1a")
        
        # Menu
        menubar = tk.Menu(editor_window)
        editor_window.config(menu=menubar)
        
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Fichier", menu=file_menu)
        
        # Zone de texte
        text_editor = scrolledtext.ScrolledText(
            editor_window,
            bg="#1a1a1a", fg="white",
            font=("Consolas", 12),
            insertbackground="white",
            selectbackground="#404040"
        )
        text_editor.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        def new_file():
            text_editor.delete(1.0, tk.END)
            
        def open_file():
            file_path = filedialog.askopenfilename()
            if file_path:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        text_editor.delete(1.0, tk.END)
                        text_editor.insert(1.0, content)
                except Exception as e:
                    messagebox.showerror("Erreur", f"Impossible d'ouvrir le fichier: {e}")
                    
        def save_file():
            file_path = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Fichiers texte", "*.txt"), ("Tous les fichiers", "*.*")]
            )
            if file_path:
                try:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(text_editor.get(1.0, tk.END))
                    messagebox.showinfo("Succès", "Fichier sauvegardé!")
                except Exception as e:
                    messagebox.showerror("Erreur", f"Impossible de sauvegarder: {e}")
        
        file_menu.add_command(label="Nouveau", command=new_file)
        file_menu.add_command(label="Ouvrir", command=open_file)
        file_menu.add_command(label="Sauvegarder", command=save_file)
        file_menu.add_separator()
        file_menu.add_command(label="Fermer", command=editor_window.destroy)
        
    def open_browser(self):
        """Ouvre un navigateur web simple"""
        browser_window = tk.Toplevel(self.root)
        browser_window.title("Navigateur Web - UltraOS")
        browser_window.geometry("1000x700")
        browser_window.configure(bg="#1a1a1a")
        
        # Barre d'adresse
        addr_frame = tk.Frame(browser_window, bg="#2d2d2d", height=50)
        addr_frame.pack(fill=tk.X)
        addr_frame.pack_propagate(False)
        
        tk.Button(addr_frame, text="←", bg="#404040", fg="white",
                 relief="flat", bd=0, width=3).pack(side=tk.LEFT, padx=5, pady=10)
        tk.Button(addr_frame, text="→", bg="#404040", fg="white",
                 relief="flat", bd=0, width=3).pack(side=tk.LEFT, padx=5, pady=10)
        tk.Button(addr_frame, text="↻", bg="#404040", fg="white",
                 relief="flat", bd=0, width=3).pack(side=tk.LEFT, padx=5, pady=10)
        
        url_var = tk.StringVar(value="https://www.google.com")
        url_entry = tk.Entry(addr_frame, textvariable=url_var,
                           bg="#404040", fg="white", relief="flat",
                           font=("Arial", 11))
        url_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=10)
        
        def go_to_url():
            url = url_var.get()
            if url:
                try:
                    webbrowser.open(url)
                    messagebox.showinfo("Navigateur", f"Ouverture de {url} dans le navigateur par défaut")
                except Exception as e:
                    messagebox.showerror("Erreur", f"Impossible d'ouvrir l'URL: {e}")
        
        tk.Button(addr_frame, text="Aller", command=go_to_url,
                 bg="#00ff88", fg="black", relief="flat", bd=0).pack(side=tk.RIGHT, padx=5, pady=10)
        
        # Zone de contenu
        content_frame = tk.Frame(browser_window, bg="#1a1a1a")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        welcome_text = """
        🌐 Navigateur UltraOS
        
        Fonctionnalités:
        • Navigation web basique
        • Favoris
        • Historique
        • Mode sombre
        
        Saisissez une URL dans la barre d'adresse pour naviguer.
        """
        
        tk.Label(content_frame, text=welcome_text,
                bg="#1a1a1a", fg="white",
                font=("Arial", 14), justify=tk.LEFT).pack(pady=50)
        
    def open_settings(self):
        """Ouvre les paramètres système"""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Paramètres - UltraOS")
        settings_window.geometry("700x500")
        settings_window.configure(bg="#1a1a1a")
        
        # Notebook pour les onglets
        notebook = ttk.Notebook(settings_window)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Onglet Système
        system_frame = tk.Frame(notebook, bg="#1a1a1a")
        notebook.add(system_frame, text="Système")
        
        tk.Label(system_frame, text="Informations Système",
                font=("Arial", 16, "bold"), bg="#1a1a1a", fg="#00ff88").pack(pady=10)
        
        info_text = f"""
        OS: UltraOS v1.0
        Utilisateur: {self.current_user}
        Plateforme: {sys.platform}
        Version Python: {sys.version}
        Répertoire: {os.getcwd()}
        """
        
        tk.Label(system_frame, text=info_text,
                bg="#1a1a1a", fg="white", justify=tk.LEFT).pack(pady=10)
        
        # Onglet Apparence
        appearance_frame = tk.Frame(notebook, bg="#1a1a1a")
        notebook.add(appearance_frame, text="Apparence")
        
        tk.Label(appearance_frame, text="Thème: Mode Sombre",
                bg="#1a1a1a", fg="white").pack(pady=20)
        
        # Onglet Réseau
        network_frame = tk.Frame(notebook, bg="#1a1a1a")
        notebook.add(network_frame, text="Réseau")
        
        tk.Label(network_frame, text="Configuration Réseau",
                bg="#1a1a1a", fg="white").pack(pady=20)
        
    def open_system_monitor(self):
        """Ouvre le moniteur système"""
        monitor_window = tk.Toplevel(self.root)
        monitor_window.title("Moniteur Système - UltraOS")
        monitor_window.geometry("800x600")
        monitor_window.configure(bg="#1a1a1a")
        
        # Informations système en temps réel
        info_frame = tk.Frame(monitor_window, bg="#1a1a1a")
        info_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        tk.Label(info_frame, text="Moniteur Système",
                font=("Arial", 18, "bold"), bg="#1a1a1a", fg="#00ff88").pack(pady=10)
        
        # CPU Usage (simulé)
        cpu_frame = tk.Frame(info_frame, bg="#2d2d2d")
        cpu_frame.pack(fill=tk.X, pady=5)
        tk.Label(cpu_frame, text="CPU: 35%", bg="#2d2d2d", fg="white").pack(side=tk.LEFT, padx=10, pady=5)
        
        # Memory Usage (simulé)
        mem_frame = tk.Frame(info_frame, bg="#2d2d2d")
        mem_frame.pack(fill=tk.X, pady=5)
        tk.Label(mem_frame, text="Mémoire: 60%", bg="#2d2d2d", fg="white").pack(side=tk.LEFT, padx=10, pady=5)
        
        # Processus
        proc_frame = tk.Frame(info_frame, bg="#1a1a1a")
        proc_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        tk.Label(proc_frame, text="Processus actifs:",
                bg="#1a1a1a", fg="white", font=("Arial", 12, "bold")).pack()
        
        processes = ["UltraOS", "Gestionnaire", "Terminal", "Éditeur"]
        for proc in processes:
            tk.Label(proc_frame, text=f"• {proc}",
                    bg="#1a1a1a", fg="white").pack(anchor="w", padx=20)
    
    def open_media_player(self):
        """Ouvre le lecteur multimédia"""
        player_window = tk.Toplevel(self.root)
        player_window.title("Lecteur Multimédia - UltraOS")
        player_window.geometry("600x400")
        player_window.configure(bg="#1a1a1a")
        
        tk.Label(player_window, text="🎵 Lecteur Multimédia",
                font=("Arial", 18, "bold"), bg="#1a1a1a", fg="#00ff88").pack(pady=20)
        
        # Contrôles
        controls = tk.Frame(player_window, bg="#1a1a1a")
        controls.pack(pady=20)
        
        tk.Button(controls, text="⏮", bg="#2d2d2d", fg="white",
                 font=("Arial", 16), relief="flat", bd=0, width=3).pack(side=tk.LEFT, padx=5)
        tk.Button(controls, text="⏯", bg="#00ff88", fg="black",
                 font=("Arial", 16), relief="flat", bd=0, width=3).pack(side=tk.LEFT, padx=5)
        tk.Button(controls, text="⏭", bg="#2d2d2d", fg="white",
                 font=("Arial", 16), relief="flat", bd=0, width=3).pack(side=tk.LEFT, padx=5)
        
    def open_utilities(self):
        """Ouvre les utilitaires système"""
        util_window = tk.Toplevel(self.root)
        util_window.title("Utilitaires - UltraOS")
        util_window.geometry("500x400")
        util_window.configure(bg="#1a1a1a")
        
        tk.Label(util_window, text="🔧 Utilitaires Système",
                font=("Arial", 18, "bold"), bg="#1a1a1a", fg="#00ff88").pack(pady=20)
        
        utilities = [
            ("📷 Capture d'écran", lambda: messagebox.showinfo("Capture", "Capture d'écran prise!")),
            ("🧹 Nettoyage disque", lambda: messagebox.showinfo("Nettoyage", "Nettoyage terminé!")),
            ("🔍 Recherche de fichiers", lambda: messagebox.showinfo("Recherche", "Fonction de recherche")),
            ("⚡ Optimisation système", lambda: messagebox.showinfo("Optimisation", "Système optimisé!")),
        ]
        
        for text, command in utilities:
            tk.Button(util_window, text=text, command=command,
                     bg="#2d2d2d", fg="white", font=("Arial", 12),
                     relief="flat", bd=0, width=25, height=2).pack(pady=10)
    
    def run(self):
        """Démarre l'OS"""
        print("🚀 Démarrage d'UltraOS...")
        print("✅ Système initialisé")
        self.root.mainloop()

def main():
    """Point d'entrée principal"""
    print("=" * 50)
    print("  UltraOS - Système d'Exploitation Moderne")
    print("  Développé en Python")
    print("=" * 50)
    
    try:
        os_instance = UltraOS()
        os_instance.run()
    except KeyboardInterrupt:
        print("\n🛑 Arrêt d'UltraOS")
    except Exception as e:
        print(f"❌ Erreur critique: {e}")
    finally:
        print("👋 UltraOS fermé")

if __name__ == "__main__":
    main()
