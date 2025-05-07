import tkinter as tk
from tkinter import filedialog, messagebox
import tempfile
import shutil
import os
import subprocess

def select_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        folder_label.config(text=f"Selected Folder: {folder_path}")
        return folder_path
    else:
        folder_label.config(text="No folder selected")
        return None

def build_installer():
    if folder_label.cget("text").startswith("Selected Folder:"):
        folder_path = folder_label.cget("text").replace("Selected Folder: ", "")
        installer_name = os.path.basename(folder_path) + "_installer"
        output_path = os.path.join(os.path.expanduser("~"), "Desktop", installer_name + ".exe")

        try:
            # Inno Setup script content
            iss_script = f"""
[Setup]
AppName={os.path.basename(folder_path)}
AppVersion=1.0
DefaultDirName={{pf}}\\{os.path.basename(folder_path)}
OutputBaseFilename={installer_name}
DefaultGroupName={os.path.basename(folder_path)}
OutputDir={os.path.expanduser("~")}\\Desktop

[Files]
Source: "{folder_path}\\*"; DestDir: "{{app}}"; Flags: recursesubdirs createallsubdirs
"""

            # Write the .iss script to a temp file
            iss_file = os.path.join(tempfile.gettempdir(), "installer_script.iss")
            with open(iss_file, "w") as f:
                f.write(iss_script)

            # Run Inno Setup Compiler
            iscc_path = r"C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
            if not os.path.isfile(iscc_path):
                messagebox.showerror("Error", f"ISCC.exe not found at:\n{iscc_path}")
                return

            subprocess.run([iscc_path, iss_file], check=True)

            messagebox.showinfo("Success", f"Installer created on your desktop:\n{output_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create installer:\n{str(e)}")
    else:
        messagebox.showwarning("Warning", "Please select a folder first!")

def main():
    root = tk.Tk()
    root.title("Installer Maker")
    root.geometry("500x300")

    label = tk.Label(root, text="Welcome to Installer Maker!", font=("Arial", 16))
    label.pack(pady=10)

    select_button = tk.Button(root, text="Select Folder", command=select_folder)
    select_button.pack(pady=10)

    global folder_label
    folder_label = tk.Label(root, text="No folder selected", font=("Arial", 12))
    folder_label.pack(pady=10)

    build_button = tk.Button(root, text="Build Installer", command=build_installer)
    build_button.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    while True:
        try:
            main()
            break
        except FileNotFoundError as e:
            print(f"File not found: {e}. Retrying...")
