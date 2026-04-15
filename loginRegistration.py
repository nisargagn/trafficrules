import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os

CSV_FILE = "users.csv"

# Utility functions
def save_user_to_csv(username, password):
    with open(CSV_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([username, password])

def validate_user_from_csv(username, password):
    if not os.path.exists(CSV_FILE):
        return False
    with open(CSV_FILE, mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row == [username, password]:
                return True
    return False

# Custom styled button with hover effect
class HoverButton(ttk.Button):
    def __init__(self, master=None, **kw):
        ttk.Button.__init__(self, master=master, **kw)
        self.default_style = "TButton"
        self.hover_style = "Hover.TButton"
        self.style = ttk.Style()
        self.style.configure(self.default_style, font=("Helvetica", 12, "bold"),
                             background="#4a7a8c", foreground="blue", borderwidth=0, focusthickness=3, focuscolor='none')
        self.style.map(self.default_style,
                       background=[('active', '#648d9f')])
        self.configure(style=self.default_style)
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
    def on_enter(self, e):
        self.configure(style=self.hover_style)
        self.style.configure(self.hover_style, background="#648d9f")
    def on_leave(self, e):
        self.configure(style=self.default_style)

# Main app class
class AuthApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Colorful Auth System")
        self.geometry("500x450")
        self.resizable(True, True)
        self.configure(bg="#e3f2fd") # Very light blue background

        # Container for frames
        self.login_frame = LoginFrame(self)
        self.register_frame = RegisterFrame(self)

        self.login_frame.pack(fill="both", expand=True)

    def switch_to_register(self):
        self.login_frame.pack_forget()
        self.register_frame.pack(fill="both", expand=True)

    def switch_to_login(self):
        self.register_frame.pack_forget()
        self.login_frame.pack(fill="both", expand=True)

# Base frame style with padding and rounded corners effect (simulated)
class StyledFrame(tk.Frame):
    def __init__(self, master=None, bg_color="#ffffff", **kwargs):
        super().__init__(master, bg=bg_color, **kwargs)
        self.config(borderwidth=0, highlightthickness=0)
        self['padx'] = 30
        self['pady'] = 30

class LoginFrame(StyledFrame):
    def __init__(self, master):
        super().__init__(master, bg_color="#6ec1e4") # Gradient blue alternative
        self.master = master
        self.create_widgets()

    def create_widgets(self):
        # Title
        tk.Label(self, text="Login", font=("Helvetica", 26, "bold"),
                 bg="#6ec1e4", fg="#ffffff").pack(pady=(10, 20))

        # Username Entry
        self.username = ttk.Entry(self, font=("Arial", 14), width=30)
        self.username.pack(pady=10)
        self.username.insert(0, "Username")
        self.username.config(foreground="gray")
        self.username.bind("<FocusIn>", self.clear_username_placeholder)
        self.username.bind("<FocusOut>", self.restore_username_placeholder)

        # Password Entry
        self.password = ttk.Entry(self, font=("Arial", 14), width=30, show="")
        self.password.pack(pady=10)
        self.password.insert(0, "Password")
        self.password.config(foreground="gray")
        self.password.bind("<FocusIn>", self.clear_password_placeholder)
        self.password.bind("<FocusOut>", self.restore_password_placeholder)

        # Login Button
        login_btn = HoverButton(self, text="Login", command=self.login_user)
        login_btn.pack(pady=15, ipadx=10, ipady=5)

        # Go to Register Button
        switch_btn = ttk.Button(self, text="Go to Register", command=self.master.switch_to_register,
                                style="Link.TButton")
        switch_btn.pack(pady=5)

        # Style for link button
        style = ttk.Style()
        style.configure("Link.TButton", foreground="#ffffff", background="#6ec1e4",
                        font=("Arial", 10, "underline"), borderwidth=0)
        style.map("Link.TButton",
                  foreground=[('active', '#d0ebff')])

    def clear_username_placeholder(self, event):
        if self.username.get() == "Username":
            self.username.delete(0, tk.END)
            self.username.config(foreground="black")

    def restore_username_placeholder(self, event):
        if not self.username.get():
            self.username.insert(0, "Username")
            self.username.config(foreground="gray")

    def clear_password_placeholder(self, event):
        if self.password.get() == "Password":
            self.password.delete(0, tk.END)
            self.password.config(show="*", foreground="black")

    def restore_password_placeholder(self, event):
        if not self.password.get():
            self.password.insert(0, "Password")
            self.password.config(show="", foreground="gray")

    def login_user(self):
        user = self.username.get()
        pwd = self.password.get()
        if user == "Username" or pwd == "Password":
            messagebox.showwarning("Login", "Please enter username and password")
            return

        if validate_user_from_csv(user, pwd):
            messagebox.showinfo("Login", "Login Successful!")
            self.master.destroy()  # Close login window
            os.system("python MainPage.py")
        else:
            messagebox.showerror("Login", "Invalid credentials")

class RegisterFrame(StyledFrame):
    def __init__(self, master):
        super().__init__(master, bg_color="#f7a1c4") # Soft pink
        self.master = master
        self.create_widgets()

    def create_widgets(self):
        # Title
        tk.Label(self, text="Register", font=("Helvetica", 26, "bold"),
                 bg="#f7a1c4", fg="#ffffff").pack(pady=(10, 20))

        # New Username Entry
        self.new_user = ttk.Entry(self, font=("Arial", 14), width=30)
        self.new_user.pack(pady=10)
        self.new_user.insert(0, "New Username")
        self.new_user.config(foreground="gray")
        self.new_user.bind("<FocusIn>", self.clear_username_placeholder)
        self.new_user.bind("<FocusOut>", self.restore_username_placeholder)

        # New Password Entry
        self.new_pwd = ttk.Entry(self, font=("Arial", 14), width=30, show="")
        self.new_pwd.pack(pady=10)
        self.new_pwd.insert(0, "New Password")
        self.new_pwd.config(foreground="gray")
        self.new_pwd.bind("<FocusIn>", self.clear_password_placeholder)
        self.new_pwd.bind("<FocusOut>", self.restore_password_placeholder)

        # Register Button
        register_btn = HoverButton(self, text="Register", command=self.register_user)
        register_btn.pack(pady=15, ipadx=10, ipady=5)

        # Back to Login Button
        back_btn = ttk.Button(self, text="Back to Login", command=self.master.switch_to_login,
                              style="Link.TButton")
        back_btn.pack(pady=5)

        style = ttk.Style()
        style.configure("Link.TButton", foreground="#ffffff", background="#f7a1c4",
                        font=("Arial", 10, "underline"), borderwidth=0)
        style.map("Link.TButton",
                  foreground=[('active', '#fbb3cb')])

    def clear_username_placeholder(self, event):
        if self.new_user.get() == "New Username":
            self.new_user.delete(0, tk.END)
            self.new_user.config(foreground="black")

    def restore_username_placeholder(self, event):
        if not self.new_user.get():
            self.new_user.insert(0, "New Username")
            self.new_user.config(foreground="gray")

    def clear_password_placeholder(self, event):
        if self.new_pwd.get() == "New Password":
            self.new_pwd.delete(0, tk.END)
            self.new_pwd.config(show="*", foreground="black")

    def restore_password_placeholder(self, event):
        if not self.new_pwd.get():
            self.new_pwd.insert(0, "New Password")
            self.new_pwd.config(show="", foreground="gray")

    def register_user(self):
        user = self.new_user.get()
        pwd = self.new_pwd.get()
        if user == "New Username" or pwd == "New Password":
            messagebox.showwarning("Register", "Please fill all fields")
            return
        if user and pwd:
            save_user_to_csv(user, pwd)
            messagebox.showinfo("Register", f"User '{user}' registered successfully!")
            self.master.switch_to_login()
        else:
            messagebox.showwarning("Register", "Please fill all fields")

if __name__ == "__main__":
    app = AuthApp()
    app.mainloop()
