from loguru import logger
import sys


# # init logger with custom config
class Logger:
    @staticmethod
    def create_sess(env):
        logger.remove()
        logger.add(
            "logs/server.log",
            format="{time} {level} {message}",
            rotation="10 MB",
            compression="zip",
            serialize=True,
        )
        env_dict = {"dev": "DEBUG", "prod": "INFO"}
        logger.add(sys.stderr, level=env_dict[env])
        return logger
