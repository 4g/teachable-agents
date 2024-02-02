from queue import Queue
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import numpy as np

@dataclass
class Event: 
    type: str
    text: str = None
    image: np.ndarray = None

    timestamp: str = "00:00:00"
    

class EventBus:
    def __init__(self, logger='bus.log') -> None:
        self.queue = Queue(maxsize=100000)
        self.stopped = False
    
    def get_timestamp(self):
        return str(datetime.now())

    def stop(self):
        self.stopped = True

    def push_event(self, event: Event):
        if self.stopped:
            raise
        event.timestamp = self.get_timestamp()
        self.queue.put(event)
        print(f"{event.timestamp}:{event.type}:{event.text}")
    
    def serialize(self, dir):
        dir = Path(dir)
        dir.mkdir(exist_ok=True, parents=True)

        while not self.queue.empty():
            

        
