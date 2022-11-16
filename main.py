import pygame
import pygame.freetype
from pygame.sprite import Sprite
from pygame.rect import Rect
from enum import Enum
from pygame.sprite import RenderUpdates
import sys
import time

#Colors used in the program 
BLUE = (106, 159, 181)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 204, 0)
GREY = (128, 128, 128)
BLACK = (0, 0, 0)


def create_surface_with_text(text, font_size, text_rgb, bg_rgb):
    """ Returns surface with text written on """
    font = pygame.freetype.SysFont("Courier", font_size, bold=True)
    surface, _ = font.render(text=text, fgcolor=text_rgb, bgcolor=bg_rgb)
    return surface.convert_alpha()


class UIElement(Sprite):
    """ An user interface element that can be added to a surface """

    def __init__(self, center_position, text, font_size, bg_rgb, text_rgb, action=None):
        """
        Args:
            center_position - tuple (x, y)
            text - string of text to write
            font_size - int
            bg_rgb (background colour) - tuple (r, g, b)
            text_rgb (text colour) - tuple (r, g, b)
            action - the gamestate change associated with this button
        """
        self.mouse_over = False

        default_image = create_surface_with_text(
            text=text, font_size=font_size, text_rgb=text_rgb, bg_rgb=bg_rgb
        )

        highlighted_image = create_surface_with_text(
            text=text, font_size=font_size * 1.2, text_rgb=text_rgb, bg_rgb=bg_rgb
        )

        self.images = [default_image, highlighted_image]

        self.rects = [
            default_image.get_rect(center=center_position),
            highlighted_image.get_rect(center=center_position),
        ]

        self.action = action

        super().__init__()

    @property
    def image(self):
        return self.images[1] if self.mouse_over else self.images[0]

    @property
    def rect(self):
        return self.rects[1] if self.mouse_over else self.rects[0]

    def update(self, mouse_pos, mouse_up):
        """ Updates the mouse_over variable and returns the button's
            action value when clicked.
        """
        if self.rect.collidepoint(mouse_pos):
            self.mouse_over = True
            if mouse_up:
                return self.action
        else:
            self.mouse_over = False

    def draw(self, surface):
        """ Draws element onto a surface """
        surface.blit(self.image, self.rect)

class Player:
    """ Stores information about a player """

    def __init__(self, score=0, lives=3, current_level=1):
        self.score = score
        self.lives = lives
        self.current_level = current_level


def main():
    pygame.init()

    screen = pygame.display.set_mode((800, 600))
    game_state = GameState.TITLE

    while True:
        if game_state == GameState.TITLE:
            game_state = title_screen(screen)

        if game_state == GameState.NEWGAME:
            player = Player()
            game_state = level_1(screen, player)

        if game_state == GameState.NEXT_LEVEL_2:
            player.current_level += 1
            game_state = level_2(screen, player)

        if game_state == GameState.NEXT_LEVEL_3:
          player.current_level += 1
          game_state = level_3(screen, player)
        
        if game_state == GameState.BETWEEN:
            game_state = between_levels(screen)

        if game_state == GameState.FAIL_SCREEN1:
          game_state = fail_screen1(screen)

        if game_state == GameState.FAIL_SCREEN2:
          game_state = fail_screen2(screen)

        if game_state == GameState.QUIT:
            pygame.quit()
            return


def title_screen(screen): # Title Screen 
    title_btn = UIElement(
      center_position = (400,200),
      font_size = 50,
      bg_rgb = BLUE,
      text_rgb = WHITE,
      text = "The World's Easiest Game",
      action = None,
    )
    start_btn = UIElement(
        center_position=(400, 350),
        font_size=30,
        bg_rgb=BLUE,
        text_rgb=WHITE,
        text="Start",
        action=GameState.NEWGAME,
    )
    quit_btn = UIElement(
        center_position=(400, 450),
        font_size=30,
        bg_rgb=BLUE,
        text_rgb=WHITE,
        text="Quit",
        action=GameState.QUIT,
    )

    buttons = RenderUpdates(title_btn, start_btn, quit_btn)

    return game_loop(screen, buttons)

def fail_screen1(screen): # Fail Screen for Level 1
    title_btn = UIElement(
      center_position = (400,200),
      font_size = 30,
      bg_rgb = RED,
      text_rgb = WHITE,
      text = "You touched the button didn't you...",
      action = None,
    )
    startAgain_btn = UIElement(
        center_position=(400, 350),
        font_size=30,
        bg_rgb= BLUE,
        text_rgb= WHITE,
        text="Restart",
        action=GameState.NEWGAME,
    )
    quit_btn = UIElement(
        center_position=(400, 450),
        font_size=30,
        bg_rgb= BLUE,
        text_rgb= WHITE,
        text="Quit",
        action=GameState.QUIT,
    )
    return_btn = UIElement(
        center_position = (400, 400),
        font_size = 30, 
        bg_rgb = BLUE,
        text_rgb = WHITE,
        text = "Return to Home",
        action = GameState.TITLE,
    )

    buttons = RenderUpdates(title_btn, startAgain_btn, quit_btn, return_btn)

    return game_loop(screen, buttons)

def fail_screen2(screen): # Fail Screen for Level 2
    title_btn = UIElement(
      center_position = (400,200),
      font_size = 30,
      bg_rgb = RED,
      text_rgb = WHITE,
      text = "Really Dig Deep... You Can Do It",
      action = None,
    )
    startAgain_btn = UIElement(
        center_position=(400, 350),
        font_size=30,
        bg_rgb= BLUE,
        text_rgb= WHITE,
        text="Restart",
        action=GameState.NEWGAME,
    )
    quit_btn = UIElement(
        center_position=(400, 450),
        font_size=30,
        bg_rgb= BLUE,
        text_rgb= WHITE,
        text="Quit",
        action=GameState.QUIT,
    )
    return_btn = UIElement(
        center_position = (400, 400),
        font_size = 30, 
        bg_rgb = BLUE,
        text_rgb = WHITE,
        text = "Return to Home",
        action = GameState.TITLE,
    )

    buttons = RenderUpdates(title_btn, startAgain_btn, quit_btn, return_btn)

    return game_loop(screen, buttons)


def level_1(screen, player): # Level 1
    return_btn = UIElement(
        center_position=(50, 570),
        font_size=20,
        bg_rgb=BLUE,
        text_rgb=WHITE,
        text="Return",
        action=GameState.TITLE,
    )
    
    nextlevel_btn = UIElement(
        center_position=(670, 570),
        font_size=20,
        bg_rgb=BLUE,
        text_rgb=WHITE,
        text=f"Next level ({player.current_level + 1})",
        action=GameState.NEXT_LEVEL_2,
    )
  
    currentlevel_btn = UIElement(
        center_position = (120,20),
        font_size = 20,
        bg_rgb = BLUE,
        text_rgb = WHITE,
        text = f"Current level ({player.current_level})",
        action = None,
    )
  
    red_btn = UIElement(
        center_position = (200,300),
        font_size = 40,
        bg_rgb = RED,
        text_rgb = WHITE,
        text = "DO NOT PRESS",
        action = GameState.FAIL_SCREEN1,
    )
    
    green_btn = UIElement(
      center_position = (600,300),
      font_size = 40,
      bg_rgb = GREEN,
      text_rgb = WHITE,
      text = "Press",
      action = GameState.NEXT_LEVEL_2,
    )
   # for i in range(0,1):
      #play_level.green_btn.hide()#print(green_btn) #button.hide()???
     # time.sleep(1)

    buttons = RenderUpdates(return_btn, nextlevel_btn, currentlevel_btn, red_btn, green_btn)

    return game_loop(screen, buttons)

def level_2(screen, player): # Level 2
  return_btn = UIElement(
        center_position=(50, 570),
        font_size=20,
        bg_rgb=BLUE,
        text_rgb=WHITE,
        text="Return",
        action=GameState.TITLE,
    )
  nextlevel_btn = UIElement(
        center_position=(670, 570),
        font_size=20,
        bg_rgb=BLUE,
        text_rgb=WHITE,
        text=f"Next level ({player.current_level + 1})",
        action=GameState.NEXT_LEVEL_3,
    )
  currentlevel_btn = UIElement(
        center_position = (120,20),
        font_size = 20,
        bg_rgb = BLUE,
        text_rgb = WHITE,
        text = f"Current level ({player.current_level})",
        action = None,
    )
  answer_btn = UIElement(
        center_position = (300, 150),
        font_size = 40,
        bg_rgb = BLUE, 
        text_rgb = WHITE,
        text = "Click the answer: ",
        action = GameState.NEXT_LEVEL_3,
  )
  equation_btn = UIElement(
        center_position = (350, 250),
        font_size = 30,
        bg_rgb = BLUE, 
        text_rgb = WHITE, 
        text = "1 + 2 + 3 - 5 * 20 = _____",
        action = None,
  )
  eqAnswer1_btn = UIElement(
        center_position = (150, 375),
        font_size = 30,
        bg_rgb = BLUE,
        text_rgb = WHITE,
        text = "94",
        action = GameState.FAIL_SCREEN2,
  )
  eqAnswer2_btn = UIElement(
        center_position = (250, 350),
        font_size = 30,
        bg_rgb = BLUE,
        text_rgb = WHITE,
        text = "61",
        action = GameState.FAIL_SCREEN2,
  )
  eqAnswer3_btn = UIElement(
        center_position = (350, 375),
        font_size = 30,
        bg_rgb = BLUE,
        text_rgb = WHITE,
        text = "-95",
        action = GameState.FAIL_SCREEN2,
  )
  eqAnswer4_btn = UIElement(
        center_position = (450, 350),
        font_size = 30,
        bg_rgb = BLUE,
        text_rgb = WHITE,
        text = "-94",
        action = GameState.FAIL_SCREEN2,
  )
  eqAnswer5_btn = UIElement(
        center_position = (550, 375),
        font_size = 30,
        bg_rgb = BLUE,
        text_rgb = WHITE,
        text = "20",
        action = GameState.FAIL_SCREEN2,
  )
  
  buttons = RenderUpdates(return_btn, nextlevel_btn, currentlevel_btn, answer_btn, equation_btn, eqAnswer1_btn, eqAnswer2_btn,eqAnswer3_btn, eqAnswer4_btn, eqAnswer5_btn)

  return game_loop(screen, buttons)

def level_3(screen, player): # Level 3
  return_btn = UIElement(
        center_position=(50, 570),
        font_size=20,
        bg_rgb=BLUE,
        text_rgb=WHITE,
        text="Return",
        action=GameState.TITLE,
    )
  nextlevel_btn = UIElement(
        center_position=(670, 570),
        font_size=20,
        bg_rgb=BLUE,
        text_rgb=WHITE,
        text=f"Next level ({player.current_level + 1})",
        action=GameState.NEXT_LEVEL_3,
    )
  currentlevel_btn = UIElement(
        center_position = (120,20),
        font_size = 20,
        bg_rgb = BLUE,
        text_rgb = WHITE,
        text = f"Current level ({player.current_level})",
        action = None,
    )
  
  buttons = RenderUpdates(return_btn, nextlevel_btn, currentlevel_btn)

  return game_loop(screen, buttons)


def between_levels(screen):
  continue_btn = UIElement(
        center_position=(400, 350),
        font_size=30,
        bg_rgb=BLUE,
        text_rgb=WHITE,
        text="Continue",
        action=GameState.NEXT_LEVEL,
  )
  next_btn = UIElement(
        center_position = (400,200),
        font_size = 50,
        bg_rgb = BLUE,
        text_rgb = WHITE,
        text = "You did it!",
        action = None,
  )

  quit_btn = UIElement(
        center_position=(400, 450),
        font_size=30,
        bg_rgb=BLUE,
        text_rgb=WHITE,
        text="Quit",
        action=GameState.QUIT,
    )

  buttons = RenderUpdates(next_btn, continue_btn, quit_btn)

  return game_loop(screen, buttons)

def game_loop(screen, buttons):
    """ Handles game loop until an action is return by a button in the
        buttons sprite renderer.
    """
    while True:
        mouse_up = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True
        screen.fill(BLUE)

        for button in buttons:
            ui_action = button.update(pygame.mouse.get_pos(), mouse_up)
            if ui_action is not None:
                return ui_action

        buttons.draw(screen)
        pygame.display.flip()


class GameState(Enum):
    QUIT = -1
    TITLE = 0
    NEWGAME = 1
    NEXT_LEVEL_2 = 2
    NEXT_LEVEL_3 = 3
    FAIL_SCREEN1 = 4
    FAIL_SCREEN2 = 5
    BETWEEN = 6

if __name__ == "__main__":
    main()