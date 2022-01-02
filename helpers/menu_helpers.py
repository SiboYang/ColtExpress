from pygame import gfxdraw

from assets.color_constants import *
from assets.font_constants import *
from assets.game_constants import *


def text_objects(text, font, colour=BLACK):
    text_surface = font.render(text, True, colour)
    return text_surface, text_surface.get_rect()


def button(text, x, y, w, h, click, screen, inactive_colour=BLUE, active_colour=LIGHT_BLUE, text_colour=WHITE):
    mouse = pygame.mouse.get_pos()
    return_value = False
    if x < mouse[0] < x + w and y < mouse[1] < y + h:  # if mouse is hovering the button
        pygame.draw.rect(screen, active_colour, (x, y, w, h))
        if click and pygame.time.get_ticks() > 100:
            return_value = True
    else:
        pygame.draw.rect(screen, inactive_colour, (x, y, w, h))

    text_surf, text_rect = text_objects(text, pygame.font.Font(FONT_BOLD, int(0.55 * h)),
                                        colour=text_colour)
    text_rect.center = (int(x + w / 2), int(y + h / 2))
    screen.blit(text_surf, text_rect)
    return return_value

def button_alpha(text, x, y, w, h, click, screen, inactive_colour=BLUE, active_colour=LIGHT_BLUE, text_colour=WHITE):
    mouse = pygame.mouse.get_pos()
    return_value = False
    if x < mouse[0] < x + w and y < mouse[1] < y + h:  # if mouse is hovering the button
        # pygame.draw.rect(screen, active_colour, (x, y, w, h))
        pygame.gfxdraw.box(screen, pygame.Rect(x,y,w,h), active_colour)
        if click and pygame.time.get_ticks() > 100:
            return_value = True
    else:
        # rect = pygame.draw.rect(screen, inactive_colour, (x, y, w, h))
        pygame.gfxdraw.box(screen, pygame.Rect(x, y, w, h), inactive_colour)

    text_surf, text_rect = text_objects(text, pygame.font.Font(FONT_BOLD, int(0.55 * h)),
                                        colour=text_colour)
    text_rect.center = (int(x + w / 2), int(y + h / 2))
    screen.blit(text_surf, text_rect)
    return return_value

def draw_rectangle(surface, x, y, width, height, color):
    return pygame.draw.rect(surface, color, (x, y, width, height))


def draw_circle(surface, x, y, radius, color):
    pygame.gfxdraw.aacircle(surface, x, y, radius, color)
    pygame.gfxdraw.filled_circle(surface, x, y, radius, color)


def toggle_btn(text, x, y, w, h, click, screen, text_colour=BLACK, enabled=True, draw_toggle=True, blit_text=True,
               enabled_color=LIGHT_BLUE, disabled_color=GREY):
    mouse = pygame.mouse.get_pos()
    # draw_toggle and blit_text are used to reduce redundant drawing and blitting (improves quality)
    rect_height = h // 2
    if rect_height % 2 == 0:
        rect_height += 1
    if enabled and draw_toggle:
        pygame.draw.rect(screen, WHITE, (x + TOGGLE_WIDTH -
                                         h // 4, y, TOGGLE_ADJ + h, rect_height))
        pygame.draw.rect(screen, enabled_color,
                         (x + TOGGLE_WIDTH, y, TOGGLE_ADJ, rect_height))
        draw_circle(screen, int(x + TOGGLE_WIDTH),
                    y + h // 4, h // 4, enabled_color)
        draw_circle(screen, int(x + TOGGLE_WIDTH + TOGGLE_ADJ),
                    y + h // 4, h // 4, enabled_color)
        draw_circle(screen, int(x + TOGGLE_WIDTH + TOGGLE_ADJ),
                    y + h // 4, h // 5, WHITE)  # small inner circle
    elif draw_toggle:
        pygame.draw.rect(screen, WHITE, (x + TOGGLE_WIDTH -
                                         h // 4, y, TOGGLE_ADJ + h, rect_height))
        pygame.draw.rect(screen, disabled_color,
                         (x + TOGGLE_WIDTH, y, TOGGLE_ADJ, rect_height))
        draw_circle(screen, int(x + TOGGLE_WIDTH),
                    y + h // 4, h // 4, disabled_color)
        draw_circle(screen, int(x + TOGGLE_WIDTH + TOGGLE_ADJ),
                    y + h // 4, h // 4, disabled_color)
        draw_circle(screen, int(x + TOGGLE_WIDTH), y + h //
                    4, h // 5, WHITE)  # small inner circle
    if blit_text:
        text_surf, text_rect = text_objects(text, pygame.font.Font(FONT_LIGHT, int(35 / 1440 * SCREEN_HEIGHT)),
                                            colour=text_colour)
        text_rect.topleft = (x, y)
        screen.blit(text_surf, text_rect)
    return x < mouse[0] < x + w and y < mouse[1] < y + h and click and pygame.time.get_ticks() > 100
