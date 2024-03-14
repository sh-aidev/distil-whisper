import redis
import os
import sys, time
from internal.utils.logger import logger
from internal.utils.config import Config
from internal.core.audio_src import  AudioSrc
from internal.core.stt import STT
from internal.utils.textformat import ANSI_RESET, ANSI_BOLD, ANSI_MAGENTA, ANSI_ITALIC

class RedisPubSub():
    def __init__(self):
        root_config_dir = "configs"

        logger.debug(f"Root config dir: {root_config_dir}")

        self.config = Config(root_config_dir)
        logger.debug("Configs Loaded...")
        
        self.stt = STT(model_name = self.config.whisper.stt_model.model_name)
        logger.debug("STT Initialized...")
        self.audio_src = AudioSrc()

        logger.debug(
            f"Connecting to Redis at: http://{os.getenv('REDIS_HOST', 'localhost')}:{os.getenv('REDIS_PORT', self.config.whisper.server.redis_port)}"
        )
        try:
            self.channel_name = self.config.whisper.server.whisper_channel_name
            self.client = redis.Redis(
                host=os.getenv('REDIS_HOST', 'localhost'),
                port=os.getenv('REDIS_PORT', self.config.whisper.server.redis_port)
            )
            logger.debug("Connected to redis...")
        except:
            logger.error("Not able to connect to Redis")
            sys.exit(0)
        logger.info("Distil Whisper Server Initialized...")
    
    def serve(self):
        while True:
            audio_data = self.audio_src()
            text = self.stt.run(audio_data)
            print("\n")
            sys.stdout.write(ANSI_BOLD + ANSI_ITALIC + ANSI_MAGENTA)
            self.print_with_typing_effect(text, 0.05)
            sys.stdout.write(ANSI_RESET)
            # logger.info(f"Predicted Output: {self.print_with_typing_effect(text, 0.05)}")
            self.client.publish(self.channel_name, str(text))
    
    @staticmethod
    def print_with_typing_effect(text, delay):
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(delay)