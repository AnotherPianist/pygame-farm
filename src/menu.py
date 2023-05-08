import pygame.display

from src.settings import SCREEN_HEIGHT, SCREEN_WIDTH, SELL_PRICES, BUY_PRICES
from src.timer import Timer


class Menu:
    def __init__(self, player, toggle_menu):
        self.player = player
        self.toggle_menu = toggle_menu
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font('../font/LycheeSoda.ttf', 30)

        self.width = 400
        self.space = 10
        self.padding = 8

        self.options = list(self.player.item_inventory.keys()) + list(self.player.seed_inventory.keys())
        self.sell_border = len(self.player.item_inventory) - 1
        self.setup()

        self.i = 0
        self.timer = Timer(200)

    def display_money(self):
        text_surf = self.font.render(f'${self.player.money}', False, 'Black')
        text_rect = text_surf.get_rect(midbottom=(SCREEN_WIDTH / 2, SCREEN_HEIGHT - 20))
        pygame.draw.rect(self.display_surface, 'White', text_rect.inflate(10, 10), 0, 4)
        self.display_surface.blit(text_surf, text_rect)

    def setup(self):
        self.text_surfs = []
        self.total_height = 0

        for i, item in enumerate(self.options):
            text = f'{"sell" if i <= self.sell_border else "buy"} {item} {"seed" if i > self.sell_border else ""} (${SELL_PRICES[item] if i <= self.sell_border else BUY_PRICES[item]})'
            text_surf = self.font.render(text, False, 'Black')
            self.text_surfs.append(text_surf)
            self.total_height += text_surf.get_height() + (2 * self.padding)

        self.total_height += self.space * (len(self.text_surfs) - 1)
        self.menu_top = SCREEN_HEIGHT / 2 - self.total_height / 2
        self.main_rect = pygame.Rect(SCREEN_WIDTH / 2 - self.width / 2, self.menu_top, self.width, self.total_height)

        self.buy_text = self.font.render('buy', False, 'Black')
        self.sell_text = self.font.render('sell', False, 'Black')

    def input(self):
        keys = pygame.key.get_pressed()
        self.timer.update()

        if keys[pygame.K_ESCAPE]:
            self.toggle_menu()

        if not self.timer.active:
            if keys[pygame.K_UP]:
                self.timer.activate()
                self.i -= 1
                if self.i < 0:
                    self.i = len(self.options) - 1
            elif keys[pygame.K_DOWN]:
                self.timer.activate()
                self.i += 1
                if self.i >= len(self.options):
                    self.i = 0
            elif keys[pygame.K_RETURN]:
                self.timer.activate()
                current_item = self.options[self.i]

                if self.i <= self.sell_border:
                    if self.player.item_inventory[current_item] > 0:
                        self.player.item_inventory[current_item] -= 1
                        self.player.money += SELL_PRICES[current_item]
                else:
                    seed_price = BUY_PRICES[current_item]
                    if self.player.money >= seed_price:
                        self.player.seed_inventory[current_item] += 1
                        self.player.money -= seed_price

    def show_entry(self, text_surf, amount, top, selected):
        bg_rect = pygame.Rect(self.main_rect.left, top, self.width, text_surf.get_height() + (2 * self.padding))
        pygame.draw.rect(self.display_surface, 'White', bg_rect, 0, 4)

        text_rect = text_surf.get_rect(midleft=(self.main_rect.left + 20, bg_rect.centery))
        self.display_surface.blit(text_surf, text_rect)

        amount_surf = self.font.render(str(amount), False, 'Black')
        amount_rect = amount_surf.get_rect(midright=(self.main_rect.right - 20, bg_rect.centery))
        self.display_surface.blit(amount_surf, amount_rect)

        if selected:
            pygame.draw.rect(self.display_surface, 'Black', bg_rect, 4, 4)

    def update(self):
        self.input()
        self.display_money()

        amounts = list(self.player.item_inventory.values()) + list(self.player.seed_inventory.values())

        for i, text_surf in enumerate(self.text_surfs):
            top = self.main_rect.top + i * (text_surf.get_height() + (2 * self.padding) + self.space)
            self.show_entry(text_surf, amounts[i], top, self.i == i)
