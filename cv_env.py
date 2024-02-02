import numpy as np
import cv2
import random
from event_bus import EventBus, Event


class GameEnvironment:
    def __init__(self, num_cookies=5, bus=None):
        self.width, self.height = 20, 20  # Size of the playing area
        self.box_position = [0, 0]
        
        self.cookie_names = 'abcdefghijklmnopqrstuvwxyz'.upper()[:num_cookies]

        rloc = lambda : random.randint(1, self.width-1)
        
        self.cookies = {name: [(rloc()//4)*4, (rloc()//4)*4] for name in self.cookie_names}
        self.current_cookie = self.cookie_names[0]
        self.score = 0
        self.game_over = False

        self.bus = bus

    def get_state(self):
        """Returns the current state of the game."""
        return {
            'box_position': self.box_position,
            'cookies': self.cookies,
            'current_cookie': self.current_cookie,
            'score': self.score
        }

    def step(self, action):
        action_event = Event(type='action', text=action)
        self.bus.push_event(action_event)

        """Updates the game state based on the action."""
        if action == 'up' and self.box_position[1] > 0:
            self.box_position[1] -= 4
        elif action == 'down' and self.box_position[1] < self.height - 1:
            self.box_position[1] += 4
        elif action == 'left' and self.box_position[0] > 0:
            self.box_position[0] -= 4
        elif action == 'right' and self.box_position[0] < self.width - 1:
            self.box_position[0] += 4

        if self.box_position == self.cookies[self.current_cookie]:
            del self.cookies[self.current_cookie]
            self.score += 1
            if self.score < len(self.cookie_names):
                self.current_cookie = self.cookie_names[self.score]

        if not self.cookies:
            self.game_over = True

        state = Event(type='state', image=self.render(), text=self.get_state())
        self.bus.push_event(state)
        
        return self.get_state()

    def render(env):
        screen_width = 1000
        img = np.zeros((screen_width, screen_width, 3), dtype=np.uint8)
        step_size = screen_width // env.width
        box_x, box_y = env.box_position
        cv2.rectangle(img, (box_x*step_size, box_y*step_size), ((box_x+1)*step_size, (box_y+1)*step_size), (255, 255, 255), 2)

        for cookie, pos in env.cookies.items():
            color = (0, 255, 0)
            if cookie == env.current_cookie:
                color = (0, 0, 255)
            
            cv2.circle(img, (pos[0]*step_size+ step_size//2, pos[1]*step_size + step_size//2), 10, color, -1)

        return img

    def render_game(env):
        window_name = 'Game'
        cv2.namedWindow(window_name)
        
        while not env.game_over:
            img = env.render()
            cv2.imshow(window_name, img)
            
            key = cv2.waitKey(10) & 0xFF

            if key == 27:  # ESC key to exit
                break
            elif key == 82 or key == 119:  # Up arrow or 'w'
                env.step('up')
            elif key == 84 or key == 115:  # Down arrow or 's'
                env.step('down')
            elif key == 81 or key == 97:  # Left arrow or 'a'
                env.step('left')
            elif key == 83 or key == 100:  # Right arrow or 'd'
                env.step('right')
        
        cv2.destroyAllWindows()