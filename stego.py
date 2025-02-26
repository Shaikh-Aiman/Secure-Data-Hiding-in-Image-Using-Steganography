import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import cv2
import numpy as np
import os

class SteganographyApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Secure Data Hiding in Images - Steganography")
        self.geometry("600x400")
        self.resizable(False, False)
        
        # Create tabbed interface
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True)
        
        self.create_encrypt_tab()
        self.create_decrypt_tab()

    def create_encrypt_tab(self):
        self.encrypt_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.encrypt_frame, text="Encrypt")

        # Make columns 0, 1, and 2 expand equally
        self.encrypt_frame.grid_columnconfigure(0, weight=1)
        self.encrypt_frame.grid_columnconfigure(1, weight=1)
        self.encrypt_frame.grid_columnconfigure(2, weight=1)

        # --- File Selection ---
        ttk.Label(self.encrypt_frame, text="Select Image File:").grid(
            row=0, column=0, padx=10, pady=10, sticky="w"
        )
        self.encrypt_image_path = tk.StringVar()
        self.encrypt_image_entry = ttk.Entry(
            self.encrypt_frame, textvariable=self.encrypt_image_path, width=50
        )
        self.encrypt_image_entry.grid(row=0, column=1, padx=10, pady=10)
        ttk.Button(self.encrypt_frame, text="Browse", command=self.browse_encrypt_image).grid(
            row=0, column=2, padx=10, pady=10
        )

        # --- Secret Message Input ---
        ttk.Label(self.encrypt_frame, text="Enter Secret Message:").grid(
            row=1, column=0, padx=10, pady=10, sticky="w"
        )
        self.secret_message = tk.StringVar()
        self.message_entry = ttk.Entry(
            self.encrypt_frame, textvariable=self.secret_message, width=50
        )
        self.message_entry.grid(row=1, column=1, padx=10, pady=10)

        # --- Passcode Input ---
        ttk.Label(self.encrypt_frame, text="Enter Passcode:").grid(
            row=2, column=0, padx=10, pady=10, sticky="w"
        )
        self.encrypt_password = tk.StringVar()
        self.password_entry = ttk.Entry(
            self.encrypt_frame, textvariable=self.encrypt_password, width=50, show="*"
        )
        self.password_entry.grid(row=2, column=1, padx=10, pady=10)

        # --- Encrypt Button (centered) ---
        ttk.Button(self.encrypt_frame, text="Encrypt Image", command=self.encrypt_image).grid(
            row=3, column=1, padx=10, pady=20, sticky="ew"
        )

    def create_decrypt_tab(self):
        self.decrypt_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.decrypt_frame, text="Decrypt")

        # Make columns 0, 1, and 2 expand equally
        self.decrypt_frame.grid_columnconfigure(0, weight=1)
        self.decrypt_frame.grid_columnconfigure(1, weight=1)
        self.decrypt_frame.grid_columnconfigure(2, weight=1)

        # --- Encrypted File Selection ---
        ttk.Label(self.decrypt_frame, text="Select Encrypted Image File:").grid(
            row=0, column=0, padx=10, pady=10, sticky="w"
        )
        self.decrypt_image_path = tk.StringVar()
        self.decrypt_image_entry = ttk.Entry(
            self.decrypt_frame, textvariable=self.decrypt_image_path, width=50
        )
        self.decrypt_image_entry.grid(row=0, column=1, padx=10, pady=10)
        ttk.Button(self.decrypt_frame, text="Browse", command=self.browse_decrypt_image).grid(
            row=0, column=2, padx=10, pady=10
        )

        # --- Passcode Input for Decryption ---
        ttk.Label(self.decrypt_frame, text="Enter Passcode:").grid(
            row=1, column=0, padx=10, pady=10, sticky="w"
        )
        self.decrypt_password = tk.StringVar()
        self.decrypt_password_entry = ttk.Entry(
            self.decrypt_frame, textvariable=self.decrypt_password, width=50, show="*"
        )
        self.decrypt_password_entry.grid(row=1, column=1, padx=10, pady=10)

        # --- Decrypt Button (centered) ---
        ttk.Button(self.decrypt_frame, text="Decrypt Image", command=self.decrypt_image).grid(
            row=2, column=1, padx=10, pady=20, sticky="ew"
        )

    # --- File Browsing Methods ---
    def browse_encrypt_image(self):
        file_path = filedialog.askopenfilename(
            title="Select Image File", 
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp"), ("All Files", "*.*")]
        )
        if file_path:
            self.encrypt_image_path.set(file_path)

    def browse_decrypt_image(self):
        file_path = filedialog.askopenfilename(
            title="Select Encrypted Image File", 
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp"), ("All Files", "*.*")]
        )
        if file_path:
            self.decrypt_image_path.set(file_path)

    # --- Encryption Logic ---
    def encrypt_image(self):
        image_path = self.encrypt_image_path.get()
        message = self.secret_message.get()
        password = self.encrypt_password.get()

        if not image_path or not message or not password:
            messagebox.showwarning("Input Error", "Please fill in all fields.")
            return

        img = cv2.imread(image_path)
        if img is None:
            messagebox.showerror("Error", "Selected image file could not be read.")
            return

        # Auto-generate output file name in the same folder with "_encrypted" appended
        directory, filename = os.path.split(image_path)
        name, _ = os.path.splitext(filename)
        output_filename = f"{name}_encrypted.png"
        output_path = os.path.join(directory, output_filename)

        n, m, z = 0, 0, 0

        # Embed lengths of password and message
        img[n, m, z] = np.uint8(len(password))
        img[n+1, m+1, (z+1)%3] = np.uint8(len(message))
        n += 2
        m += 2
        z = (z+2) % 3

        # Embed password + message
        for char in password + message:
            img[n, m, z] = np.uint8(ord(char))
            n += 1
            m += 1
            z = (z+1) % 3

        try:
            cv2.imwrite(output_path, img)
            messagebox.showinfo("Success", f"Image encrypted successfully!\nSaved as:\n{output_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save encrypted image.\n{e}")

    # --- Decryption Logic ---
    def decrypt_image(self):
        image_path = self.decrypt_image_path.get()
        password_attempt = self.decrypt_password.get()

        if not image_path or not password_attempt:
            messagebox.showwarning("Input Error", "Please select an image and enter the passcode.")
            return

        img = cv2.imread(image_path)
        if img is None:
            messagebox.showerror("Error", "Selected image file could not be read.")
            return

        try:
            # Retrieve stored lengths
            password_length = int(img[0, 0, 0])
            message_length = int(img[1, 1, (0+1)%3])
            total_chars = password_length + message_length

            # Check if total_chars fits into the diagonal
            h, w, _ = img.shape
            available_steps = min(h, w) - 2
            if total_chars > available_steps:
                messagebox.showerror("Error", "The selected image does not appear to have any hidden message.")
                return

            n, m, z = 2, 2, (0+2)%3

            # Extract password
            extracted_password = ""
            for _ in range(password_length):
                extracted_password += chr(int(img[n, m, z]))
                n += 1
                m += 1
                z = (z+1) % 3

            # Validate password
            if extracted_password != password_attempt:
                messagebox.showerror("Error", "Incorrect passcode! Decryption failed.")
                return

            # Extract hidden message
            message = ""
            for _ in range(message_length):
                message += chr(int(img[n, m, z]))
                n += 1
                m += 1
                z = (z+1) % 3

            messagebox.showinfo("Decrypted Message", f"Secret Message:\n{message}")

        except Exception:
            messagebox.showerror("Error", "The selected image does not appear to have hidden data.")

if __name__ == "__main__":
    app = SteganographyApp()
    app.mainloop()
