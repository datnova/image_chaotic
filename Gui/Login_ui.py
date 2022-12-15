from customtkinter import CTkFrame, CTkLabel, CTkEntry, CTkButton, CTk
from Signup_ui import SignupUI, App
from tkinter import messagebox

class LoginUI:
    def __init__(self, root: CTk, app: App = None, main_ui = None):
        self.root =             root
        self.app =              app
        self.main_ui =          main_ui
        self.signup_ui =        SignupUI(self.root, self.app, self)
        self.frame =            CTkFrame(master=self.root)
        self.main_label =       CTkLabel(master=self.frame)
        self.login_label =      CTkLabel(master=self.frame)
        self.username_entry =   CTkEntry(master=self.frame)
        self.password_entry =   CTkEntry(master=self.frame)
        self.login_button =     CTkButton(master=self.frame)
        self.signup_button =    CTkButton(master=self.frame)
    
    def Setup(self):
        self.Setup_frame()
        self.Setup_main_label()
        self.Setup_login_lable()
        self.Setup_username_entry()
        self.Setup_password_entry()
        self.Setup_login_button()
        self.Setup_sigup_button()
    
    def Setup_frame(self):
        self.frame.pack(pady=12, padx=12, fill="both", expand=True)
    
    def Setup_username_entry(self):
        self.username_entry.configure(placeholder_text="Username", width=200)
        self.username_entry.pack(pady=12, padx=10)

    def Setup_password_entry(self):
        self.password_entry.configure(placeholder_text="Password", width=200, show="*")
        self.password_entry.pack(pady=12, padx=10)
    
    def Setup_login_button(self):
        self.login_button.configure(text="Log in", command=self.Log_in)
        self.login_button.pack(pady=12, padx=10)
    
    def Setup_sigup_button(self):
        self.signup_button.configure(text="Sign up", command = self.Sign_up)
        self.signup_button.pack(pady=12, padx=10)
    
    def Setup_login_lable(self):
        self.login_label.configure(text="Log in", font=("Roboto", 20))
        self.login_label.pack(pady=12, padx=10, fill="both")
    
    def Setup_main_label(self):
        self.main_label.configure(text="Crypto Image", font=("Roboto", 30), text_color="#399745")
        self.main_label.pack(pady=12, padx=10, fill="both")
        
    def Show(self):
        self.root.geometry("600x400")
        self.Setup()
    
    def Hide(self):
        self.frame.pack_forget()
        
    def Sign_up(self):
        self.Hide()
        self.signup_ui.Show()
        
    def Log_in(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if not (username and password):
            messagebox.showerror("Error", "Please enter username and password!")
            return
        
        res = self.app.Login(username, password)
        if res["result"] == False:
            messagebox.showerror("Error", res["message"])
            return

        self.Hide()
        self.main_ui.Show()
            
        