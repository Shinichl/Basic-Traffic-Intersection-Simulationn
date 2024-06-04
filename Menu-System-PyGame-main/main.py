import pygame, sys
from button import Button


pygame.init()

SCREEN = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Menu")

BG = pygame.image.load("assets/Background.png")

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)

    
def play():
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("black")

        PLAY_TEXT = get_font(30).render("This is the PLAY screen.", True, "White")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(640, 260))
        SCREEN.blit(PLAY_TEXT, PLAY_RECT)

        PLAY_BACK = Button(image=None, pos=(640, 460), 
                            text_input="BACK", font=get_font(75), base_color="White", hovering_color="Green")

        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)          
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu()

        pygame.display.update()

def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        # Render text with shadow
        MENU_TEXT_SHADOW = get_font(70).render("TRAFFIC LIGHT SIM", True, "#000000")
        MENU_TEXT = get_font(70).render("TRAFFIC LIGHT SIM", True, "#b68f40")

        # Get rectangles for positioning
        MENU_SHADOW_RECT = MENU_TEXT_SHADOW.get_rect(center=(640 + 3, 100 + 3))  # Adjust position for shadow
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        # Blit shadow text first
        SCREEN.blit(MENU_TEXT_SHADOW, MENU_SHADOW_RECT)

        # Blit main text
        SCREEN.blit(MENU_TEXT, MENU_RECT)

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(660, 350), 
                    text_input="START SIM", font=get_font(40), base_color="Green", hovering_color="White")
        PLAY_BUTTON_SHADOW = get_font(40).render("START SIM", True, "#000000")  # Shadow text
        PLAY_BUTTON_RECT = PLAY_BUTTON_SHADOW.get_rect(center=(660 + 3, 350 + 3))  # Adjust position for shadow
        SCREEN.blit(PLAY_BUTTON_SHADOW, PLAY_BUTTON_RECT)
                          
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 550), 
                            text_input="QUIT", font=get_font(35), base_color="Red", hovering_color="White")

        for button in [PLAY_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()
