import pygame
import random

pygame.init()
# wielkosc okna gry
WIDTH, HEIGHT = 1000, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Connecting the dots!") # nazwa aplikacji która sie wyswietla
BACKGROUND = (0, 0, 0) #zmienna zawierająca kolor tła
FPS = 60 # limit odswiezania ekraniu

#Obraz reprezentujący gracza
PLAYER_IMAGE = pygame.image.load('human.png') #ładuję obrazek pod zmienną
PLAYER_IMAGE = pygame.transform.scale(PLAYER_IMAGE, (70, 70)) #skaluję obrazek pod zmienną
#położenie gracza
player_x = WIDTH // 2
player_y = HEIGHT // 2
movement_speed = 10 #szybkoc poruszania się przy nacinieciu przycisku w pikselach

#OBRAZ GWIAZDKI
STAR_IMAGE = pygame.image.load('star.jpg')
STAR_IMAGE = pygame.transform.scale(STAR_IMAGE, (50, 50))

#LOSOWE POŁOŻENIE GWIAZDKI
star_x = random.randint(0, WIDTH - STAR_IMAGE.get_width())
star_y = random.randint(0, HEIGHT - STAR_IMAGE.get_height())

#OBRAZ CZASZKI
SKULL_IMAGE = pygame.image.load('skull.jpg')
SKULL_IMAGE = pygame.transform.scale(SKULL_IMAGE, (80, 60))

#LOSOWE POŁOŻENIE CZASZKI
skull_x = random.randint(0, WIDTH - SKULL_IMAGE.get_width())
skull_y = random.randint(0, HEIGHT - SKULL_IMAGE.get_height())

#zmienna reprezentująca punktacje i ilosc zyc
score = 0
lost_lives = 3
font = pygame.font.Font(None, 36)

#zmienna zmieniająca stan wyganej
game_won = False
game_lost = False

#lista przechowująca pozycje czaszek w każdej iteracji gry
skull_positions = []


     
   
#GŁÓWNA PĘTLA GRY   
def start_game():
    

    global player_x, player_y, star_x, star_y, skull_x, skull_y, score
    global game_won, game_lost, lost_lives #robimy te zmienne jako globalne żeby funkcja mogla je widziec
    
    clock = pygame.time.Clock()
    run = True
    spawn_skulls()
    
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                
                
        #RUCH GRACZA
        keys = pygame.key.get_pressed() #sprawdza czy przycisk jest wcisniety
        if keys[pygame.K_w]:
            player_y -= movement_speed
        if keys[pygame.K_s]:
            player_y += movement_speed
        if keys[pygame.K_a]: 
            player_x -= movement_speed
        if keys[pygame.K_d]:
            player_x += movement_speed
        
        #OGRANICZENIE RUCHU DO WIELKOŚCI OKNA
        player_x = max(0, min(player_x, WIDTH - PLAYER_IMAGE.get_width()))
        player_y = max(0, min(player_y, HEIGHT - PLAYER_IMAGE.get_height()))
        
        #WYKRYWANIE KOLIZJI GRACZ-CZASZKA
        player_rect = pygame.Rect(player_x, player_y, PLAYER_IMAGE.get_width(), PLAYER_IMAGE.get_height())
        if check_collision_with_skull(player_rect):
            lost_lives -= 1
            spawn_skulls()
            
           
        
        #WYKRYWANIE KOLIZJI GRACZ-GWIAZDKA
        if not game_won and not game_lost:
            player_rect = pygame.Rect(player_x, player_y, PLAYER_IMAGE.get_width(), PLAYER_IMAGE.get_height())
            star_rect = pygame.Rect(star_x, star_y, STAR_IMAGE.get_width(), STAR_IMAGE.get_height())
            
            if player_rect.colliderect(star_rect):
                score += 1
                # Nowa pozycja gwiazdki
                star_x = random.randint(0, WIDTH - STAR_IMAGE.get_width())
                star_y = random.randint(0, HEIGHT - STAR_IMAGE.get_height())
                spawn_skulls()
            
            #jesli zebrano x punktow - przerywamy petlea
            if check_victory():
                game_won = True
                run = False
            
            if lost_lives == 0:
                game_lost = True
                run = False
            
        
            #rysujemy odswiezone okno    
            draw_window(player_x, player_y)
       
        
    pygame.quit()
    
#FUNKCJA RYSUJĄCA RZECZY NA EKRANIE
def draw_window(x, y):
     if not game_won and not game_lost:
         WIN.fill(BACKGROUND)
         WIN.blit(PLAYER_IMAGE, (x, y))
         WIN.blit(STAR_IMAGE, (star_x, star_y))
        
         for skull_x, skull_y in skull_positions:
            WIN.blit(SKULL_IMAGE, (skull_x, skull_y))
        
         score_text = font.render(f"Zdobyte gwiazdki: {score}", True, (255, 255, 255))
         lost_text = font.render(f"Pozostałe życia: {lost_lives}", True, (255, 255, 255))
      
         WIN.blit(score_text, (10, 10))
         WIN.blit(lost_text, (10, 50))
     elif game_won:
         win_text = font.render("Gratulacje, wygrałeś!", True, (0, 255, 0))
         text_rect = win_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
         WIN.blit(win_text, text_rect)
     elif game_lost:
         lost_text = font.render('Przegrałes, nacisnij ESC zeby wyjsc.', True, (0, 255, 0))
         text_rect = lost_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
         WIN.blit(lost_text, text_rect)
     
          
     pygame.display.update() 
     
#Funkcja sprawdzająca czy zdobyto okreslona liczbe punktów
def check_victory():
    if score >= 10:
        print("Gratulacje! Wygrałeś!")
        return True
    return False

#funkcja generująca czaszki na ekranie
def spawn_skulls(num_skulls=3):
    global skull_positions
    skull_positions = []  # Resetujemy pozycje przeszkód przy iteracji
    
    for var in range(num_skulls):
        while True: #pętla sprawdzającza czy czaszka nie spawnuje na graczu
            x = random.randint(0, WIDTH - SKULL_IMAGE.get_width())
            y = random.randint(0, HEIGHT - SKULL_IMAGE.get_height())
            
            player_rect = pygame.Rect(player_x, player_y, PLAYER_IMAGE.get_width(), PLAYER_IMAGE.get_height())
            skull_rect = pygame.Rect(x, y, SKULL_IMAGE.get_width(), SKULL_IMAGE.get_height())
            
            if not player_rect.colliderect(skull_rect):
                skull_positions.append((x, y))
                break
            
#funkcja sprawdzająca czy zaszła kolizja z czaszką
def check_collision_with_skull(player_rect):
    for skull_x, skull_y in skull_positions:
        skull_rect = pygame.Rect(skull_x, skull_y, SKULL_IMAGE.get_width(), SKULL_IMAGE.get_height())
        if player_rect.colliderect(skull_rect):
            return True
    return False


     
if __name__ == '__main__':
    start_game()



