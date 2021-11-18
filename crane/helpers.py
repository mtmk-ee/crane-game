import pygame

pygame.font.init()

_FONTS = {}

def _get_font(name: str='Comic Sans MS', size: int=30) -> pygame.font.Font:
    return _FONTS.setdefault(name.lower(), {}).setdefault(size, pygame.font.SysFont(name, size))

def draw_text(surface: pygame.surface.Surface, text: str, font_name: str, size: int, color: tuple, pos: tuple):
    text_surface = _get_font(font_name, size).render(text, True, color)
    surface.blit(text_surface, pos)
