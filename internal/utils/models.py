from pydantic import BaseModel

class LoggerModel(BaseModel):
    environment: str

class ServerModel(BaseModel):
    redis_port: str
    whisper_channel_name: str

class STTModel(BaseModel):
    model_name: str

class Model(BaseModel):
    logger: LoggerModel
    server: ServerModel
    stt_model: STTModel