
import pygame, sys, random, json 

def draw_floor():
	screen.blit(floor_surface,(floor_x_pos,900))
	screen.blit(floor_surface,(floor_x_pos + 576,900))

def create_pipe():
	random_pipe_pos = random.choice(pipe_height)
	bottom_pipe = pipe_surface.get_rect(midtop = (700,random_pipe_pos))
	top_pipe = pipe_surface.get_rect(midbottom = (700,random_pipe_pos - 300))
	return bottom_pipe,top_pipe

def move_pipes(pipes, pipe_speed):
	for pipe in pipes:
		pipe.centerx -= pipe_speed
	return pipes

def draw_pipes(pipes):
	for pipe in pipes:
		if pipe.bottom >= 1024:
			screen.blit(pipe_surface,pipe)
		else:
			flip_pipe = pygame.transform.flip(pipe_surface,False,True)
			screen.blit(flip_pipe,pipe)

def remove_pipes(pipes):
	for pipe in pipes:
		if pipe.centerx == -600:
			pipes.remove(pipe)
	return pipes
def check_collision(pipes, health):
	for pipe in pipes:
		if bird_rect.colliderect(pipe):
			death_sound.play()
			return False

	if bird_rect.top <= -100 or bird_rect.bottom >= 900:
		return False

	return True

def rotate_bird(bird):
	new_bird = pygame.transform.rotozoom(bird,-bird_movement * 3,1)
	return new_bird

def bird_animation():
	new_bird = bird_frames[bird_index]
	new_bird_rect = new_bird.get_rect(center = (100,bird_rect.centery))
	return new_bird,new_bird_rect

def score_display(game_state):
	if game_state == 'main_game':
		score_surface = game_font.render(str(int(score)),True,(255,255,255))
		score_rect = score_surface.get_rect(center = (288,100))
		gravity_surface = game_font.render(str(gravity),True,(255,255,255))
		gravity_rect = gravity_surface.get_rect(center = (100, 870))
		gravity_icon_surface = pygame.image.load('assets/sprites/gravity.png')
		gravity_icon_surface = pygame.transform.scale2x(gravity_icon_surface)
		gravity_icon_rect = gravity_icon_surface.get_rect(center = (30, 870))

		pipe_speed_surface = game_font.render(str(pipe_speed),True,(255,255,255))
		pipe_speed_rect = gravity_surface.get_rect(center = (100, 800))
		pipe_speed_icon_surface = pygame.image.load('assets/sprites/pipe_speed.png')
		pipe_speed_icon_surface = pygame.transform.scale2x(pipe_speed_icon_surface)
		pipe_speed_icon_rect = gravity_icon_surface.get_rect(center = (30, 800))
		screen.blit(score_surface,score_rect)
		screen.blit(gravity_surface,gravity_rect)
		screen.blit(gravity_icon_surface,gravity_icon_rect)
		screen.blit(pipe_speed_icon_surface,pipe_speed_icon_rect)
		screen.blit(pipe_speed_surface,pipe_speed_rect)
 
	if game_state == 'game_over':
		score_surface = game_font.render(f'Score: {int(score)}' ,True,(255,255,255))
		score_rect = score_surface.get_rect(center = (288,100))
		screen.blit(score_surface,score_rect)
		high_score_surface = game_font.render(f'High score: {int(high_score)}',True,(255,255,255))
		high_score_rect = high_score_surface.get_rect(center = (288,850))
		screen.blit(high_score_surface,high_score_rect)

def update_score(score, high_score):
	if score > high_score:
		high_score = score
	return high_score


game_icon = pygame.image.load('assets/sprites/icon.png')
pygame.display.set_icon(game_icon)
pygame.display.set_caption("Floating")


def choose_gravity_atribute():
	gravity = random.choice(gravity_options)
	return gravity


def choose_pipe_speed_atribute():
	pipe_speed = random.choice(pipe_speed_options)
	return pipe_speed

pygame.mixer.pre_init(frequency = 44100, size = 16, channels = 1, buffer = 512)
pygame.init()
screen = pygame.display.set_mode((576,1024))
clock = pygame.time.Clock()
game_font = pygame.font.Font('font.ttf',40)

# Game Variables
gravity_options = [0.25, 0.30, 0.20, 0.15]
pipe_speed_options = [3, 5, 7, 9]
pipe_speed = (choose_pipe_speed_atribute())
gravity = (choose_gravity_atribute())
bird_movement = 0
game_active = True
score = 0
high_score = 0


bg_surface = pygame.image.load('assets/backgrounds/background-day.png').convert()
bg_surface = pygame.transform.scale2x(bg_surface)

floor_surface = pygame.image.load('assets/sprites/base.png').convert()
floor_surface = pygame.transform.scale2x(floor_surface)
floor_x_pos = 0

bird_downflap = pygame.transform.scale2x(pygame.image.load('assets/sprites/bluebird-downflap.png').convert_alpha())
bird_midflap = pygame.transform.scale2x(pygame.image.load('assets/sprites/bluebird-midflap.png').convert_alpha())
bird_upflap = pygame.transform.scale2x(pygame.image.load('assets/sprites/bluebird-upflap.png').convert_alpha())
bird_frames = [bird_downflap,bird_midflap,bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center = (100,512))

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP,200)

pipe_surface = pygame.image.load('assets/sprites/pipe-green.png')
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE,900)
pipe_height = [400,600,800,500]

game_over_surface = pygame.transform.scale2x(pygame.image.load('assets/sprites/message.png').convert_alpha())
game_over_rect = game_over_surface.get_rect(center = (288,512))

flap_sound = pygame.mixer.Sound('assets/audio/wing.wav')
death_sound = pygame.mixer.Sound('assets/audio/die.wav')
score_sound = pygame.mixer.Sound('assets/audio/point.wav')
score_sound_countdown = 100


health = 0

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE and game_active:
				bird_movement = 0
				bird_movement -= 8
				flap_sound.play()
			if event.key == pygame.K_SPACE and game_active == False:
				game_active = True
				pipe_list.clear()
				bird_rect.center = (100,512)
				bird_movement = 0
				score = 0
			if event.key == pygame.K_LSHIFT and game_active == True:
				gravity = 1
				gravity -= 0.2
			if event.key != pygame.K_LSHIFT and game_active == True:
				gravity = (choose_gravity_atribute())

		if event.type == SPAWNPIPE:
			pipe_list.extend(create_pipe())

		if event.type == BIRDFLAP:
			if bird_index < 2:
				bird_index += 1
			else:
				bird_index = 0

			bird_surface,bird_rect = bird_animation()

	screen.blit(bg_surface,(0,0))

	if game_active:
		# Bird
		bird_movement += gravity
		rotated_bird = rotate_bird(bird_surface)
		bird_rect.centery += bird_movement
		screen.blit(rotated_bird,bird_rect)
		game_active = check_collision(pipe_list, health)

		# Pipes
		pipe_list = move_pipes(pipe_list, pipe_speed)
		pipe_list = remove_pipes(pipe_list)
		draw_pipes(pipe_list)
		
		score += 0.010
		score_display('main_game')
		score_sound_countdown -= 1
		if score_sound_countdown <= 0:
			score_sound.play()
			score_sound_countdown = 70
	else:
		screen.blit(game_over_surface,game_over_rect)
		high_score = update_score(score,high_score)
		score_display('game_over')


	# Floor
	floor_x_pos -= 1
	draw_floor()
	if floor_x_pos <= -576:
		floor_x_pos = 0
	

	pygame.display.update()
	clock.tick(100)