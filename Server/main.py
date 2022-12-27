import uvicorn
from fastapi import FastAPI, Form, File, Response
from ServerApp import ServerApp
from getpass import getpass

DATABASE_DIR = ":memory:"
# DATABASE_DIR = "app.db"

server_app = ServerApp(DATABASE_DIR)
app = FastAPI()

def Config_database() -> bool:
    load_database = input("Do you want to keep old key config (Y/n): ")[:1].lower()
    load_database = load_database if load_database else "y"
    if load_database == "y":
        password = getpass("Input password: ")
        res = server_app.Load_database_key(password)
        print(res["message"])
        return res["result"]
    elif load_database == "n":
        print("Create new database config.")
        while True:
            password = getpass("enter password: ")
            repassword = getpass("re enter password: ")
            if repassword == password: break
            else: print("Please enter same passwaords")
        print(server_app.Renew_database_key(password)["message"])
        print(server_app.Load_database_key(password)["message"])
        return True
    return False

@app.post("/create_account")
async def create_account(username: str = Form(), password: str = Form()):
    res = server_app.Create_user(username, password)
    return res

@app.get("/login")
async def login(username: str = Form(), password: str = Form()):
    res = server_app.Login(username, password)
    return res

@app.post("/extend_cookie")
async def extend_cookie(cookie: str = Form()):
    res = server_app.Login_cookie(cookie)
    return res

@app.get("/user_info")
async def user_info(cookie: str = Form()):
    res = server_app.Get_user_info(cookie)
    return res

@app.get("/own_imgs/{user_name}")
async def own_imgs(user_name: str, cookie: str = Form()):
    res = server_app.Get_own_imgs(cookie, user_name)
    return res

@app.get("/purchase_imgs")
async def purchase_imgs(cookie: str = Form()):
    res = server_app.Get_purchase_imgs(cookie)
    return res

@app.post("/buy_img/{owner}/{img_name}")
async def buy_img(owner: str, img_name: str, cookie: str = Form()):
    res = server_app.Buy_img(cookie, owner, img_name)
    return res

@app.get("/download/{owner}/{img_name}")
async def download_img(owner: str, img_name: str, cookie: str = Form()):
    img_res = server_app.Get_image(cookie, owner, img_name)
    if img_res["result"] == False: return img_res
    
    res = Response(img_res["image"])
    res.headers["img_name"] = img_res["img_name"].decode()
    res.headers["owner"] = img_res["owner"].decode()
    return res

@app.post("/upload/{img_name}/{cost}")
async def upload_img(img_name: str, cost: int, img: bytes = File(), cookie: str = Form()):
    if (res := server_app.Verify_cookie(cookie))["result"] == False:
        return res
    
    # encrypt img and then upload it into server
    res = server_app.Upload_img(cookie, img, img_name, cost)
    return res


@app.post("/change_database_password")
async def change_database_password(old_password: str = Form(), new_password: str = Form()):
    res = server_app.Change_database_password(old_password, new_password)
    return res

@app.post("/renew_database_key")
async def renew_database_key(password: str = Form()):
    res = server_app.Renew_database_key(password)
    return res

@app.post("/load_database_key")
async def load_database_key(password: str = Form()):
    res = server_app.Load_database_key(password)
    return res


if __name__ == "__main__":
    while True:
        if Config_database(): break
    uvicorn.run(app, host="127.0.0.1", port=8000)
    


