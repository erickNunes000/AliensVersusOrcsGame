import pgzrun
import pygame
from pygame import Rect
from pgzero.actor import Actor
import random  # 🔹 Agora usamos para alternar o número de inimigos

pygame.mixer.init()  

# Dimensões da tela
WIDTH = 800
HEIGHT = 600
GROUND_Y = 500  
TITLE = "Aliens 👽 vs Orcs 👹 "

# Estados do jogo
game_state = "menu"
sound_on = True
enemy_count = 1  # 🔹 Começa com 1 inimigo, depois alterna para 2

# Botões do menu
buttons = {
    "start": Rect(300, 200, 200, 50),
    "sound": Rect(300, 300, 200, 50),
    "quit": Rect(300, 400, 200, 50)
}

def play_music():
    """Toca a música apenas se estiver ativada."""
    if sound_on:
        music.play("preview-5")  
        music.set_volume(0.4)  

# ✅ Inicia a música corretamente ao abrir o jogo
play_music()

# Classe do Herói
class Hero:
    def __init__(self):
        self.actor = Actor("p3_front", (200, GROUND_Y))  
        self.speed = 10  
        self.jump_power = -22
        self.gravity = 0.6
        self.velocity_y = 0
        self.frame = 0
        self.frame_delay = 7 
        self.frame_counter = 0  
        self.idle_frames = ["p3_front", "p3_stand", "p3_front"]
        self.walk_frames = ["p3_walk01", "p3_walk02", "p3_walk03"]
        self.on_ground = True

    def update(self):
        keys = keyboard
        self.frame_counter += 3
        if self.frame_counter >= self.frame_delay:
            self.frame_counter = 0  

            if keys.left:
                self.actor.x -= self.speed
                self.frame = (self.frame + 1) % len(self.walk_frames)
                self.actor.image = self.walk_frames[self.frame]

            elif keys.right:
                self.actor.x += self.speed
                self.frame = (self.frame + 1) % len(self.walk_frames)
                self.actor.image = self.walk_frames[self.frame]

            else:
                self.frame = (self.frame + 1) % len(self.idle_frames)
                self.actor.image = self.idle_frames[self.frame]

        # Pulo
        if keys.up and self.on_ground:
            self.velocity_y = self.jump_power
            self.on_ground = False

        # Aplicar gravidade
        self.velocity_y += self.gravity
        self.actor.y += self.velocity_y

        # Impedir que o herói caia abaixo do chão
        if self.actor.y >= GROUND_Y:
            self.actor.y = GROUND_Y
            self.velocity_y = 0
            self.on_ground = True

    def draw(self):
        self.actor.draw()

# Classe do Inimigo
class Enemy:
    def __init__(self, x_offset=0):
        self.actor = Actor("orc_attack0", (WIDTH + x_offset, GROUND_Y))  
        self.speed = 2  
        self.frame = 0
        self.frame_delay = 6  
        self.frame_counter = 0  
        self.walk_frames = ["orc_attack0", "orc_attack1", "orc_attack2"]

    def update(self):
        self.actor.x -= self.speed  

        self.frame_counter += 1
        if self.frame_counter >= self.frame_delay:
            self.frame_counter = 0  
            self.frame = (self.frame + 1) % len(self.walk_frames)
            self.actor.image = self.walk_frames[self.frame]

        # Se o inimigo sair completamente da tela, remove todos e gera novos
        if self.actor.right < 0:
            spawn_enemies()

    def draw(self):
        self.actor.draw()

# Criar objetos
hero = Hero()
enemies = []  # 🔹 Lista para armazenar inimigos

def spawn_enemies():
    """Alterna entre 1 e 2 inimigos e cria novos quando os antigos saem da tela."""
    global enemies, enemy_count  

    enemy_count = 2 if enemy_count == 1 else 1  # Alterna entre 1 e 2 inimigos
    enemies = [Enemy(i * 50) for i in range(enemy_count)]  # Cria novos inimigos

# 🔹 Chamar a função ao iniciar o jogo para gerar os primeiros inimigos
spawn_enemies()

def check_collision():
    """Verifica se o herói colidiu com algum inimigo."""
    global game_state
    for enemy in enemies:
        if hero.actor.colliderect(enemy.actor):  
            game_state = "gameover"  

def draw():
    screen.clear()
    
    try:
        screen.blit("spaceship", (0, 0))  
    except:
        print("⚠️ Imagem de fundo 'spaceship.png' não encontrada na pasta 'images'!")

    if game_state == "menu":
        screen.draw.text("MENU PRINCIPAL", center=(WIDTH//2, 100), fontsize=50, color="white")
        for name, rect in buttons.items():
            screen.draw.filled_rect(rect, "gray")
            screen.draw.rect(rect, "white")
        screen.draw.text("Começar o jogo", center=buttons["start"].center, fontsize=30, color="black")
        screen.draw.text("Música: " + ("Ligada" if sound_on else "Desligada"), center=buttons["sound"].center, fontsize=30, color="black")
        screen.draw.text("Sair do jogo", center=buttons["quit"].center, fontsize=30, color="black")

    elif game_state == "jogo":
        hero.draw()
        for enemy in enemies:
            enemy.draw()

    elif game_state == "gameover":
        screen.draw.text("GAME OVER!", center=(WIDTH//2, HEIGHT//2), fontsize=80, color="red")
        screen.draw.text("Clique para voltar ao menu", center=(WIDTH//2, HEIGHT//2 + 50), fontsize=30, color="white")

def update():
    if game_state == "jogo":
        hero.update()
        for enemy in enemies:
            enemy.update()
        check_collision()

def on_mouse_down(pos):
    global game_state, sound_on

    if game_state == "menu":
        if buttons["start"].collidepoint(pos):
            game_state = "jogo"
            if sound_on:
                play_music()
                sounds.monster.play(-1)
                sounds.monster.set_volume(0.4)

        elif buttons["sound"].collidepoint(pos):
            sound_on = not sound_on
            if sound_on:
                play_music()
            else:
                music.stop()
                sounds.monster.stop()

        elif buttons["quit"].collidepoint(pos):
            exit()

    elif game_state == "gameover":  #encerra o jogo
        game_state = "menu"

pgzrun.go()
