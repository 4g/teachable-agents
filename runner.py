from event_bus import EventBus
from audio_capture import LiveTranscriber
from cv_env import GameEnvironment
from threading import Thread

def start():
    bus = EventBus()
    user_listener = LiveTranscriber(bus=bus)
    listener = Thread(target=user_listener.transcribe)
    
    env = GameEnvironment(bus=bus)
    game = Thread(target=env.render_game)

    listener.start()
    game.start()
    
    game.join()
    user_listener.stop()
    listener.join()

start()