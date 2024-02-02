from event_bus import EventBus
from audio_capture import LiveTranscriber
from cv_env import GameEnvironment
from threading import Thread
from time import sleep

def start():
    bus = EventBus()
    user_listener = LiveTranscriber(bus=bus)
    listener = Thread(target=user_listener.transcribe)
    
    env = GameEnvironment(bus=bus)
    game = Thread(target=env.render_game)

    listener.start()
    game.start()
    
    game.join()
    # keep listening for few more seconds before shutting down
    sleep(2)
    user_listener.stop()
    listener.join()

    bus.serialize('events_dir')

start()