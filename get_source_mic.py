import pyaudio

paudio = pyaudio.PyAudio()

num_devices = paudio.get_host_api_info_by_index(0).get("deviceCount")

for i in range(0, num_devices):
    print(paudio.get_device_info_by_host_api_device_index(0, i).get("name"))
