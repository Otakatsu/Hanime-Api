from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse, FileResponse
import requests
import json
import secrets
from dateutil import parser
import requests


app = FastAPI()
@app.get('/')
def root(request: Request):
    return {"root": request.url.hostname}


@app.get('/search')
async def search(query, page):
    query = query
    page = page  
    res = {
        "search_text": query,
        "tags":
            [],
        "brands":
            [],
        "blacklist":
            [],
        "order_by": 
            [],
        "ordering": 
            [],
        "page": page,
    }
    headers = {
        "Content-Type": "application/json; charset=utf-8"
    }
    x = requests.post("https://search.htv-services.com", headers=headers, json=res)
    rl = x.json()
    text = {
        "response": json.loads(rl'hits']),
        "page": rl['page']
    }
    return text

@app.get('/recent')
async def recent(page = 0):
    page = page
    url = "https://search.htv-services.com"
    res = {
        "search_text": "",
        "tags":
            [],
        "brands":
            [],
        "blacklist":
            [],
        "order_by": "created_at_unix",
        "ordering": "desc",
        "page": page,
    }
    headers = {
        "Content-Type": "application/json; charset=utf-8"
    }
    x = requests.post(url, headers=headers, json=res)
    rl = x.json()
    text = {
        "reposone": json.loads(rl['hits']),
        "page": rl['page']
    }
    return text

@app.get('/trending')
async def trending(time = "month",page = 0):
    time = time
    p = page
    headers = {"X-Signature-Version": "web2",
               "X-Signature": secrets.token_hex(32)}
    x = requests.get(f"https://hanime.tv/api/v8/browse-trending?time={time}&page={p}", headers=headers)
    rl = x.json()
    text = {
        "reposone": rl["hentai_videos"],
        "time": rl["time"],
        "page": rl["page"]
    }
    return text


@app.get('/details')
async def details(id):
    id = id
    x = f"https://hanime.tv/api/v8/video?id={id}"
    x = requests.get(x)
    rl = x.json()
    created_at = rl["hentai_video"]["created_at"] = parser.parse(
        rl["hentai_video"]["created_at"]).strftime("%Y %m %d")
    released_date = rl["hentai_video"]["released_at"] = parser.parse(
        rl["hentai_video"]["released_at"]).strftime("%Y %m %d")
    view = rl["hentai_video"]["views"] = "{:,}".format(
        rl["hentai_video"]["views"])
    tags = rl["hentai_video"]["hentai_tags"]    
    text = {
        "query": rl["hentai_video"]["slug"],
        "name": rl["hentai_video"]["name"],
        "poster": rl["hentai_video"]["cover_url"],
        "id": rl["hentai_video"]["id"],   
        "description": rl["hentai_video"]["description"],     
        "views": view,
        "brand": rl["hentai_video"]["brand"],
        "created_at": created_at,
        "released_date": released_date,
        "is_censored": rl["hentai_video"]["is_censored"],         
        "tags": [x["text"] for x in tags]         
    }
    return text


@app.get('/link')
async def hentai_video(id):
    url = f"https://hanime.tv/api/v8/video?id={id}" 
    x = requests.get(url, headers={
        "X-Session-Token": "PhzIzReFsg7g2GZi-tz9KVpR2LskgMP8-l_xJ0kmbwhSuBOcD3yZJeOoQKS-ND1w3qFCGj0Y2HzfJ4renU82W25BNSVI6KnmwfiN5e9lueyQOYbZ0RVKmS2Ek1fLKvMnS_3ktEUiFOTjSCezPusemw==(-(0)-)hDLS0eC_45mNW15pn3ZJYQ==",
    })   
    rl = x.json()   
    text = {
        "data": rl["videos_manifest"]["servers"][0]["streams"]
    }
    return text

@app.get('/play')
async def m3u8(link):
    x = f'''
    <DOCTYPE html>
    <html>
    <body>
    <video id="live"  autoplay controls>
        <source src="{link}" type="video/mp4">
        </video>
        </body>
        </html>
    '''
    return HTMLResponse(content=x, status_code=200)
