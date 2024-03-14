from internal.server.pubsub import RedisPubSub

class App:
    def __init__(self) -> None:
        self.redis = RedisPubSub()

    def run(self):
        self.redis.serve()