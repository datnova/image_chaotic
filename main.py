import uvicorn
from fastapi import FastAPI, Form, File, Response
from ServerApp import ServerApp

# DATABASE_DIR = ":memory:"
DATABASE_DIR = "app.db"

server_app = ServerApp(DATABASE_DIR)
app = FastAPI()

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
    res.headers["img_name"] = img_res["img_name"]
    res.headers["owner"] = img_res["owner"]
    return res

@app.post("/upload/{img_name}/{cost}")
async def upload_img(img_name: str, cost: int, img: bytes = File(), cookie: str = Form()):
    if (res := server_app.Verify_cookie(cookie))["result"] == False:
        return res
    
    # encrypt img and then upload it into server
    res = server_app.Upload_img(cookie, img, img_name, cost)
    return res

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
    


