import pygame

level_map = [
    "xxxxxxxxxxxxxxxx",
    "x..............x",
    "x...........x..x",
    "x.......xxxx...x",
    "x..............x",
    "xxxxxxxxxxxxxxxx"
]


class Player:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        
        self.speed_x = 0
        self.speed_y = 0
        
        self.gravity = 0.4
        
        self.rect = pygame.Rect(self.x,self.y, 32, 32)
        
    def handle_input(self,keys):
        if keys[pygame.K_LEFT]:
            self.speed_x = -5
        elif keys[pygame.K_RIGHT]:
            self.speed_x = 5
        else:
            self.speed_x = 0
            
        if keys[pygame.K_UP]:
            if self.speed_y == 0:
                self.speed_y = -10
        
    def update(self):
        self.speed_y += self.gravity
        
        self.x += self.speed_x
        self.y += self.speed_y
        
        self.rect.x = self.x
        self.rect.y = self.y
        
    def draw(self,surface):
        pygame.draw.rect(surface, (255,0,0), self.rect)

floor_rect = pygame.Rect(0,550,800,50)

def main():
    pygame.init()  # "Ligue os holofotes" do teatro (inicializa o Pygame)
    player = Player(32,32)
    

    # Crie o palco: uma janela de 800x600, por exemplo
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Meu Jogo de Plataforma")
    
    clock = pygame.time.Clock()  # Controlador de tempo (para limitar FPS se quiser)
    
    running = True
    while running:
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Pinte o "fundo do palco" (tela) com uma cor sólida
        screen.fill((135, 206, 235))  # Cor de "céu" (RGB)
        if player.rect.colliderect(floor_rect):
            # Se o player está colidindo por baixo, encoste o retângulo do player no retângulo do chão
            player.rect.bottom = floor_rect.top
            # Ajustar a posição y do player
            player.y = player.rect.y
            # Zerar a velocidade vertical para não continuar "caindo"
            player.speed_y = 0
        
        # Desenhar o chão
        pygame.draw.rect(screen, (0, 200, 0), floor_rect)    
        # Aqui você desenhará todos os elementos do jogo (personagem, chão, etc.)
        player.handle_input(keys)
        player.update()
        player.draw(screen)
        pygame.display.flip()  # Atualiza a tela com tudo que foi desenhado
        clock.tick(60)         # 60 FPS (opcional)
    
    pygame.quit()

if __name__ == "__main__":
    main()
