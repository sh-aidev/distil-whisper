import pyaudio
from typing import Optional
import numpy as np
import scipy.signal as sps

from internal.utils.noise_check import NoiseCheck
from internal.utils.logger import logger

class AudioSrc:
    def __init__(
        self, 
        mic_name: str ="USB Audio Device:", 
        inrate: int = 44100, 
        channels: int = 1, 
        width: int = 2, 
        chunk_size: int = 1024, 
        duration: int = 1000 # in ms
        ):
        self.inrate = inrate
        # self.vad = VADDetector()
        self._isNoise = NoiseCheck()
        self.chunk_size = chunk_size
        self.outrate = 16000
        self.channels = channels
        self.mic_name = mic_name
        self.no_of_chunk = int((inrate/self.chunk_size) * (duration / 1000))
        self.storage = []
        paudio = pyaudio.PyAudio()
        
        speaker_idx = self.get_speaker_index(paudio)

        if speaker_idx is None:
            logger.debug("Could not find the mentioned Mic attached")
            raise ValueError("Could not find the mentioned Mic attached")

        self.stream = paudio.open(
            rate=inrate,
            format=paudio.get_format_from_width(width),
            channels=channels,
            input=True,
            input_device_index=speaker_idx,
        )
        logger.debug("PyAudio stream initialized")
        self.paudio = paudio
        self.counter = 0
        self.done = False
        self.is_first = False
        self.memory = []


    def get_speaker_index(self, paudio) -> Optional[int]:
        num_devices = paudio.get_host_api_info_by_index(0).get("deviceCount")
        for i in range(0, num_devices):
            # print(self.paudio.get_device_info_by_host_api_device_index(0, i).get("name"))
            if (
                self.mic_name
                in paudio.get_device_info_by_host_api_device_index(0, i).get("name")
            ):
                logger.debug(f"Got speaker index for {paudio.get_device_info_by_host_api_device_index(0, i).get('name')}: {i}")
                return i

    def __call__(self):
        self.done = False
        while not self.done:
            audio_chunk = np.frombuffer(
                self.stream.read(self.chunk_size, exception_on_overflow=False),
                dtype=np.int16,
            )[0::self.channels]
            # print(f"audio_chunk shape: {audio_chunk.shape}")
            no_of_samples = int(len(audio_chunk) * float(self.outrate) / self.inrate)
            audio_chunk = np.array(sps.resample(audio_chunk, no_of_samples), dtype=np.int16)
            is_noise = self._isNoise(audio_chunk)
            if not is_noise:
                self.is_first = True

            if self.is_first:
                self.memory.append(audio_chunk)
                self.counter = self.counter + 1 if is_noise else 0
                # logger.debug(f"noise check: {is_noise}, counter: {self.counter}, no_of_chunk: {self.no_of_chunk}, memory length: {len(self.memory)}")
                if self.counter > self.no_of_chunk:
                    self.is_first = False
                    self.counter = 0
                    self.done = True
                    self.audio = np.concatenate(self.memory)
                    self.memory = []
                    self.audio = np.array(self.audio) / np.max(np.abs(self.audio))
                    return {"path": "", "array": self.audio, "sampling_rate": self.outrate}


    def stop(self):
        self.stream.stop_stream()
        self.stream.close()
        self.paudio.terminate()