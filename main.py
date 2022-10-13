##ToDo:
## - Fix api calls to equipedCosmetics so they return corect data
## - get discord profilePictures working
## - make sql calls more optimised
## - have a stroke, and die; if that doesnt work just jump of a bridge
## - fuck and humiliate whoever decompiles the client/api
## - jerk off to the clean /docs ui


import asyncio
from fastapi import FastAPI, WebSocket, Query, status, Response
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import mysql.connector
import json
import discord
import paypalrestsdk
from starlette.requests import Request
import os

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

tags_metadata = [
    {
        "name": "root",
        "description": "Just stuff so the api stays online!",
    },
    {
        "name": "user",
        "description": "To get information about a userer.",
    },
    {
        "name": "client",
        "description": "Whats required to handel things in the client, like login and out and administrative calls.",
    },
    {
        "name": "stats",
        "description": "To get global stats about the client.",
    },
    {
        "name": "assets",
        "description": "To get assets not related to the client.",
    },
    {
        "name": "shop",
        "description": "Whats required to handel things in the store, like listing all the items and geting item information.",
    },
]

paypalrestsdk.configure({
  "mode": "sandbox", # sandbox or live
  "client_id": "AXN5yyxphtBu0Wk_hUBiLvUPUf1GqwiXGED8ty_AhBT7wfM1cXOhN3UbYnNd_f8r-ndkzUKgfp94F9V5",
  "client_secret": "EBQTXBBuDw0QeoTfE4DcAzsSrHYIC5It3tDCiB9r7bfVInR5WCchoqorEQkBE1Q_VNno4niuEL9pjEUe" })

class create_dict(dict):
    def __init__(self):
        self = dict()
    def add(self, key, value):
        self[key] = value

def mysqlQuery(q):
    mydb = mysql.connector.connect(host="hestia.engelbrecht.pro", user="SpyMiner_GLC", password="Password1", database="SpyMiner_GLC")
    cursor = mydb.cursor()
    cursor.execute(q)
    result = cursor.fetchall()
    cursor.close()
    return result

def mysqlQueryInsert(q):
    mydb = mysql.connector.connect(host="hestia.engelbrecht.pro", user="SpyMiner_GLC", password="Password1", database="SpyMiner_GLC")
    cursor = mydb.cursor()
    cursor.execute(q)
    mydb.commit()
    cursor.close()

def remove_values_from_list(the_list, val):
   return [value for value in the_list if value != val]

app = FastAPI(title="GLC-API", docs_url="/docs", redoc_url=None, openapi_tags=tags_metadata)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
  asyncio.create_task(client.start('OTQ0Nzc3OTM0OTE1Mzk5Njkx.GG7FnP.09BePYF6tn5AYPpkyk8mnHyoGtVxpGSJS-DiGQ'))


@app.get("/", tags=["root"]
async def home():
    return RedirectResponse(url='https://www.glacierclient.net'))

@app.get("/update", tags=["root"]
async def update():
    os.system("git pull")
    return "200 ok"

@app.get("/favicon.ico", tags=["root"])
async def favicon():
    return RedirectResponse(url="https://www.glacierclient.net/glclogo_16x16.png")

@app.get("/robots.txt", tags=["root"])
async def robots():
    return RedirectResponse(url="https://www.glacierclient.net/apirobots.txt")

@app.get("/user/playername/{UUID}", tags=["user"])
async def getPlayerName(UUID):
    returnedData = mysqlQuery(f"SELECT * From Players WHERE UUID=\"{UUID}\"")
    if returnedData == []:
        return {"error": "User Doesn't Exist! (0x3df5)"}
    else:
        return {"UUID": UUID, "Player": returnedData[0][2]}

@app.get("/user/playerUUID/{playerName}", tags=["user"])
async def getPlayerUUID(playerName):
    returnedData = mysqlQuery(f"SELECT * From Players WHERE playerName=\"{playerName}\"")
    if returnedData == []:
        return {"error": "User Doesn't Exist! (0x3df5)"}
    else:
        return {"Player": playerName, "UUID": returnedData[0][1]}

@app.get("/user/isbanned/{uuid}", tags=["user"])
async def isBanned(uuid):
    returnedData = mysqlQuery(f"SELECT * FROM Players WHERE UUID=\"{uuid}\"")
    if returnedData == []:
        return {"error": "User Doesn't Exist! (0x3df5)"}
    else:
        return {"UUID": uuid, "isBanned": returnedData[0][3], "banReason": returnedData[0][4]}

@app.get("/user/betaAccess/{uuid}", tags=["user"])
async def hasBetaAccess(uuid):
    returnedData = mysqlQuery(f"SELECT * FROM Players WHERE UUID='{uuid}'")
    if returnedData == []:
        return {"error": "User Doesn't Exist! (0x3df5)"}
    else:
        return {"UUID": uuid, "betaAccess": returnedData[0][5]}

@app.get("/user/isonline/{uuid}", tags=["user"])
async def isBanned(uuid):
    returnedData = mysqlQuery(f"SELECT * FROM Players WHERE UUID=\"{uuid}\"")
    if returnedData == []:
        return {"error": "User Doesn't Exist! (0x3df5)"}
    else:
        return {"UUID": uuid, "isOnline": returnedData[0][7]}

@app.get("/user/equipedCosmetics/{uuid}", tags=["user"])
async def getUsersEquipedCosmetics(uuid):
    returnedData = mysqlQuery(f"SELECT * FROM Players WHERE UUID='{uuid}'")
    if returnedData == []:
        return {"error": "User Doesn't Exist! (0x3df5)"}
    elif returnedData[0][9] == None:
        return {"error": "User Doesn't Have Cosmetics Equiped! (0x3de4)"}
    else:
        consmeticsList = returnedData[0][9].decode("utf-8").split(",")
        return {"UUID" : uuid, "equipedCosmetics" : consmeticsList}

@app.get("/user/ownedCosmetics/{uuid}", tags=["user"])
async def getUsersOwnedCosmetics(uuid):
    returnedData = mysqlQuery(f"SELECT * FROM Players WHERE UUID='{uuid}'")
    if returnedData == []:
        return {"error": "User Doesn't Exist! (0x3df5)"}
    elif returnedData[0][8] == None:
        return {"error": "User Doesn't own any Cosmetics! (0x3de5)"}
    else:
        consmeticsList = returnedData[0][8].decode("utf-8").split(",")
        return {"UUID" : uuid, "ownedCosmetics" : consmeticsList}

@app.get("/user/listAll", tags=["user"])
async def listAll():
    returnedData = mysqlQuery("SELECT * FROM Players")
    mydict= create_dict()
    for row in returnedData:
        mydict.add(row[0],({"UUID":row[1],"playerName":row[2],"isBanned":row[3],"banReason":row[4], "betaAccess":row[5], "rank":row[6], "isOnline":row[7], "ownedCosmetics":row[8], "equipedCosmetics":row[9]}))
    return mydict

@app.get("/client/login/{uuid}/{playerName}", tags=["client"])
async def playerLogin(uuid, playerName):
    returnedData = mysqlQuery(f"SELECT * FROM Players WHERE UUID=\"{uuid}\"")
    if returnedData == []:
         mysqlQueryInsert(f"INSERT INTO `Players` (`id`, `UUID`, `playerName`, `isBanned`, `banReason`, `betaAccess`, `rank`, `isOnline`, `ownedCosmetics`, `equipedCosmetics`) VALUES (NULL, '{uuid}', '{playerName}', '0', NULL, '0', 'Member', '1', NULL, NULL);")
         return {"message": "Added Player and Set as Online!"}
    elif returnedData[0][3] != playerName:
        mysqlQueryInsert(f"UPDATE Players SET playerName='{playerName}' WHERE UUID='{uuid}'")
        mysqlQueryInsert(f"UPDATE Players SET isOnline=1 WHERE UUID='{uuid}'")
        return {"message": "Updated playerName in DB and set as Online!"}
    elif returnedData[0][3] == playerName:
        mysqlQueryInsert(f"UPDATE Players SET isOnline=1 WHERE UUID='{uuid}'")
        return {"message": "Set Player As Online!"}

@app.get("/client/logout/{uuid}", tags=["client"])
async def playerLogout(uuid):
    mysqlQueryInsert(f"UPDATE Players SET isOnline=0 WHERE UUID='{uuid}'")
    return {"message": "Set Player As Offline!"}
 
@app.get("/client/getNone", tags=["client"])
async def getNone():
    return None

@app.get("/stats/currentlyOnline", tags=["stats"])
async def getNumOfPlayersOnline():
    returnedData = mysqlQuery(f"SELECT COUNT(UUID) FROM Players WHERE isOnline=1")
    return {"Online": returnedData[0][0]}
    
@app.get("/stats/addDownload", tags=["stats"])
async def addDownload(ending):
    returnedData = mysqlQuery("SELECT data FROM Stats WHERE header='downloads'")
    mysqlQueryInsert(f"UPDATE Stats SET data={returnedData[0][0] + 1} WHERE header='downloads'")
    return RedirectResponse(url= f"https://www.glacierclient.net/download/Installer.{ending}")

@app.get("/stats/downloads", tags=["stats"])
async def getDownloads():
    returnedData = mysqlQuery("SELECT data FROM Stats WHERE header='downloads'")
    return {"Downloads": returnedData[0][0]}

@app.get("/login/microsoft", tags=["root"])
async def getLoginTokenURL(request: Request) -> None:
    return {"URI": "https://api.glacierclient.net" + request.url.path + "?code="+ request.query_params["code"] + "&state=<optional%3b"}

@app.get("/assets/discord/pfp/{id}", tags=["assets"])
async def getDiscordPFP(id):
    user = await client.fetch_user(id)
    return RedirectResponse(url= user.avatar_url)

@app.get("/assets/minecraft/renders/face/{uuid}", tags=["assets"])
async def getAssetRenderFace(uuid):
    return RedirectResponse(url= f"https://crafatar.com/avatars/{uuid}")

@app.get("/assets/minecraft/renders/head/{uuid}", tags=["assets"])
async def getAssetRenderHead(uuid):
    return RedirectResponse(url= f"https://crafatar.com/renders/head/{uuid}")

@app.get("/assets/minecraft/renders/body/{uuid}", tags=["assets"])
async def getAssetRenderBody(uuid):
    return RedirectResponse(url= f"https://crafatar.com/renders/body/{uuid}")

@app.get("/assets/minecraft/render/bust/{uuid}", tags=["assets"])
async def getAssetrenderBust(uuid):
    return RedirectResponse(url= f"https://visage.surgeplay.com/bust/{uuid}")

@app.get("/assets/minecraft/skin/{uuid}", tags=["assets"])
async def getAssetSkin(uuid):
    return RedirectResponse(url= f"https://crafatar.com/skins/{uuid}")    

@app.get("/assets/items/{id}", tags=["assets"])
async def getItemAssetsByID(id):
    returnedData = mysqlQuery(f"SELECT * FROM ShopItems WHERE id='{id}'")
    return {"id" : id, "asset" : returnedData[0][7]}

@app.get("/shop/items/listAll", tags=["shop"])
async def listAllItems():
    returnedData = mysqlQuery("SELECT * FROM ShopItems")
    mydict= create_dict()
    for row in returnedData:
        mydict.add(row[0],({"available":row[1],"item":row[2],"catagory":row[3], "description":row[4], "price":row[5], "thumnailLocation":row[6], "asset":row[7]}))
    return mydict

@app.get("/shop/item/{id}", tags=["shop"])
async def getItemByID(id):
    returnedData = mysqlQuery(f"SELECT * FROM ShopItems WHERE id=\"{id}\"")
    return {"id": id, "available": returnedData[0][1], "item": returnedData[0][2], "catagory": returnedData[0][3], "description": returnedData[0][4], "price": returnedData[0][5], "thumnaolLocation": returnedData[0][6], "asset": returnedData[0][7]}
    
@app.get("/shop/items/{catagory}", tags=["shop"])
async def getItemsByCatagory(catagory):
    returnedData = mysqlQuery(f"SELECT * FROM ShopItems WHERE catagory=\"{catagory}\"")
    mydict= create_dict()
    for row in returnedData:
        mydict.add(row[0],({"available":row[1],"item":row[2],"catagory":row[3], "description":row[4], "price":row[5], "thumnailLocation":row[6], "asset":row[7]}))
    return mydict
    
@app.get("/shop/payment/paypal/{uuid}", tags=["shop"])
async def prossessingpaymentPaypal(uuid, id : List[int] = Query(None)):
    items = []
    totalPrice = 0.00
    for x in id:
        returnedData = mysqlQuery(f"SELECT * FROM ShopItems WHERE id=\"{x}\"")
        items.append({
                    "name": returnedData[0][2],
                    "sku": x,
                    "price": returnedData[0][5],
                    "currency": "USD",
                    "quantity": 1})
        totalPrice = totalPrice + returnedData[0][5]
                 
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"},
        "redirect_urls": {
            "return_url": "https://api.glacierclient.net/shop/payment/return/paypal/execute",
            "cancel_url": "https://www.glacierclient.net/shop"},
        "transactions": [{
            "item_list": {
                "items": items },
            "amount": {
                "total": totalPrice,
                "currency": "USD"},
            "description": uuid}]})
    if payment.create():
        return RedirectResponse(url=payment.links[1].href)

@app.get("/shop/payment/return/paypal/execute", tags=["shop"])
async def paypalPaymentReturn(paymentId : str = "", token : str = "", PayerID : str = ""):
    payment = paypalrestsdk.Payment.find(paymentId)
    playerUUID = payment.transactions[0].description
    items = []
    for x in payment.transactions[0].item_list.items:
        items.append(x.sku)
        
    returnedData = mysqlQuery(f"SELECT * FROM Players WHERE UUID='{playerUUID}'")
    if returnedData[0][8] == None:
        cosmetics = ",".join(str(x) for x in items)
    else:
        for x in returnedData[0][8].split(","):
            items = remove_values_from_list(items, x)
        cosmetics = returnedData[0][8] + "," + ",".join(str(x) for x in items)
    mysqlQueryInsert(f"UPDATE Players SET ownedCosmetics='{cosmetics}' WHERE UUID='{playerUUID}'")
    return RedirectResponse(url='https://www.glacierclient.net')
    
@app.websocket("/")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")

@app.get("/client/version", tags=["client"])
async def getCurrentVersion():
    retunedData = mysqlQuery(f"SELECT * FROM `version` ORDER BY id DESC LIMIT 0, 1")
    return {"ver" : retunedData[0][1], "verLong" : retunedData[0][2], "download" : retunedData[0][3]}
