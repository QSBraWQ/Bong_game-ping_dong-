from pygame import *
from sys import exit
from random import randint

init()

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, player_stretch_x, player_stretch_y):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (player_stretch_x, player_stretch_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update_left(self):
        keys = key.get_pressed()
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_height - self.rect.height - 5:
            self.rect.y += self.speed

    def update_right(self):
        keys = key.get_pressed()
        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < win_height - self.rect.height - 5:
            self.rect.y += self.speed

class Ball(GameSprite):
    def __init__(self, player_image, player_x, player_y, player_speed, player_stretch_x, player_stretch_y):
        super().__init__(player_image, player_x, player_y, player_speed, player_stretch_x, player_stretch_y)
        self.speed_x = player_speed
        self.speed_y = player_speed
        self.default_speed_x=self.speed_x
        self.default_speed_y=self.speed_y
    
    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        
        # Ball collision with top and bottom
        if self.rect.y <= 0 or self.rect.y >= win_height - self.rect.height:
            self.speed_y *= -1
        
        # Ball collision with paddles
        if sprite.collide_rect(self, player) or sprite.collide_rect(self, enemy):
            self.speed_x *= -1.1  # 10% speed increase
            self.speed_y *= 1.1
            bounce.play()
        
        # Ball out of bounds (left or right)
        global player_score
        global enemy_score
        if self.rect.x <= 0:
            self.rect.x = win_width // 2
            self.rect.y = win_height // 2
            self.speed_x *= -1
            enemy_score+=1
            self.speed_x=self.default_speed_x + (player_score + enemy_score)*0.1
            self.speed_y=self.default_speed_y + (player_score + enemy_score)*0.1
            win.play()
        if self.rect.x >= win_width:
            self.rect.x = win_width // 2
            self.rect.y = win_height // 2
            self.speed_x *= -1
            player_score+=1
            self.speed_x=self.default_speed_x + (player_score + enemy_score)*0.1
            self.speed_y=self.default_speed_y + (player_score + enemy_score)*0.1
            win.play()
# Game setup
win_width = 1366
win_height = 768
window = display.set_mode((win_width, win_height))
display.set_caption("Pong Game")
player_score=0
enemy_score=0
# Load background (make sure you have 'sky.jpg' in your directory)
background = transform.scale(image.load("sky.jpg"), (win_width, win_height))

# Create game objects
player = Player('platform_1.png', 30, win_height//2 - 60, 8, 20, 120)
enemy = Player('platform_2.png', win_width - 50, win_height//2 - 60, 8, 20, 120)
ball = Ball('ball.png', win_width//2, win_height//2, 5, 30, 30)
mixer.init()
mixer.music.load('disbelief_mus.mp3')
mixer.music.play(-1)
mixer.music.set_volume(0.25)
bounce=mixer.Sound("snd_graze.wav")
win=mixer.Sound("snd_won.wav")
win.set_volume(0.5)
win_counter=0

# Create sprite groups
players = sprite.Group(player)
enemies = sprite.Group(enemy)
balls = sprite.Group(ball)

game = True
finish = False
clock = time.Clock()
FPS = 180
pause = False
font.init()
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                pause = not pause
    
    if not pause:
        window.blit(background, (0, 0))
        
        # Player controls
        player.update_left()  # Left player uses arrow keys
        enemy.update_right()  # Right player uses W/S keys
        
        # Ball movement
        ball.update()
        font_obj = font.SysFont('Arial', 36)
        score_left = font_obj.render('Score '+str(+ player_score), True, (179, 22, 11))
        score_right = font_obj.render('Score '+str( enemy_score), True, (179, 22, 11))
        window.blit(score_left, (win_width//4, 30))
        window.blit(score_right, (3*win_width//4, 30))
        
        # Draw everything
        players.draw(window)
        enemies.draw(window)
        balls.draw(window)

        # Win check
        win_fnt= font.SysFont('Arial', 80)
        if player_score > 5:
            win_result = win_fnt.render('Player 1 won', True, (0,0,0))
            window.blit(win_result, (win_width//2-400, win_height//2))
            win_counter+=1
            if win_counter > FPS*4:
                game=False
        elif enemy_score > 5:
            win_result = win_fnt.render('Player 2 won', True, (0,0,0))
            window.blit(win_result, (win_width//2-400, win_height//2))
            win_counter+=1
            if win_counter > FPS*4:
                game=False

        display.update()
        clock.tick(FPS)