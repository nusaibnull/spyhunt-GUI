import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import shutil
import re # Regular expression library

# --- ★ Banner Removal Function ★ ---
def remove_banner_print(filepath):
    """
    Finds the banner print statement in a Python file and comments it out.
    Creates a backup first.
    """
    if not filepath or not os.path.exists(filepath):
        messagebox.showerror("Error", "File not selected or not found.")
        return

    backup_path = filepath + ".bak"
    banner_print_pattern = re.compile(r"^\s*print\(.*\+\s*banner\)") # Regex to find the print line

    try:
        # 1. Create backup
        shutil.copy2(filepath, backup_path)
        status_label.config(text=f"Backup created: {os.path.basename(backup_path)}")
        root.update_idletasks()

        # 2. Read lines and find the banner print line
        lines = []
        found = False
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f_in:
            lines = f_in.readlines()

        modified_lines = []
        for line in lines:
            if not found and banner_print_pattern.match(line):
                modified_lines.append("# " + line) # Comment out the line
                found = True
                status_label.config(text="Banner print statement found and commented out.")
                root.update_idletasks()
            else:
                modified_lines.append(line)

        if not found:
             status_label.config(text="Banner print statement not found. No changes made.")
             messagebox.showwarning("Not Found", "Could not find the banner print line (print(... + banner)).\nNo changes were made.")
             # Optionally remove the backup if nothing was changed
             try: os.remove(backup_path)
             except OSError: pass
             return

        # 3. Write back the modified content using UTF-8
        with open(filepath, 'w', encoding='utf-8') as f_out:
            f_out.writelines(modified_lines)

        status_label.config(text="Banner print statement successfully commented out!")
        messagebox.showinfo("Success", f"Banner print statement commented out in:\n{os.path.basename(filepath)}\n\nBackup saved as:\n{os.path.basename(backup_path)}")

    except Exception as e:
        status_label.config(text=f"Error: {e}")
        messagebox.showerror("Error", f"Failed to modify file:\n{e}\n\nBackup was created at:\n{backup_path}")


# --- ★ GUI Functions ★ ---

def browse_file_gui():
    """Opens file dialog and updates entry."""
    filepath = filedialog.askopenfilename(
        title="Select spyhunt.py (or similar script)",
        filetypes=(("Python files", "*.py"), ("All files", "*.*"))
    )
    if filepath:
        file_path_entry.delete(0, tk.END)
        file_path_entry.insert(0, filepath)
        status_label.config(text="File selected. Ready to patch.")

def start_patching():
    """Gets file path from entry and starts patching."""
    filepath = file_path_entry.get()
    remove_banner_print(filepath)


# --- ★ GUI Setup ★ ---
root = tk.Tk()
root.title("Banner Print Remover Tool")
root.geometry("600x180")

# --- Styles ---
style = ttk.Style()
style.theme_use('clam')
BG_COLOR="#2E2E2E"; FG_COLOR="#E0E0E0"; FIELD_BG="#3E3E3E"; ACTIVE_BG="#4A4A4A"
BTN_COLOR = "#0078D4"; BTN_ACTIVE = "#005BA1"

style.configure('.', background=BG_COLOR, foreground=FG_COLOR, fieldbackground=FIELD_BG)
style.map('.', background=[('active', ACTIVE_BG)])
style.configure('TFrame', background=BG_COLOR)
style.configure('TLabel', background=BG_COLOR, foreground=FG_COLOR)
style.configure('TButton', background=BTN_COLOR, foreground='white', font=('Arial', 10, 'bold'), padding=5)
style.map('TButton', background=[('active', BTN_ACTIVE)])
style.configure('TEntry', fieldbackground=FIELD_BG, foreground=FG_COLOR, insertcolor=FG_COLOR)
root.configure(bg=BG_COLOR)

# --- Main Frame ---
main_frame = ttk.Frame(root, padding="15")
main_frame.pack(fill=tk.BOTH, expand=True)
main_frame.columnconfigure(1, weight=1) # Make entry expand

# File Selection Row
ttk.Label(main_frame, text="Python File:").grid(row=0, column=0, padx=(0, 10), pady=10, sticky=tk.W)
file_path_entry = ttk.Entry(main_frame, width=50)
file_path_entry.grid(row=0, column=1, padx=(0, 5), pady=10, sticky=tk.EW)
browse_button = ttk.Button(main_frame, text="Browse...", command=browse_file_gui)
browse_button.grid(row=0, column=2, pady=10)

# Patch Button Row
patch_button = ttk.Button(main_frame, text="Remove Banner Print (with Backup)", command=start_patching)
patch_button.grid(row=1, column=0, columnspan=3, pady=10, ipady=5)

# Status Label Row
status_label = ttk.Label(main_frame, text="Select the Python file containing the banner...", wraplength=550)
status_label.grid(row=2, column=0, columnspan=3, pady=(10, 0), sticky=tk.W)

# --- Start GUI ---
root.mainloop()