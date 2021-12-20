import time
import pygame
from Agent import qLearningAgent
from Environment import Playground, BuildPlayground

# Initializing the Colours
ORANGE = (255, 165, 0)
GREEN = (0, 150, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

display_height, display_width = 700, 600

pygame.init()
pygame.display.set_caption('Grid environment')
gameDisplay = pygame.display.set_mode((display_width, display_height))
clock = pygame.time.Clock()

game_matrix = BuildPlayground(rows=10, columns=10)
env = Playground(gameDisplay, game_matrix)

# agents are initialized
police = qLearningAgent(env, alpha=0.1, nA=4)
thief = qLearningAgent(env, alpha=0.1, nA=4)

# loading the saved policies from previous run
police.changePolicy('./policy_police.pickle')
thief.changePolicy('./policy_thief.pickle')


# displaying function
def show_info(money, burglar):
    pygame.draw.rect(gameDisplay, BLACK, [0, 600, 600, 5])
    font = pygame.font.SysFont(None, 40)
    text1 = font.render("Thief gets the money: " + str(money), True, GREEN)
    text2 = font.render("Thief gets caught: " + str(burglar), True, RED)

    gameDisplay.blit(text1, (50, 610))
    gameDisplay.blit(text2, (50, 655))


# indicative rectangle to show money grabbed or thief caught
def draw_rect(color, x, y, width, height):
    pygame.draw.rect(gameDisplay, color, [x * width, y * height, width, height], 10)
    pygame.display.update()
    time.sleep(2)


total_thief_caught = 0
total_money_grabbed = 0

numEscapes = 10

# loop over every escape attempted
for escape in range(1, numEscapes + 1):

    state = env.reset()
    action_thief = thief.takeAction(state['thief'])
    action_police = police.takeAction(state['police'])

    # rendering the playground
    env.render(escape)

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        next_state, reward, done, info = env.step(action_thief, action_police)

        gameDisplay.fill(WHITE)
        env.render(escape)
        show_info(total_money_grabbed, total_thief_caught)

        # updating the display
        pygame.display.update()
        clock.tick(30)

        if done:
            if info['money_grabbed']:
                total_money_grabbed += 1
                draw_rect(GREEN, info['x'], info['y'], info['width'], info['height'])

            if info['thief_caught']:
                total_thief_caught += 1
                draw_rect(RED, info['x'], info['y'], info['width'], info['height'])

            break

        # update state and action
        state = next_state
        action_thief = thief.takeAction(state['thief'])
        action_police = police.takeAction(state['police'])

time.sleep(2)
pygame.quit()
