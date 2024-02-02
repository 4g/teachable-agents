from queue import Queue
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import numpy as np
import cv2
import json

@dataclass
class Event: 
    type: str
    text: str = "None"
    image: np.ndarray = None

    timestamp: str = "00:00:00"
    
class EventBus:
    def __init__(self, log_dir=None):
        self.queue = Queue(maxsize=100000)
        self.stopped = False
        self.log_dir = log_dir
        self.event_index = 0
        
        if self.log_dir:
            self.prepare_logger(self.log_dir)
    
    def get_timestamp(self):
        return str(datetime.now())

    def stop(self):
        self.stopped = True

    def push_event(self, event: Event):
        if self.stopped:
            raise
        event.timestamp = self.get_timestamp()
        self.queue.put(event)
        self.log_event(event=event)

    def log_event(self, event):
        if self.log_dir is None:
            return 
        
        if self.log_dir == 'stdin':
            print(f"{event.timestamp}:{event.type}:{event.text}")
        
        else:
            event = self.queue.get()
            image_path = None

            if event.image is not None:
                image_path = str(self.images_dir / f'{self.event_index}.png')
                cv2.imwrite(image_path, event.image)
                self.event_index += 1
            
            serial_event = {'type': event.type,
                'text': event.text,
                'timestamp': event.timestamp,
                'image': image_path
                }
            
            serial_event_json = json.dumps(serial_event) + "\n"
            self.logfile.write(serial_event_json)


    def prepare_logger(self, dir):
        dir = Path(dir)
        dir.mkdir(exist_ok=True, parents=True)

        self.logfile = open(dir / 'events.log', 'w')
        self.images_dir = dir / 'images/'

        self.images_dir.mkdir(exist_ok=True, parents=True)