import customtkinter
from App import App
from Main_ui import MainUI

app = App()

customtkinter.set_appearance_mode("system")
customtkinter.set_default_color_theme("dark-blue")

root = customtkinter.CTk()
root.title("Crypto Image")
main_ui = MainUI(root, app)

root.mainloop()
