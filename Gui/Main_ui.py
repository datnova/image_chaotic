from customtkinter import CTkFrame, CTkLabel, CTkButton, CTk, CTkTextbox, CTkInputDialog
from Login_ui import LoginUI, App
from tkinter import messagebox, filedialog


class MainUI:
    def __init__(self, root: CTk, app: App = None):
        self.root =                      root
        self.app =                       app
        self.frame =                     CTkFrame(master=self.root)

        self.menu_frame =                CTkFrame(master=self.frame)
        self.menu_label =                CTkLabel(master=self.menu_frame)
        self.search_button =             CTkButton(master=self.menu_frame)
        self.own_button =                CTkButton(master=self.menu_frame)
        self.purchase_button =           CTkButton(master=self.menu_frame)
        self.username_info_label =       CTkLabel(master=self.menu_frame)
        self.money_info_label =          CTkLabel(master=self.menu_frame)
        self.signout_button =            CTkButton(master=self.menu_frame)
        
        self.display_frame =             CTkFrame(master=self.frame)
        
        # display search frame
        self.search_label =              CTkLabel(master=self.display_frame)
        self.search_user_button =        CTkButton(master=self.display_frame)
        self.username_label =            CTkLabel(master=self.display_frame)
        self.search_imgs_textbox =       CTkTextbox(master=self.display_frame)
        self.purchased_imgs_button =     CTkButton(master=self.display_frame)
        
        # display owned imgs frame
        self.owned_imgs_textbox =        CTkTextbox(master=self.display_frame)
        self.owned_img_label =           CTkLabel(master=self.display_frame)
        self.upload_button =             CTkButton(master=self.display_frame)
        self.download_owned_button =     CTkButton(master=self.display_frame)
        
        # display purchased img frame
        self.purchased_imgs_textbox =    CTkTextbox(master=self.display_frame)
        self.purchased_img_label =       CTkLabel(master=self.display_frame)
        self.download_purchased_button = CTkButton(master=self.display_frame)
        
        self.login_ui = LoginUI(self.root, self.app, self)
        self.login_ui.Show()

    def Setup(self):
        self.Setup_frame()
        self.Setup_menu_frame()
        self.Setup_display_frame()
        self.Setup_display_search_frame()
        
    def Setup_frame(self):
        self.frame.pack(pady=12, padx=12, fill="both", expand=True)
        
    def Setup_menu_frame(self):
        self.menu_frame.pack_propagate(False)
        self.menu_frame.configure(width=230, height=550, corner_radius=30)
        self.menu_frame.pack(padx=20, pady=20, anchor="center", side="left")
        
        self.menu_label.configure(text="Crypto Image", text_color="#399745", font=("Roboto", 24))
        self.menu_label.pack(pady=20)
        
        self.search_button.configure(
            text="Search", 
            width=230, 
            height=50, 
            font=("Roboto", 20), 
            corner_radius=30,
            command=self.Setup_display_search_frame)
        self.search_button.pack(pady=10)
        
        self.own_button.configure(
            text="Owned", 
            width=230, 
            height=50, 
            font=("Roboto", 20), 
            corner_radius=30,
            command=self.Setup_display_owned_frame)
        self.own_button.pack(pady=10)
        
        self.purchase_button.configure(
            text="Purchased", 
            width=230, 
            height=50, 
            font=("Roboto", 20),  
            corner_radius=30, 
            command=self.Setup_display_purchased_frame)
        self.purchase_button.pack(pady=10)
        
        self.Setup_user_info()
        
        self.Setup_signout_button()
                
    def Setup_signout_button(self):
        self.signout_button.configure(text="sign out", 
                                      width=30, 
                                      height=30, 
                                      font=("Roboto", 20), 
                                      corner_radius=30,
                                      fg_color="#FC3C3C",
                                      hover_color="#C73737",
                                      command=self.sign_out)
        self.signout_button.pack(pady=10, side="bottom")
                    
    def sign_out(self):
        self.Hide()
        self.login_ui.Show()
        
    def Setup_user_info(self):
        self.Reload_user_info()
        self.username_info_label.pack()
        self.money_info_label.pack()
        
    def Reload_user_info(self):
        res = self.app.Get_user_info()
        self.username_info_label.configure(text=f"username: {res['user_name']}")
        self.money_info_label.configure(text=f"money: {res['money']}")
        
    def Setup_display_frame(self):
        self.display_frame.grid_propagate(False)
        self.display_frame.configure(width=900, height=550, corner_radius=30)
        self.display_frame.pack(padx=20, pady=20, side="right")

    def Setup_display_search_frame(self):
        self.Clear_display_frame()
        
        self.search_label.configure(text="Search images", font=("Roboto", 30), text_color="#399745")
        self.search_label.grid(padx=(100,10), sticky="w")
        
        self.search_user_button.configure(text="Search user", command=self.Find_user)
        self.search_user_button.grid(column=0, row=0, sticky='w', pady=(80, 0), padx=(100,0))
        
        self.username_label.configure(text="Username: ")
        self.username_label.grid(column=1, row=0, sticky='w', pady=(80, 0))

        self.search_imgs_textbox.configure(width=600, height=200, state='disable', font=("Roboto", 15))
        self.search_imgs_textbox.grid(column=0, row=1, sticky="w", padx=(100, 0), columnspan=3)
        
        self.purchased_imgs_button.configure(text="Purchase", command=self.Purchase_img)
        self.purchased_imgs_button.grid(column=2, row=2, sticky='e')

    def Setup_display_owned_frame(self):
        self.Clear_display_frame()
        
        self.owned_img_label.configure(text="Owned images", font=("Roboto", 30), text_color="#399745")
        self.owned_img_label.grid(column=0, row=0, pady=(50, 0), padx=(100,10), sticky="w")
        
        self.owned_imgs_textbox.configure(width=600, height=200, state='disable', font=("Roboto", 15))
        self.owned_imgs_textbox.grid(column=0, row=1, sticky="w", padx=(100, 0), columnspan=3)
        
        self.upload_button.configure(text="upload image", command=self.Upload_img)
        self.upload_button.grid(column=0, row=2, sticky="w", padx=(100, 0))
        
        self.download_owned_button.configure(text="download image", command=self.Download_owned_img)
        self.download_owned_button.grid(column=2, row=2, sticky='e')
        
        self.Reload_owned_imgs()

    def Setup_display_purchased_frame(self):
        self.Clear_display_frame()
        
        self.purchased_img_label.configure(text="Purchased images", font=("Roboto", 30), text_color="#399745")
        self.purchased_img_label.grid(column=0, row=0, pady=(50, 0), padx=(100,10), sticky="w")

        self.purchased_imgs_textbox.configure(width=600, height=200, state='disable', font=("Roboto", 15))
        self.purchased_imgs_textbox.grid(column=0, row=1, sticky="w", padx=(100, 0), columnspan=3)
        
        self.download_purchased_button.configure(text="download image", command=self.Download_purchase_img)
        self.download_purchased_button.grid(column=0, row=2, sticky="e")
        
        self.Reload_purchased_imgs()
        
    def Clear_display_frame(self):
        for item in self.display_frame.winfo_children():
            item.grid_forget()

    def Reload_owned_imgs(self):
        self.owned_imgs_textbox.configure(state="normal")
        self.owned_imgs_textbox.delete("0.0", "end")
        imgs = self.app.Search_owned_imgs()["imgs_name"]
        for img in imgs:
            self.owned_imgs_textbox.insert(f"0.0", f"{img[0].ljust(60)}| {img[1]}\n")
        self.owned_imgs_textbox.insert(f"0.0", f"{'<img name>'.ljust(60)}| <cost>\n")
        self.owned_imgs_textbox.configure(state="disable")

    def Reload_purchased_imgs(self):
        self.purchased_imgs_textbox.configure(state="normal")
        self.purchased_imgs_textbox.delete("0.0", "end")
        imgs = self.app.Search_purchased_imgs()["imgs_name"]
        for img in imgs:
            self.purchased_imgs_textbox.insert(f"0.0", f"{img[0].ljust(40)}| {img[2].ljust(40)}|{img[1]}\n")
        self.purchased_imgs_textbox .insert(f"0.0", f"{'<img name>'.ljust(40)}| {'<owner>'.ljust(40)}| <cost>\n")
        self.purchased_imgs_textbox.configure(state="disable")

    def Reload_search_imgs(self, username: str):
        self.search_imgs_textbox.configure(state="normal")
        self.search_imgs_textbox.delete("0.0", "end")
        imgs = self.app.Search_owned_imgs(username)["imgs_name"]
        for img in imgs:
            self.search_imgs_textbox.insert(f"0.0", f"{img[0].ljust(60)}| {img[1]}\n")
        self.search_imgs_textbox.insert(f"0.0", f"{'<img name>'.ljust(60)}| <cost>\n")
        self.search_imgs_textbox.configure(state="disable")

    def Upload_img(self):
        img_path = filedialog.askopenfilename(
            initialdir = "C:\\",
            title = "Select file",
            filetypes = (("png files","*.png"), ("all files","*.*"))
        )
        if not img_path: return 

        while True:        
            try:
                dialog = CTkInputDialog(text="Type in img cost:", title="Input cost")
                cost = dialog.get_input()
                break
            except ValueError:
                messagebox.showerror("Error", "Please only input number!")
        
        res = self.app.Upload_img(img_path, cost)
        if res.get("result") is None:
            return
        elif res["result"] == False:
            messagebox.showerror("Error", res["message"])
        else:
            self.Reload_owned_imgs()
            messagebox.showinfo("Info", res["message"])

    def Download_owned_img(self):
        dialog = CTkInputDialog(text="Type in image name:", title="download image")
        img_name = dialog.get_input()
        img_name = img_name if img_name.endswith(".png") else f"{img_name}.png"
        
        file_path = filedialog.asksaveasfilename(
            initialdir = "c:\\",
            defaultextension=".png",
            title = "Select file",
            filetypes = (("png files","*.png"),("all files","*.*"))
        )
        
        if self.app.Download_img(img_name, file_path, self.app.username) == False:
            messagebox.showerror("Error", f"Cant download {img_name} owned by {self.app.username}")
        else:
            messagebox.showinfo("Info", "Download success!")

    def Download_purchase_img(self):
        dialog = CTkInputDialog(text="Type in image name:", title="download image")
        img_name = dialog.get_input()
        img_name = img_name if img_name.endswith(".png") else f"{img_name}.png"
        
        dialog = CTkInputDialog(text="Type in owner:", title="download image")
        owner = dialog.get_input()
        
        file_path = filedialog.asksaveasfilename(
            initialdir = "c:\\",
            defaultextension=".png",
            title = "Select file",
            filetypes = (("png files","*.png"),("all files","*.*"))
        )
        
        if self.app.Download_img(img_name, file_path, owner) == False:
            messagebox.showerror("Error", f"Cant download {img_name} owned by {owner}")
        else:
            messagebox.showinfo("Info", "Download success!")

    def Purchase_img(self):
        dialog = CTkInputDialog(text="Type in image name:", title="purchase image")
        img_name = dialog.get_input()
        img_name = img_name if img_name.endswith(".png") else f"{img_name}.png"
        
        res = self.app.Purchase_img(img_name)
        if res["result"] == False:
            messagebox.showerror("Error", res["message"])
        else:
            messagebox.showinfo("Info", res["message"])
            self.Reload_user_info()

    def Find_user(self):
        dialog = CTkInputDialog(text="Type in username:", title="Search username")
        username = dialog.get_input()
        
        if not username: return
        self.app.current_search_name = username
        
        res = self.app.Search_owned_imgs(username)
        if res["result"] == False:
            self.username_label.configure(text="Username: ")
            messagebox.showerror("Error", res["message"])
            return
        
        self.username_label.configure(text=f"Username: {username}")
        self.Reload_search_imgs(username)

    def Show(self):
        self.root.geometry("1100x480")
        self.Setup()
    
    def Hide(self):
        self.frame.pack_forget()
        self.menu_frame.pack_forget()
        self.display_frame.pack_forget()
        
