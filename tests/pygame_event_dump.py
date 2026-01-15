import pygame

pygame.init()
pygame.joystick.init()

if pygame.joystick.get_count() == 0:
    print("No joystick detected")
    quit()

js = pygame.joystick.Joystick(0)
js.init()

print("Joystick:", js.get_name())
print("Buttons:", js.get_numbuttons())
print("Axes:", js.get_numaxes())
print("Hats:", js.get_numhats())
print("---- Move D-pad / press buttons / move sticks ----")

while True:
    for event in pygame.event.get():
        print(event)
