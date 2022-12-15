from customtkinter import CTkFrame, CTkLabel, CTkEntry, CTkButton, CTk
from tkinter import messagebox
from App import App

class SignupUI:
    def __init__(self, root: CTk, app: App = None, signin_ui = None):
        self.root =             root
        self.app =              app
        self.signin_ui =        signin_ui
        self.frame =            CTkFrame(master=self.root)
        self.main_label =       CTkLabel(master=self.frame)
        self.signup_label =     CTkLabel(master=self.frame)
        self.username_entry =   CTkEntry(master=self.frame)
        self.password_entry =   CTkEntry(master=self.frame)
        self.repassword_entry = CTkEntry(master=self.frame)
        self.signup_button =    CTkButton(master=self.frame)
        self.back_button =      CTkButton(master=self.frame)

    def Setup(self):
        self.Setup_frame()
        self.Setup_main_label()
        self.Setup_signup_lable()
        self.Setup_username_entry()
        self.Setup_password_entry()
        self.Setup_repassword_entry()
        self.Setup_sigup_button()
        self.Setup_back_button()
        
    def Setup_frame(self):
        self.frame.pack(pady=12, padx=12, fill="both", expand=True)
        
    def Setup_username_entry(self):
        self.username_entry.configure(placeholder_text="Username", width=200)
        self.username_entry.pack(pady=12, padx=10)
                
    def Setup_password_entry(self):
        self.password_entry.configure(placeholder_text="Password", width=200, show="*")
        self.password_entry.pack(pady=12, padx=10)

    def Setup_repassword_entry(self):
        self.repassword_entry.configure(placeholder_text="Retype password", width=200, show="*")
        self.repassword_entry.pack(pady=12, padx=10)
    
    def Setup_sigup_button(self):
        self.signup_button.configure(text="Sign up", command=self.Check_password)
        self.signup_button.pack(pady=12, padx=10)
    
    def Setup_back_button(self):
        self.back_button.configure(
            text="⬅", 
            font=("Roboto", 24),
            width=40,
            text_color="#FF0000",
            fg_color="transparent",
            hover_color="#FF6666",
            command=self.Back_signin)
        self.back_button.pack(padx=10, side="left")
    
    def Setup_main_label(self):
        self.main_label.configure(text="Crypto Image", font=("Roboto", 30), text_color="#399745")
        self.main_label.pack(pady=12, padx=10, fill="both")    
        
    def Setup_signup_lable(self):
        self.signup_label.configure(text="Sign up", font=("Roboto", 20))
        self.signup_label.pack(pady=12, padx=10, fill="both")
    
    def Show(self):
        self.root.geometry("600x400")
        self.Setup()
    
    def Hide(self):
        self.frame.pack_forget()
    
    def Back_signin(self):
        self.Hide()
        self.signin_ui.Show()
        
    def Check_password(self):
        pwd1 = self.password_entry.get()
        pwd2 = self.repassword_entry.get()
        username = self.username_entry.get()
        
        if not (pwd1 and pwd2 and username):
            messagebox.showwarning("warning", "Please enter passwords and username!")
            return
        
        res = self.app.Signup(username, pwd1, pwd2)
        if res["result"]:
            messagebox.showinfo("message", res["message"])
        else:
            messagebox.showerror("Error", res["message"])
            