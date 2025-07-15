import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
FPS = 60
TILE_SIZE = 32

# Colors
dark_gray = (40, 40, 40)
white = (255, 255, 255)
blue = (50, 150, 255)
green = (50, 255, 50)
yellow = (255, 255, 50)
red = (255, 50, 50)
brown = (139, 69, 19)

# Maze layout
# 'W' wall, '.' floor, 'K' key, 'D' door, 'E' exit
MAZE_MAP = [
    "WWWWWWWWWWWWWWWWWWWW",
    "W.....W.........K.W",
    "W.W.W.W.WWWWWW.W.WW",
    "W.W.W.....W....W..W",
    "W.W.W.WWWW.W.WWW.WW",
    "W...W.W....W.W....W",
    "WWW.W.W.WW.W.WWWW.W",
    "W...W...W..W......W",
    "W.WWWWW.WW.W.WWWWWW",
    "W.K....W...W...E..W",
    "WWWWWWWWWWWWWWWWWWWW",
]

class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE-4, TILE_SIZE-4))
        self.image.fill(blue)
        self.rect = self.image.get_rect(topleft=(pos[0]+2, pos[1]+2))
        self.speed = TILE_SIZE
        self.has_key = False

    def move(self, dx, dy, walls, door_group):
        new_x = self.rect.x + dx
        new_y = self.rect.y + dy
        # Tentative rect
        new_rect = pygame.Rect(new_x, new_y, self.rect.width, self.rect.height)

        # Check wall collision
        for wall in walls:
            if new_rect.colliderect(wall.rect):
                return
        # Check door collision
        for door in door_group:
            if new_rect.colliderect(door.rect) and not self.has_key:
                return
        self.rect.x = new_x
        self.rect.y = new_y

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, color):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=pos)

class Key(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE//2, TILE_SIZE//2))
        self.image.fill(yellow)
        self.rect = self.image.get_rect(center=(pos[0]+TILE_SIZE//2, pos[1]+TILE_SIZE//2))

class Door(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(brown)
        self.rect = self.image.get_rect(topleft=pos)

class Exit(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(red)
        self.rect = self.image.get_rect(topleft=pos)


def load_maze(maze_map):
    walls = pygame.sprite.Group()
    keys = pygame.sprite.Group()
    doors = pygame.sprite.Group()
    exit_group = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    for y, row in enumerate(maze_map):
        for x, char in enumerate(row):
            pos = (x*TILE_SIZE, y*TILE_SIZE)
            if char == 'W':
                wall = Tile(pos, dark_gray);
                walls.add(wall); all_sprites.add(wall)
            elif char == 'K':
                key = Key(pos);
                keys.add(key); all_sprites.add(key)
            elif char == 'D':
                door = Door(pos);
                doors.add(door); all_sprites.add(door)
            elif char == 'E':
                ex = Exit(pos);
                exit_group.add(ex); all_sprites.add(ex)
    return walls, keys, doors, exit_group, all_sprites


def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Maze Adventure with Key & Door')
    clock = pygame.time.Clock()

    walls, keys, doors, exit_group, maze_sprites = load_maze(MAZE_MAP)
    # Player start
    start_pos = (TILE_SIZE+2, TILE_SIZE+2)
    player = Player(start_pos)
    all_sprites = pygame.sprite.Group(maze_sprites, player)

    font = pygame.font.SysFont(None, 24)
    collected_keys = 0
    total_keys = len(keys)
    won = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and not won:
                dx = dy = 0
                if event.key == pygame.K_LEFT: dx = -player.speed
                if event.key == pygame.K_RIGHT: dx = player.speed
                if event.key == pygame.K_UP: dy = -player.speed
                if event.key == pygame.K_DOWN: dy = player.speed
                if dx or dy:
                    player.move(dx, dy, walls, doors)

        # Collect key
        hit_keys = pygame.sprite.spritecollide(player, keys, True)
        if hit_keys:
            collected_keys += len(hit_keys)
            player.has_key = True
            for door in doors:
                door.kill()  # Open all doors

        # Check exit
        if pygame.sprite.spritecollideany(player, exit_group) and collected_keys == total_keys:
            won = True

        # Draw
        screen.fill(white)
        all_sprites.draw(screen)

        # HUD
        text = f'Keys: {collected_keys}/{total_keys}'
        screen.blit(font.render(text, True, (0,0,0)), (10, SCREEN_HEIGHT-30))
        if won:
            msg = font.render('You found all keys and escaped the maze! Congrats!', True, green)
            screen.blit(msg, (50, SCREEN_HEIGHT//2))

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == '__main__':
    main()
