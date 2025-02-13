# requires-python ">=3.13"
# dependencies = [
#     "fastapi",
#     "uvicorn",
#     "requests"
# ]

from fastapi import FastAPI,HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
import os

app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

AIPROXY_TOKEN=os.getenv("AIPROXY_TOKEN")

@app.get("/")
def home():
    return "Man this takes a lot of time"

@app.get("/read")
def read_file(path: str):
    try:
        with open(path,"r") as f:
            return f.read()
    except:
        raise HTTPException(status_code=404,detail="File does not exist")

@app.route("/run")
def task_runner(task: str):
    url= "https://aiproxy.sanand.workers.dev/openai/v1/chat/completions"
    headers={
        "Content-Type": "application/json",
        "Authorization":f"Bearer {AIPROXY_TOKEN}"
    }
    data={
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "user", "content": task},
            {"role": "system", "content": ""}
            
        ]
    }
    requests(url=url, headers=headers, json=data)




if __name__ == '__main__':
    import uvicorn   
    uvicorn.run(app,host="0.0.0.0",port=8000)
      
