import pygame

pygame.init()
pygame.joystick.init()

if pygame.joystick.get_count() == 0:
    print("No controller detected")
    quit()

js = pygame.joystick.Joystick(0)
js.init()

print("Controller:", js.get_name())
print("Press buttons (Ctrl+C to quit)")

while True:
    pygame.event.pump()  # process events
    

    for i in range(js.get_numbuttons()):
        if js.get_button(i):
            print("Button", i, "pressed")
