import pygame

from client.ui.theme import COLORS


class Button:
    def __init__(self, x, y, w, h, text, font, enabled=True):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.font = font
        self.enabled = enabled

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()

        if not self.enabled:
            color = COLORS["button_disabled"]
        elif self.rect.collidepoint(mouse_pos):
            color = COLORS["button_hover"]
        else:
            color = COLORS["button"]

        pygame.draw.rect(screen, color, self.rect, border_radius=10)

        text_surface = self.font.render(self.text, True, COLORS["text"])
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, event):
        if not self.enabled:
            return False

        return (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and self.rect.collidepoint(event.pos)
        )


class TextInput:
    def __init__(self, x, y, w, h, font, placeholder="", password=False):
        self.rect = pygame.Rect(x, y, w, h)
        self.font = font
        self.placeholder = placeholder
        self.password = password
        self.text = ""
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)

        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key == pygame.K_RETURN:
                self.active = False
            else:
                if len(self.text) < 24:
                    self.text += event.unicode

    def draw(self, screen):
        pygame.draw.rect(screen, COLORS["input_bg"], self.rect, border_radius=8)

        border_color = COLORS["success"] if self.active else COLORS["input_border"]
        pygame.draw.rect(screen, border_color, self.rect, width=2, border_radius=8)

        shown_text = self.text

        if self.password and self.text:
            shown_text = "*" * len(self.text)

        if shown_text:
            surface = self.font.render(shown_text, True, COLORS["text"])
        else:
            surface = self.font.render(self.placeholder, True, COLORS["text_muted"])

        screen.blit(surface, (self.rect.x + 12, self.rect.y + 10))


def draw_text(screen, text, x, y, font, color=None):
    if color is None:
        color = COLORS["text"]

    surface = font.render(text, True, color)
    screen.blit(surface, (x, y))


def draw_center_text(screen, text, y, font, color=None):
    if color is None:
        color = COLORS["text"]

    surface = font.render(text, True, color)
    rect = surface.get_rect(center=(screen.get_width() // 2, y))
    screen.blit(surface, rect)


def draw_center_text_shadow(screen, text, y, font, color, shadow_color=(0, 0, 0)):
    surface_shadow = font.render(text, True, shadow_color)
    rect_shadow = surface_shadow.get_rect(center=(screen.get_width() // 2 + 3, y + 3))
    screen.blit(surface_shadow, rect_shadow)

    surface = font.render(text, True, color)
    rect = surface.get_rect(center=(screen.get_width() // 2, y))
    screen.blit(surface, rect)


def draw_text_shadow(screen, text, x, y, font, color, shadow_color=(0, 0, 0)):
    shadow_surface = font.render(text, True, shadow_color)
    screen.blit(shadow_surface, (x + 3, y + 3))

    surface = font.render(text, True, color)
    screen.blit(surface, (x, y))


def draw_panel(screen, x, y, w, h):
    rect = pygame.Rect(x, y, w, h)
    pygame.draw.rect(screen, COLORS["panel"], rect, border_radius=16)


def draw_background(screen, background_image=None):
    if background_image:
        bg = pygame.image.load(background_image).convert()
        bg = pygame.transform.scale(bg, screen.get_size())
        screen.blit(bg, (0, 0))
        return

    width, height = screen.get_size()

    for y in range(height):
        ratio = y / height

        r = int(COLORS["bg_top"][0] * (1 - ratio) + COLORS["bg_bottom"][0] * ratio)
        g = int(COLORS["bg_top"][1] * (1 - ratio) + COLORS["bg_bottom"][1] * ratio)
        b = int(COLORS["bg_top"][2] * (1 - ratio) + COLORS["bg_bottom"][2] * ratio)

        pygame.draw.line(screen, (r, g, b), (0, y), (width, y))
