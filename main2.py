import pygame
import sys

#############################################
# 1) MAPA EM TEXTO
#############################################

level_map = [
    "xxxxxxxxxxxxxxxx",
    "x..............x",
    "x..............x",
    "x......xxx.....x",
    "x..............x",
    "x...........x..x",
    "x......xxx.....x",
    "x..............x",
    "x..............x",
    "x..............x",
    "x..............x",
    "xxxxxxxxxxxxxxxx"
]

TILE_SIZE = 64  # tamanho final do sprite (escala aplicada)

#############################################
# 2) CLASSE "KNIGHT" (PERSONAGEM)
#############################################

class Knight:
    def __init__(self, x, y):
        self.spritesheet = pygame.image.load("knight.png").convert_alpha()
        self.idle_frames = []
        self.run_frames = []
        self.load_frames()

        self.current_frame = 0
        self.image = self.idle_frames[self.current_frame]
        self.rect = self.image.get_rect(topleft=(x, y))

        self.animation_timer = 0
        self.speed = TILE_SIZE // 8  # Velocidade baseada no tamanho do tile
        self.moving = False

    def load_frames(self):
        """Carrega os quadros para idle e run com escala."""
        scale = TILE_SIZE / 16  # Escala do frame original (16x16 para TILE_SIZE)

        # Idle (linha 1 do spritesheet, y=0)
        for i in range(4):  # 4 frames na linha 1
            frame = self.spritesheet.subsurface((i * 32, 0, 32, 32))  # y=0
            scaled_frame = pygame.transform.scale(frame, (int(32 * scale), int(32 * scale)))
            self.idle_frames.append(scaled_frame)

        # Run (linha 3 do spritesheet, y=32)
        for i in range(8):  # 8 frames na linha 3
            frame = self.spritesheet.subsurface((i * 32, 64, 32, 32))  # y=32
            scaled_frame = pygame.transform.scale(frame, (int(32 * scale), int(32 * scale)))
            self.run_frames.append(scaled_frame)

    def update(self, keys):
        """Atualiza o cavaleiro."""
        self.moving = False

        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
            self.moving = True
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
            self.moving = True

        # Alterna entre as animações
        frames = self.run_frames if self.moving else self.idle_frames
        self.animation_timer += 1
        if self.animation_timer >= 10:  # Troca de frame a cada 10 ticks
            self.animation_timer = 0
            self.current_frame = (self.current_frame + 1) % len(frames)
            self.image = frames[self.current_frame]

    def draw(self, screen):
        screen.blit(self.image, self.rect)


#############################################
# 3) FUNÇÕES PARA CRIAR A LISTA DE RETÂNGULOS DE TILE SÓLIDO
#############################################

def create_solid_tiles(map_data):
    """Cria uma lista de pygame.Rect para cada 'x' no mapa."""
    solid_rects = []
    for row_index, row in enumerate(map_data):
        for col_index, char in enumerate(row):
            if char == 'x':
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE
                solid_rects.append(pygame.Rect(x, y, TILE_SIZE, TILE_SIZE))
    return solid_rects


#############################################
# 4) FUNÇÃO PRINCIPAL
#############################################

def main():
    pygame.init()
    screen_width = len(level_map[0]) * TILE_SIZE
    screen_height = len(level_map) * TILE_SIZE
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Jogo de Plataforma - Cavaleiro")

    clock = pygame.time.Clock()

    knight = Knight(x=TILE_SIZE, y=TILE_SIZE * 5)
    solid_tiles = create_solid_tiles(level_map)

    running = True
    while running:
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Atualizar lógica
        knight.update(keys)

        # Desenhar
        screen.fill((50, 150, 200))  # Cor do fundo
        for tile in solid_tiles:
            pygame.draw.rect(screen, (100, 100, 100), tile)
        knight.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
