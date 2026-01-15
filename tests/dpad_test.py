import pygame

pygame.init()
pygame.joystick.init()

if pygame.joystick.get_count() == 0:
    print("No joystick detected")
    quit()

js = pygame.joystick.Joystick(0)
js.init()

print("Joystick connected:", js.get_name())
print("Move the D-pad (Ctrl+C to quit)")

while True:
    for event in pygame.event.get():

        if event.type == pygame.JOYHATMOTION:
            hat = event.hat   
            x, y = event.value   

            print(f"HAT {hat} moved: x={x}, y={y}")

            if (x, y) == (0, 1):
                print("D-pad UP")
            elif (x, y) == (0, -1):
                print("D-pad DOWN")
            elif (x, y) == (-1, 0):
                print("D-pad LEFT")
            elif (x, y) == (1, 0):
                print("D-pad RIGHT")

