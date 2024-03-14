import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
from internal.utils.logger import logger

class STT():
    def __init__(self, model_name = "distil-whisper/distil-large-v2"):
    # def __init__(self, model_name = "distil-whisper/distil-medium.en"):
        logger.debug(f"Loading Model: {model_name}")
        device = "cuda:0" if torch.cuda.is_available() else "cpu"
        torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32
        model = AutoModelForSpeechSeq2Seq.from_pretrained(
            model_name, torch_dtype=torch_dtype, low_cpu_mem_usage=True, use_safetensors=True
        ).to(device)
        logger.debug("Model Loaded...")
        processor = AutoProcessor.from_pretrained(model_name)
        self.pipe = pipeline(
            "automatic-speech-recognition",
            model=model,
            tokenizer=processor.tokenizer,
            feature_extractor=processor.feature_extractor,
            max_new_tokens=128,
            torch_dtype=torch_dtype,
            device=device,
        )
        logger.debug("STT pipeline created...")

    def run(self, audio_data):
        logger.debug("Predicting text from audio...")
        #write audio data to a text file
        return self.pipe(audio_data)["text"]

