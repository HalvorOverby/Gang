# Import and initialize the pygame library
import pygame


pygame.init()
 
# Set up the drawing window
screen = pygame.display.set_mode([500, 500])

# Run until the user asks to quit
running = True
while running: 
# Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((248, 249, 249))
    pygame.draw.circle(screen, (0, 0, 255), (250, 250), 75)
  # Flip the display
    pygame.display.flip()
pygame.quit()