import pgzrun
import random

WIDTH= 800  
HEIGHT= 500

class Player(Actor):
    def __init__(self):
        super().__init__('player_stand_r1', (WIDTH /2,HEIGHT/6))
        self.velocity_y = 0
        self.gravity = 1.35
        self.direction = 'right'
        self.is_moving = False
        self.is_on_air = True
        self.idle_images_r = ['player_stand_r1','player_stand_r2']
        self.idle_images_l = ['player_stand_l1','player_stand_l2']
        self.walk_images_r = ['player_walk_r1', 'player_walk_r2']
        self.walk_images_l = ['player_walk_l1', 'player_walk_l2']
        self.frame_index = 0
        
    def move(self): 
        self.is_moving=False
        if keyboard.d:
            self.x += self.movement_Speed
            self.direction= 'right'
            self.is_moving=True
        if keyboard.a:
            self.x -= self.movement_Speed
            self.direction= 'left'
            self.is_moving=True
        if keyboard.w and not self.is_on_air:
            self.velocity_y =-30
            self.is_on_air =True 
            if sound_on:
                sounds.jump.play()   

    def apply_gravity(self):    
        self.y += self.velocity_y    
        self.velocity_y += self.gravity

        if self.bottom > HEIGHT-4:
            self.bottom = HEIGHT
            self.velocity_y = 0
            self.is_on_air = False
        else:
            self.is_on_air=True

    def animate(self):
        
        self.frame_index += 0.12
        if self.frame_index >= len(self.walk_images_r):
            self.frame_index = 0


        if self.is_on_air:
            if self.direction =='right':
                self.image='player_air_r'
            else:
                self.image='player_air_l'    
    
        elif self.is_moving:
            if self.direction=='right':       
                self.image = self.walk_images_r[int(self.frame_index)]
            elif self.direction=='left':       
                self.image = self.walk_images_l[int(self.frame_index)]        
        else: 
            if self.direction=='right':
                self.image= self.idle_images_r[int(self.frame_index)]
            elif self.direction=='left':
                self.image= self.idle_images_l[int(self.frame_index)]

    def boundaries(self):

        if self.right > WIDTH:
            self.right=WIDTH
        if self.left < 0:
            self.left = 0
        if self.top < 0:
            self.top =0

class Enemy(Actor):
    def __init__(self, image, y, speed):
        super().__init__(image,(-200,y))
        self.speed = speed
        self.spawn_timer=0
        self.spawn_chance = random.randint(100,160)
        self.direction = 'right'
    def move(self):
        self.x += self.speed
        
        if self.x>WIDTH+100 or self.x< -100:
            self.spawn_timer+=1

            if self.spawn_timer> self.spawn_chance:
                self.spawn_timer=0
                self.spawn_chance= random.randint(100,160)
                if random.randint(0,1)==0:
                    self.x=-50
                    self.speed= abs(self.speed)
                    self.direction='left'
                else:
                    self.x = WIDTH+50
                    self.speed = -abs(self.speed)
                    self.direction='right'
class Spinner(Enemy):
    def __init__(self):
        super().__init__('spinner1', HEIGHT -20,4)
        self.images = ['spinner1', 'spinner2']
        self.frame_index=0
    def animate(self):
        self.frame_index +=0.2
        if self.frame_index >= len(self.images):
            self.frame_index=0
        self.image = self.images[int(self.frame_index)]

class Fly(Enemy):
    def __init__(self):
        super().__init__('fly1_r',220,6)
        self.images_r= ['fly1_r', 'fly2_r']
        self.images_l= ['fly1_l', 'fly2_l']
        self.frame_index=0
    def animate(self):
        self.frame_index +=0.12
        if self.frame_index >= len(self.images_r):
            self.frame_index=0
        
        if self.direction == 'right':
            self.image= self.images_r[int(self.frame_index)]
        else:
            self.image= self.images_l[int(self.frame_index)]
player = Player()
spinner= Spinner()
fly = Fly()

game_state= 'menu'
sound_on=False
has_lost = 0
win_timer=0
win_time_limit=30
player_won=False



play_button = Rect(WIDTH/2 -100, 305,200,50)
sound_button= Rect(WIDTH/2 -100,365, 200,50)
quit_button= Rect(WIDTH/2 -60, 425, 120,60)


def update():
    global game_state
    
    if game_state =='menu':
        return
    
    player.move()
    player.apply_gravity()
    player.animate()
    player.boundaries()
    
    spinner.move()
    spinner.animate()
    fly.move()
    fly.animate()
    
    if player.colliderect(spinner) or player.colliderect(fly):
        if sound_on:
            sounds.hit.play()
            sounds.hit.set_volume(.4)
        game_state = 'menu'
        sounds.theme_music.stop()
def on_mouse_down(pos):
    global game_state,sound_on


    if game_state=='menu':
        
        if play_button.collidepoint(pos):
            reset_game()
            global player_won
            game_state='play'
            player_won=False
            clock.schedule_interval(update_timer,1)
        elif sound_button.collidepoint(pos):
            sound_on = not sound_on
            if sound_on:
                sounds.theme_music.set_volume(.4)
                sounds.click.set_volume(.5)
                sounds.click.play()
                sounds.jump.set_volume(1)
            else:
                sounds.theme_music.set_volume(0)
                sounds.jump.set_volume(0)
                sounds.theme_music.stop()
        elif quit_button.collidepoint(pos):
            quit()            

def reset_game():
    global has_lost,win_timer
    clock.unschedule(update_timer)
    player.pos = (WIDTH/2, HEIGHT/6)
    player.velocity_y = 0
    player.is_on_air = True
    player.movement_Speed=6

    spinner.x = -200
    spinner.speed = 8
    spinner.spawn_timer = 0
    fly.x=WIDTH+200
    fly.speed=8
    fly.spawn_timer=0

    win_timer=0
    has_lost=1
    if sound_on:
        sounds.theme_music.play()
def draw():

    global has_lost
    screen.blit('background',(0,0))

    if game_state=='menu':
        
        screen.draw.text("Play", center=play_button.center, fontsize=50, color ='white')
        sound_text = "Sound: On" if sound_on else "Sound:Off"
        screen.draw.text(sound_text, center=sound_button.center, fontsize=40, color='white')
        screen.draw.text("Quit", center = quit_button.center, fontsize=40, color= 'white')
        screen.draw.text("MUSHROOM ALIEN", center=(WIDTH/2,80), fontsize=65, color= 'white', shadow=(1,1))
        if has_lost ==1 and player_won==False:
            screen.draw.text("Game Over", center=(WIDTH/2,160), fontsize=85, color= 'red', shadow=(1,1))
        
    if player_won:
        global win_timer
        screen.draw.text(
        "YOU WIN", center=(WIDTH/2,210), fontsize =90, color="green", shadow=(2,2))
        sounds.theme_music.stop()
    elif game_state=='play':
        player.draw()
        spinner.draw()
        fly.draw()
        
        screen.draw.text(
            f"{win_timer} / {win_time_limit}",
        topright=(WIDTH-20,20), fontsize=35, color = ('yellow'))


def update_timer():
    global win_timer, player_won, game_state
    if game_state == 'menu':
        return
    if win_timer<win_time_limit:
        win_timer+=1
    else:
        player_won=True
        game_state='menu'
        if sound_on:
            sounds.win_sound.set_volume(.2)
            sounds.win_sound.play()
            
        
        win_timer=0

pgzrun.go()

