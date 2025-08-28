# main.py
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from dashscope import Application
import os
import json
from pydantic_settings import BaseSettings
import asyncio
from typing import AsyncGenerator
from dotenv import load_dotenv
load_dotenv()

print("allowed_origins from os.environ:", os.environ.get("allowed_origins"))
class Settings(BaseSettings):
    chat_agent_api_key: str #所有的agent的apikey都是一样的


    #辅助性agent

    only_translate_app_id: str

    #quickChatScreen中的agent
    zero_app_id:str
    soul_app_id:str
    misheard_app_id: str
    correction_app_id: str
    game_misheard_app_id: str
    game_word_app_id: str
    culture_app_id: str
    dialect_app_id: str
    super_translate_app_id: str
    stem_app_id:str
    dream_weaver_app_id: str
    fantasy_master_app_id: str
    glitch_space_app_id: str
    ln_factory_app_id: str
    proto_jin_app_id: str
    self_splitter_app_id: str
    unconscious_app_id: str

    #多体讨论要用的agent
    jinguji_app_id:str
    fujii_app_id:str
    yamada_app_id:str
    yamamoto_app_id:str
    fujisaki_app_id:str
    nakamura_app_id:str
    tanaka_app_id:str
    takahash_app_id:str
    sato_app_id:str
    
    #
    allowed_origins: str
    
    class Config:
        env_file = ".env"

settings = Settings()

print("Loaded settings:", settings.dict())  # 查看完整设置

app = FastAPI()
# 替换原来的 origin 处理
origins = [origin.strip() for origin in settings.allowed_origins.split(",")]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.middleware("http")
async def log_origin(request: Request, call_next):
    origin = request.headers.get("origin")
    method = request.method
    print(f"Request Origin: {origin} | Method: {method}")
    response = await call_next(request)
    return response
# 在app.add_middleware之后添加
print("Current allowed origins:", origins)
CONFIG_MAP = {
    "only-translate": {
        "api_key": settings.chat_agent_api_key,
        "app_id": settings.only_translate_app_id
    },
    "zero": {
        "api_key": settings.chat_agent_api_key,
        "app_id": settings.zero_app_id
    },
    "soul": {
        "api_key": settings.chat_agent_api_key,
        "app_id": settings.soul_app_id
    },
    "misheard": {  
        "api_key": settings.chat_agent_api_key,
        "app_id": settings.misheard_app_id
    },
    "correction": {  
        "api_key": settings.chat_agent_api_key,
        "app_id": settings.correction_app_id
    },
    "game-misheard": {
        "api_key": settings.chat_agent_api_key,
        "app_id": settings.game_misheard_app_id
    },
    "game-word": {
        "api_key": settings.chat_agent_api_key,
        "app_id": settings.game_word_app_id
    },
    "culture": {
        "api_key": settings.chat_agent_api_key,
        "app_id": settings.culture_app_id
    },
    "dialect": {
        "api_key": settings.chat_agent_api_key,
        "app_id": settings.dialect_app_id
    },
    "super-translate": {
        "api_key": settings.chat_agent_api_key,
        "app_id": settings.super_translate_app_id
    },
    "stem":{
        "api_key":settings.chat_agent_api_key,
        "app_id":settings.stem_app_id
    },
        "dream-weaver": {
        "api_key": settings.chat_agent_api_key,
        "app_id": settings.dream_weaver_app_id
    },
    "fantasy-master": {
        "api_key": settings.chat_agent_api_key,
        "app_id": settings.fantasy_master_app_id
    },
    "glitch-space": {
        "api_key": settings.chat_agent_api_key,
        "app_id": settings.glitch_space_app_id
    },
    "ln-factory": {
        "api_key": settings.chat_agent_api_key,
        "app_id": settings.ln_factory_app_id
    },
    "proto-jin": {
        "api_key": settings.chat_agent_api_key,
        "app_id": settings.proto_jin_app_id
    },
    "self-splitter": {
        "api_key": settings.chat_agent_api_key,
        "app_id": settings.self_splitter_app_id
    },
    "unconscious": {
        "api_key": settings.chat_agent_api_key,
        "app_id": settings.unconscious_app_id
    },
    "jinguji": {
        "api_key": settings.chat_agent_api_key,
        "app_id": settings.jinguji_app_id
    },
    "fujii": {
        "api_key": settings.chat_agent_api_key,
        "app_id": settings.fujii_app_id
    },
    "yamada": {
        "api_key": settings.chat_agent_api_key,
        "app_id": settings.yamada_app_id
    },
    "yamamoto": {
        "api_key": settings.chat_agent_api_key,
        "app_id": settings.yamamoto_app_id
    },
    "fujisaki": {
        "api_key": settings.chat_agent_api_key,
        "app_id": settings.fujisaki_app_id
    },
    "nakamura": {
        "api_key": settings.chat_agent_api_key,
        "app_id": settings.nakamura_app_id
    },
    "tanaka": {
        "api_key": settings.chat_agent_api_key,
        "app_id": settings.tanaka_app_id
    },
    "takahashi": {
        "api_key": settings.chat_agent_api_key,
        "app_id": settings.takahash_app_id
    },
    "sato": {
        "api_key": settings.chat_agent_api_key,
        "app_id": settings.sato_app_id
    }
}

async def generate_stream(prompt_text: str, config: dict) -> AsyncGenerator[str, None]:
    responses = Application.call(
        api_key=config['api_key'],
        app_id=config['app_id'],
        prompt=prompt_text,  # 使用拼接后的完整prompt
        stream=True,
        incremental_output=True
    )
    
    try:
        for response in responses:
            if response.status_code == 200:
                # 修正字段路径（根据实际API响应结构）
                content = response.output.text  # 阿里云百炼的标准响应字段
                yield json.dumps({
                    "content": content,
                    "finished": False
                }) + "\n"
                await asyncio.sleep(0)  # 让出事件循环
            else:
                raise HTTPException(status_code=response.status_code, detail=response.message)
    except Exception as e:
        yield json.dumps({
            "error": str(e),
            "finished": True
        }) + "\n"



@app.api_route("/api/process", methods=["POST", "OPTIONS"])
async def process_request(request: Request):
    # 只处理 POST，OPTIONS 由 CORS 中间件自动处理，无需你管
    data = await request.json()
    input_text = data.get("inputText")
    agent_mode = data.get("agentMode")
    history = data.get("history", [])
    if not input_text or not agent_mode:
        raise HTTPException(status_code=400, detail="Invalid params")

    config = CONFIG_MAP.get(agent_mode)
    if not config:
        raise HTTPException(status_code=400, detail="Invalid mode")

    # 拼接历史消息作为 prompt
    prompt = ""
    for msg in history:
        prompt += f"{msg['role']}: {msg['content']}\n"
    prompt += f"user: {input_text}\nassistant:"
    return StreamingResponse(
        generate_stream(prompt, config),
        media_type="application/x-ndjson"
    )
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=3000,
    )