# This is an absolutely shit program and no hiring managers should ever lay eyes on this garbage

# Import and initialize the pygame library
import pygame
from enum import Enum
from threading import Timer

pygame.init()

class Skill(Enum):
  NONE = 0
  SINGLE = 1
  MEN_SHORI = 2
  FUCHI_SHORI = 3
  DOKA_SHORI = 4
  KADO_SHORI = 5

class Inputs(Enum):
  NONE = 0
  KA_LEFT = 1
  DON_LEFT = 2
  DON_RIGHT = 3
  KA_RIGHT = 4
# Set up the drawing window
screen = pygame.display.set_mode([1280, 720])
pygame.display.set_caption("Taiko Practice Tool")

class KeyBindings:
  def __init__(self):
    self.ka_left = 'd'
    self.don_left = 'f'
    self.don_right = 'j'
    self.ka_right = 'k'

  def get_all_bindings(self):
    return {
      'ka_left': self.ka_left,
      'don_left': self.don_left,
      'don_right': self.don_right,
      'ka_right': self.ka_right
    }

running = True
previous_stroke: Inputs = Inputs.NONE
current_skill: Skill = Skill.NONE
current_pressed_count = 0
ren_count = 0
shori_next_has_to_switch = False #for men/fuchi shori
is_failed_state = False
fail_cause = ''

binds = KeyBindings()

def isGoodHit(inputKey: str) -> (bool, str):
  global current_skill, previous_stroke, shori_next_has_to_switch #I'm going to kill myself
  match inputKey:
    case binds.ka_left:
      match current_skill:
        case Skill.NONE:
          match previous_stroke:
            case Inputs.KA_LEFT:
              current_skill = Skill.FUCHI_SHORI
              shori_next_has_to_switch = True
            case Inputs.DON_LEFT:
              current_skill = Skill.DOKA_SHORI
            case Inputs.DON_RIGHT | Inputs.KA_RIGHT:
              current_skill = Skill.SINGLE
        case Skill.SINGLE:  # As long as previous input != same side as current input
          if previous_stroke == Inputs.KA_LEFT or previous_stroke == Inputs.DON_LEFT:
            return False, 'LK SINGLE: Bad - Left twice'
        case Skill.MEN_SHORI:  # Fuchi input on men shori
          return False, 'LK MS: Bad - Fuchi on Men Shori'
        case Skill.FUCHI_SHORI:
          match previous_stroke:
            case Inputs.KA_LEFT:
              if shori_next_has_to_switch:
                return False, "LK FS: Bad - 3 Fuchi in a row"
              else:  # kk pattern (next has to be right k
                shori_next_has_to_switch = True
            case Inputs.KA_RIGHT:
              if not shori_next_has_to_switch:
                return False, "LK FS: Bad - 1 fuchi on right before switch"
              else:  # switch successful
                shori_next_has_to_switch = False
        case Skill.KADO_SHORI:
          if previous_stroke != Inputs.DON_RIGHT:
            return False, "LK KD: Bad - incorrect left fuchi hit"
        case Skill.DOKA_SHORI:
          if previous_stroke != Inputs.DON_LEFT:
            return False, "LK DK: Bad - incorrect left fuchi hit"
      previous_stroke = Inputs.KA_LEFT
    case binds.don_left:
      match current_skill:
        case Skill.NONE:
          match previous_stroke:
            case Inputs.KA_LEFT:
              current_skill = Skill.KADO_SHORI
            case Inputs.DON_LEFT:
              current_skill = Skill.MEN_SHORI
              shori_next_has_to_switch = True
            case Inputs.DON_RIGHT | Inputs.KA_RIGHT:
              current_skill = Skill.SINGLE
        case Skill.SINGLE:  # As long as previous input != same side as current input
          if previous_stroke == Inputs.KA_LEFT or previous_stroke == Inputs.DON_LEFT:
            return False, 'LD SINGLE: Bad - Left twice'
        case Skill.MEN_SHORI:
          match previous_stroke:
            case Inputs.DON_LEFT:
              if shori_next_has_to_switch:
                return False, "LD MS: Bad - 3 Men in a row"
              else:  # kk pattern (next has to be right k
                shori_next_has_to_switch = True
            case Inputs.DON_RIGHT:
              if not shori_next_has_to_switch:
                return False, "LD MS: Bad - 1 men on right before switch"
              else:  # switch successful
                shori_next_has_to_switch = False
        case Skill.FUCHI_SHORI:
          return False, "LD FS: Bad - Men on FS"
        case Skill.KADO_SHORI:
          if previous_stroke != Inputs.KA_LEFT:
            return False, "LD KD: Bad - incorrect left men hit"
        case Skill.DOKA_SHORI:
          if previous_stroke != Inputs.KA_RIGHT:
            return False, "LD DK: Bad - incorrect left men hit"
      previous_stroke = Inputs.DON_LEFT
    case binds.don_right:
      match current_skill:
        case Skill.NONE:
          match previous_stroke:
            case Inputs.KA_RIGHT:
              current_skill = Skill.KADO_SHORI
            case Inputs.DON_RIGHT:
              current_skill = Skill.MEN_SHORI
              shori_next_has_to_switch = True
            case Inputs.DON_LEFT | Inputs.KA_LEFT:
              current_skill = Skill.SINGLE
        case Skill.SINGLE:  # As long as previous input != same side as current input
          if previous_stroke == Inputs.KA_RIGHT or previous_stroke == Inputs.DON_RIGHT:
            return False, 'RD SINGLE: Bad - RIGHT twice'
        case Skill.MEN_SHORI:
          match previous_stroke:
            case Inputs.DON_RIGHT:
              if shori_next_has_to_switch:
                return False, "RD MS: Bad - 3 Men in a row"
              else:  # kk pattern (next has to be LEFT k
                shori_next_has_to_switch = True
            case Inputs.DON_LEFT:
              if not shori_next_has_to_switch:
                return False, "RD MS: Bad - 1 men on LEFT before switch"
              else:  # switch successful
                shori_next_has_to_switch = False
        case Skill.FUCHI_SHORI:
          return False, "RD FS: Bad - Men on FS"
        case Skill.KADO_SHORI:
          if previous_stroke != Inputs.KA_RIGHT:
            return False, "RD KD: Bad - incorrect RIGHT men hit"
        case Skill.DOKA_SHORI:
          if previous_stroke != Inputs.KA_LEFT:
            return False, "RD DK: Bad - incorrect RIGHT men hit"
      previous_stroke = Inputs.DON_RIGHT
    case binds.ka_right:
      match current_skill:
        case Skill.NONE:
          match previous_stroke:
            case Inputs.KA_RIGHT:
              current_skill = Skill.FUCHI_SHORI
              shori_next_has_to_switch = True
            case Inputs.DON_RIGHT:
              current_skill = Skill.DOKA_SHORI
            case Inputs.DON_LEFT | Inputs.KA_LEFT:
              current_skill = Skill.SINGLE
        case Skill.SINGLE:  # As long as previous input != same side as current input
          if previous_stroke == Inputs.KA_RIGHT or previous_stroke == Inputs.DON_RIGHT:
            return False, 'RK SINGLE: Bad - RIGHT twice'
        case Skill.MEN_SHORI:  # Fuchi input on men shori
          return False, 'RK MS: Bad - Fuchi on Men Shori'
        case Skill.FUCHI_SHORI:  # previous guaranteed to be LEFT or RIGHT Fuchi
          match previous_stroke:
            case Inputs.KA_RIGHT:
              if shori_next_has_to_switch:
                return False, "RK FS: Bad - 3 Fuchi in a row"
              else:  # kk pattern (next has to be LEFT k
                shori_next_has_to_switch = True
            case Inputs.KA_LEFT:
              if not shori_next_has_to_switch:
                return False, "RK FS: Bad - 1 fuchi on LEFT before switch"
              else:  # switch successful
                shori_next_has_to_switch = False
        case Skill.KADO_SHORI:
          if previous_stroke != Inputs.DON_LEFT:
            return False, "RK KD: Bad - incorrect RIGHT fuchi hit"
        case Skill.DOKA_SHORI:
          if previous_stroke != Inputs.DON_RIGHT:
            return False, "RK DK: Bad - incorrect RIGHT fuchi hit"
      previous_stroke = Inputs.KA_RIGHT
  return True, ""

def render_text(text, font, color):
  return font.render(text, True, color)

def reset():
  global is_failed_state, previous_stroke, current_skill, ren_count
  is_failed_state = False
  previous_stroke = Inputs.NONE
  current_skill = Skill.NONE
  ren_count = 0

def fail(reason: str):
  global is_failed_state, fail_cause
  is_failed_state = True
  fail_cause = reason
  Timer(1, reset).start()

default_font = pygame.font.Font(None, 74)

#load images and shit

while running:
  screen.fill((255, 255, 255))
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
    elif event.type == pygame.KEYDOWN:
      current_pressed_count += 1
      key = pygame.key.name(event.key)
      #Practicing Zone vvv
      if is_failed_state: continue
      if key not in binds.get_all_bindings().values(): continue #Ignore non keys
      if current_pressed_count > 1:
        fail('Double Input')
        continue
      isGood, reason = isGoodHit(key)
      if not isGood:
        fail(reason)
      else:
        ren_count += 1
    elif event.type == pygame.KEYUP:
        current_pressed_count -= 1

  #Rendering text
  skill_face = render_text(str(current_skill), default_font, (0, 0, 0))
  count_face = render_text(f"{ren_count}", default_font, (0, 0, 0))
  screen.blit(skill_face, (50, 50))
  screen.blit(count_face, (50, 150))
  if is_failed_state:
    fail_face = render_text(f"Fail: {fail_cause}", default_font, (255, 0, 0))
    screen.blit(fail_face, (50, 250))
  pygame.display.flip()

pygame.quit()
