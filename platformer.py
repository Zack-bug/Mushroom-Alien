import pgzrun
import math
import random

WIDTH= 800  
HEIGHT= 500

player = Actor('player_stand_r')
walk_images_R = ['player_walk_r1','player_walk_r2']
walk_images_L = ['player_walk_l1','player_walk_l2']
player.pos = (WIDTH/2, HEIGHT/6)
movementSpeed = 8
velocity_y = 0
gravity = 1
frame_index=0
direction = 'right'
is_moving = False
is_on_air = True
has_lost = 0

spinner = Actor('spinner1')
spinner.images=['spinner1','spinner2']
spinner.pos= (-200, HEIGHT-20)
spinner_frame=0
spinner_spawn_timer=0
spinner_speed=4

fly = Actor('fly1')
fly.images=['fly1','fly2']
fly.pos= (0, 200)
fly_frame=0
fly_spawn_timer=0
fly_speed=5

game_state= 'menu'
sound_on=False
play_button = Rect(WIDTH/2 -100, 305,200,50)
sound_button= Rect(WIDTH/2 -100,365, 200,50)
quit_button= Rect(WIDTH/2 -60, 425, 120,60)


def update():
    global velocity_y, frame_index, direction, is_moving, is_on_air, game_state, spinner_spawn_timer,spinner_speed,spinner_spawn_chance, fly_spawn_timer, fly_speed, fly_spawn_chance
    
    if game_state =='menu':
        return
    
    gravity = 1.35
    is_moving=False
    spinner.x+=spinner_speed
    if keyboard.d:
        player.x += movementSpeed
        direction= 'right'
        is_moving=True
    if keyboard.a:
        player.x -= movementSpeed
        direction= 'left'
        is_moving=True
    if keyboard.w and not is_on_air:
        velocity_y =-30
        is_on_air =True 
        if sound_on:
             sounds.jump.play()   

    player.y += velocity_y    
    velocity_y += gravity

    if player.bottom > HEIGHT-4:
        player.bottom = HEIGHT
        velocity_y = 0
        is_on_air = False
    else:
        is_on_air=True

    
    frame_index += 0.12
    if frame_index >= len(walk_images_R):
       frame_index = 0


    if is_on_air:
        if direction =='right':
            player.image='player_air_r'
        else:
            player.image='player_air_l'    
    
    elif is_moving:
        if direction=='right':       
            player.image = walk_images_R[int(frame_index)]
        elif direction=='left':       
            player.image = walk_images_L[int(frame_index)]        

    
    elif direction=='right':
        player.image='player_stand_r'
    elif direction =='left':
        player.image='player_stand_l'      

    
    if player.right > WIDTH:
        player.right=WIDTH
    if player.left < 0:
        player.left = 0
    if player.top < 0:
        player.top =0


    spinner.x += spinner_speed
    if spinner.x > WIDTH + 100 or spinner.x < -100:
        spinner_spawn_timer += 1
        spinner_spawn_chance = random.randint(100,160)
    
        if spinner_spawn_timer > spinner_spawn_chance:
            spinner_spawn_timer = 0
            
            if random.randint(0, 1) == 0:
                    spinner.x = -50
                    spinner_speed = 4
            else:
                spinner.x = WIDTH + 50
                spinner_speed = -4
    if player.colliderect(spinner):
        if sound_on:
            sounds.hit.play()
            sounds.hit.set_volume(.4)
        game_state = 'menu'
        spinner_speed=0


    fly.x += fly_speed
    if fly.x > WIDTH + 100 or fly.x < -100:
        fly_spawn_timer += 1
        fly_spawn_chance = random.randint(100,160)
        if fly_spawn_timer > fly_spawn_chance:
            fly_spawn_timer = 0
            
            if random.randint(0, 1) == 0:
                    fly.x = -0
                    fly_speed = 5
            else:
                fly.x = WIDTH + 50
                fly_speed = -5
    if player.colliderect(fly):
        game_state = 'menu'
        if sound_on:
             sounds.hit.play()  
             sounds.hit.set_volume(.4)
        fly_speed=0

def on_mouse_down(pos):
    global game_state,sound_on


    if game_state=='menu':
        
        if play_button.collidepoint(pos):
            reset_game()
            game_state='play'
        elif sound_button.collidepoint(pos):
            sound_on = not sound_on
            if sound_on:
                sounds.theme_music.play(-1)
                sounds.theme_music.set_volume(.4)
            else:
                sounds.theme_music.set_volume(0)
                sounds.jump.set_volume(0)
                sounds.theme_music.stop()
        elif quit_button.collidepoint(pos):
            quit()            

def reset_game():
    global spinner_speed, spinner_spawn_timer, velocity_y, is_on_air,has_lost, fly_speed, fly_spawn_timer

    player.pos = (WIDTH/2, HEIGHT/6)
    velocity_y = 0
    is_on_air = True

    spinner.x = -200
    spinner_speed = 4
    spinner_spawn_timer = 0
    
    fly.x=WIDTH+200
    fly_speed=5
    fly_spawn_timer=0
    has_lost=1
def draw():
    global has_lost
    screen.blit('background',(0,0))

    if game_state=='menu':
        
        screen.draw.text("Play", center=play_button.center, fontsize=50, color ='white')
        sound_text = "Sound: On" if sound_on else "Sound:Off"
        screen.draw.text(sound_text, center=sound_button.center, fontsize=40, color='white')
        screen.draw.text("Quit", center = quit_button.center, fontsize=40, color= 'white')
        screen.draw.text("MUSHROOM ALIEN", center=(WIDTH/2,80), fontsize=65, color= 'white', shadow=(1,1))
        if has_lost ==1:
            screen.draw.text("Game Over", center=(WIDTH/2,160), fontsize=85, color= 'white', shadow=(1,1))
        

    elif game_state=='play':
        player.draw()
        spinner.draw()
        fly.draw()
pgzrun.go()

