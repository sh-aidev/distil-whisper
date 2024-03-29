import numpy as np
from internal.utils.logger import logger

class NoiseCheck:
    @staticmethod
    def __call__( audio_chunk: np.array ) :
        average = sum(map(abs, audio_chunk))/ len(audio_chunk)
        # logger.debug(f"Audio Chunk details => Sum: {sum(audio_chunk)}, Length: {len(audio_chunk)}, Average value: {average}")

        return True if (average > 1000 or average < 100) else False

