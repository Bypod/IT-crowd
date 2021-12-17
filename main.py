import pygame, random


clock = pygame.time.Clock()

from pygame.locals import *

pygame.init()
WINDOW_SIZE = (1200, 800)

screen = pygame.display.set_mode(WINDOW_SIZE,0,32)

display = pygame.Surface((300, 200))

pygame.display.set_caption('The IT Crowd:"The Missing Plug."')

 #load images
bgImg = pygame.image.load('imgs/bg_img.jpg')

blockImgOG = pygame.image.load('imgs/green_block.jpg')
blockImg = pygame.transform.scale(blockImgOG, (16, 16))



TILE_SIZE = 20
air_timer = 0
true_scroll = [0, 0]
moveRight = False
moveLeft = False
playerYMom = 0
CHUNK_SIZE = 8

def generate_chunk(x,y):
    chunk_data = []
    for y_pos in range(CHUNK_SIZE):
        for x_pos in range(CHUNK_SIZE):
            target_x = x * CHUNK_SIZE + x_pos
            target_y = y * CHUNK_SIZE + y_pos
            tile_type = 0
            if target_y > 10:
                tile_type = 2 #grass
            elif target_y == 10:
                tile_type = 1 #dirt
            elif target_y == 9:
                if random.randint(1,5) == 1:
                    tile_type = 3 #plant
            if tile_type != 0:
                chunk_data.append([[target_x, target_y], tile_type])
    return chunk_data


 #game map
'''game_map = 
            [['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0',],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0',],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0',],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0',],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0',],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0',],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0',],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0',],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0',],
            ['0','0','0','0','1','1','1','0','0','0','0','0','0','0','0','1','0','0','0','0',],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','1','0','1','0','0','0','0',],
            ['1','1','1','0','0','0','0','0','0','0','1','1','0','1','0','1','0','0','0','0',],
            ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1',]]'''


global animations_frames
animation_frames = {}

def load_animation(path,frame_durations):
    global animation_frames
    animation_name = path.split('/')[-1]
    animation_frame_data = []
    n = 0
    for frame in frame_durations:
        animation_frame_id = animation_name + '_' + str(n)
        img_loc = path + '/' + animation_frame_id + '.png'
        # player_animations/idle/idle_0.png
        animation_image = pygame.image.load(img_loc).convert()
        animation_image.set_colorkey((255,255,255))
        animation_frames[animation_frame_id] = animation_image.copy()
        for i in range(frame):
            animation_frame_data.append(animation_frame_id)
        n += 1
    return animation_frame_data

def change_action(action_var,frame,new_value):
    if action_var != new_value:
        action_var = new_value
        frame = 0
    return action_var,frame

animation_database = {}

animation_database['run'] = load_animation('animations/run', [7, 7])
animation_database['idle'] = load_animation('animations/idle', [7])

game_map = {}

tile_index = {1:blockImg,
              2:blockImg,
              3:blockImg}

jump_sound = pygame.mixer.Sound('sounds/jump.mp3')

pygame.mixer.music.load('sounds/music.mp3')
pygame.mixer.music.play(-1)

player_action = 'idle'
player_frame = 0
player_flip = False \

player_img = pygame.image.load('imgs/Moss_pixel_1.png')
#player_img = pygame.transform.scale(player_imgOG, (12, 32))

def collision_test(rect, tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list

def move(rect, movement, tiles):
    collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}
    rect.x += movement[0]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[0] > 0:
            rect.right = tile.left
            collision_types['right'] = True
        elif movement[0] < 0:
            rect.left = tile.right
            collision_types['left'] = True
    rect.y += movement[1]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types['bottom'] = True
        elif movement[1] < 0:
            rect.top = tile.bottom
            collision_types['top'] = True
    return rect, collision_types

player_rect = pygame.Rect(1, 1, player_img.get_width(), player_img.get_height())

background_objects = [[0.25, [120,10,70,400]], [0.25,[280,30,40,400]], [0.5,[30,40,40,400]], [0.5, [130,90,100,400]], [0.5, [300,80,120,400]]]

run = True
while run:
    display.fill((0, 150, 250))



    '''y = 0
    for layer in game_map:
        x = 0
        for tile in layer:
            if tile == '1':
                display.blit(blockImg, (x * TILE_SIZE, y * TILE_SIZE))
            if tile != '0':
                tile_rects.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            x += 1
        y += 1'''

    true_scroll[0] += (player_rect.x - true_scroll[0] - 155)/20
    true_scroll[1] += (player_rect.y - true_scroll[1] - 113)/20
    scroll = true_scroll.copy()
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])

    pygame.draw.rect(display, (7,80,75), pygame.Rect(0,120,300,80))
    for background_object in background_objects:
        obj_rect = pygame.Rect(background_object[1][0] - scroll[0] * background_object[0], background_object[1][1] - scroll[1] * background_object[0], background_object[1][2], background_object[1][3])
        if background_object[0] == 0.5:
            pygame.draw.rect(display, (12,222,150), obj_rect)
        else:
            pygame.draw.rect(display, (91,9,85), obj_rect)

    tile_rects = []
    for y in range(4):
        for x in range(5):
            target_x = x - 1 + int(scroll[0] / (CHUNK_SIZE * 16))
            target_y = y - 1 + int(scroll[1] / (CHUNK_SIZE * 16))
            target_chunk = str(target_x) + ';' + str(target_y)
            if target_chunk not in game_map:
                game_map[target_chunk] = generate_chunk(target_x, target_y)
            for tile in game_map[target_chunk]:
                display.blit(tile_index[tile[1]], (tile[0][0]*16 - scroll[0], tile[0][1]*16 - scroll[1]))
                if tile[1] in [1,2]:
                    tile_rects.append(pygame.Rect(tile[0][0]*16, tile[0][1]*16, 16, 16))




    #tile rendering

    player_movement = [0, 0]
    if moveRight:
        player_movement[0] += 2
    if moveLeft:
        player_movement[0] -= 2
    player_movement[1] += playerYMom
    playerYMom += 0.2
    if playerYMom > 3:
        playerYMom = 3

    if player_movement[0] > 0:
        player_action,player_frame = change_action(player_action, player_frame, 'run')
        player_flip = False
    if player_movement[0] == 0:
        player_action, player_frame = change_action(player_action, player_frame, 'idle')
    if player_movement[0] < 0:
        player_action, player_frame = change_action(player_action, player_frame, 'run')
        player_flip = True

    player_rect, collisions = move(player_rect, player_movement, tile_rects)
    if collisions['bottom']:
        playerYMom = 0
        air_timer = 0
    if collisions['top']:
        playerYMom = 0
    else:
        air_timer += 1

    player_frame += 1
    if player_frame >= len(animation_database[player_action]):
        player_frame = 0
    player_img_id = animation_database[player_action][player_frame]
    player_img = animation_frames[player_img_id]
    display.blit(pygame.transform.flip(player_img,player_flip,False), (player_rect.x - scroll[0], player_rect.y - scroll[1]))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == KEYDOWN:
            if event.key == K_m:
                pygame.mixer.music.fadeout(1000)
            if event.key == K_n:
                pygame.mixer.music.play(-1)
            if event.key == K_RIGHT or event.key == K_d:
                moveRight = True
            if event.key == K_LEFT or event.key == K_a:
                moveLeft = True

            if event.key == K_w or event.key == K_UP or event.key == K_SPACE:
                jump_sound.play()
                if air_timer < 6:

                    playerYMom = -5
        if event.type == KEYUP:
            if event.key == K_RIGHT or event.key == K_d:
                moveRight = False
            if event.key == K_LEFT or event.key == K_a:
                moveLeft = False

    surf = pygame.transform.scale(display, WINDOW_SIZE)
    screen.blit(surf, (0, 0))
    pygame.display.update() #update display
    clock.tick(60) #maintain 60 fps

pygame.quit()