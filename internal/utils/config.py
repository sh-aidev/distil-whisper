import toml
import os
from internal.utils.models import Model

class Config:

    def __init__(self, root_config_path: str):
        self.whisper = Model(
            **toml.load(os.path.join(root_config_path, "config.toml"))
        )


