import pygame


pygame.font.init()
_FONTS = {} # cache of loaded fonts


def _get_font(name: str='Comic Sans MS', size: int=30) -> pygame.font.Font:
    """Retrieves a pygame font object, loading it if it hasn't been
    loaded before.

    Args:
        name (str): name of the font
        size (int): font size

    Returns:
        The font object
    """
    return _FONTS.setdefault(name.lower(), {}).setdefault(size, pygame.font.SysFont(name, size))

def draw_text(surface: pygame.surface.Surface, text: str, font_name: str, size: int, color: tuple, pos: tuple):
    """Draws some text to a surface.

    Args:
        surface (Surface): the surface to render to.
        text (str): the text to draw.
        font_name (str): the name of the font.
        size (int): the size of the text.
        color (tuple): the color of the text as an RGB tuple.
        pos (tuple): the coordinates to draw the text at.
    """
    text_surface = _get_font(font_name, size).render(text, True, color)
    surface.blit(text_surface, pos)
