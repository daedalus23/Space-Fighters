import pygame
import os
pygame.font.init()
pygame.mixer.init()


Width, Height = 1000, 500
Win = pygame.display.set_mode((Width, Height))
pygame.display.set_caption("Space Fights")

White = (255, 255, 255)
Black = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

Border = pygame.Rect(Width/2 - 5, 0, 10, Height)

BulletHitSound = pygame.mixer.Sound(os.path.join("assets", "laser-hit.wav"))
BulletFireSound = pygame.mixer.Sound(os.path.join("assets", "laser-shot.wav"))
ExplosionSound = pygame.mixer.Sound(os.path.join("assets", "sci-fi-explosion.wav"))

HealthFont = pygame.font.SysFont("Roboto", 40)
WinnerFont = pygame.font.SysFont("Roboto", 150)

FPS = 60
Bullet_VEL = 7
VEL = 5
Ship_width, Ship_height = 55, 40

PlayerOneHit = pygame.USEREVENT + 1
PlayerTwoHit = pygame.USEREVENT + 2

PlayerOne_ship_img = pygame.image.load(
    os.path.join("assets", "PlayerOne.png"))
PlayerOne_ship = pygame.transform.scale(PlayerOne_ship_img, (Ship_width, Ship_height))
PlayerOne_ship = pygame.transform.flip(PlayerOne_ship, True, False)

PlayerTwo_ship_img = pygame.image.load(
    os.path.join("assets", "PlayerTwo.png"))
PlayerTwo_ship = pygame.transform.scale(PlayerTwo_ship_img, (Ship_width, Ship_height))

Background = pygame.transform.scale(pygame.image.load(os.path.join("assets", "Background.png")), (Width, Height))


def draw_window(playerOne, playerTwo, playerOneBullets, playerTwoBullets, playerOneHealth, playerTwoHealth):
    Win.fill(White)
    Win.blit(Background, (0, 0))
    pygame.draw.rect(Win, Black, Border)

    playerOneHealthText = HealthFont.render(f"Health: {playerOneHealth}", 1, White)
    playerTwoHealthText = HealthFont.render(f"Health: {playerTwoHealth}", 1, White)
    Win.blit(playerOneHealthText, (10, 10))
    Win.blit(playerTwoHealthText, (Width - playerTwoHealthText.get_width() - 10, 10))

    Win.blit(PlayerOne_ship, (playerOne.x, playerOne.y))
    Win.blit(PlayerTwo_ship, (playerTwo.x, playerTwo.y))

    for bullet in playerOneBullets:
        pygame.draw.rect(Win, RED, bullet)
    for bullet in playerTwoBullets:
        pygame.draw.rect(Win, YELLOW, bullet)
    pygame.display.update()


def draw_winner(text):
    drawText = WinnerFont.render(text, 1, White)
    Win.blit(drawText, (Width/2 - drawText.get_width()/2, Height/2 - drawText.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)     # Seconds


def playerOne_handle_movement(keys_pressed, playerOne):
    if keys_pressed[pygame.K_a] and playerOne.x > 0:  # Left
        playerOne.x -= VEL
    if keys_pressed[pygame.K_d] and playerOne.x < 440:  # Right
        playerOne.x += VEL
    if keys_pressed[pygame.K_w] and playerOne.y > 0:  # Up
        playerOne.y -= VEL
    if keys_pressed[pygame.K_s] and playerOne.y < 460:  # Down
        playerOne.y += VEL


def playerTwo_handle_movement(keys_pressed, playerTwo):
    if keys_pressed[pygame.K_j] and playerTwo.x > 505:  # Left
        playerTwo.x -= VEL
    if keys_pressed[pygame.K_l] and playerTwo.x < 945:  # Right
        playerTwo.x += VEL
    if keys_pressed[pygame.K_i] and playerTwo.y > 0:  # Up
        playerTwo.y -= VEL
    if keys_pressed[pygame.K_k] and playerTwo.y < 460:  # Down
        playerTwo.y += VEL


def handle_bullets(playerOneBullets, playerTwoBullets, playerOne, playerTwo):
    for bullet in playerOneBullets:
        bullet.x += Bullet_VEL
        if playerTwo.colliderect(bullet):
            pygame.event.post(pygame.event.Event(PlayerTwoHit))
            playerOneBullets.remove(bullet)
        elif bullet.x > Width:
            playerOneBullets.remove(bullet)

    for bullet in playerTwoBullets:
        bullet.x -= Bullet_VEL
        if playerOne.colliderect(bullet):
            pygame.event.post(pygame.event.Event(PlayerOneHit))
            playerTwoBullets.remove(bullet)
        elif bullet.x < 0:
            playerTwoBullets.remove(bullet)


def main():
    playerOne = pygame.Rect(250, 250, Ship_width, Ship_height)
    playerTwo = pygame.Rect(750, 250, Ship_width, Ship_height)

    playerOneBullets = []
    playerTwoBullets = []
    playerOneHealth = 10
    playerTwoHealth = 10

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL:
                    bullet = pygame.Rect(
                        playerOne.x + playerOne.width,      # X position
                        playerOne.y + playerOne.height/2,   # Y position
                        10,                                 # Width
                        5                                   # Height
                    )
                    playerOneBullets.append(bullet)
                    BulletFireSound.play()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    bullet = pygame.Rect(
                        playerTwo.x,                        # X position
                        playerTwo.y + playerTwo.height/2,   # Y position
                        10,                                 # Width
                        5                                   # Height
                    )
                    playerTwoBullets.append(bullet)
                    BulletFireSound.play()

            if event.type == PlayerOneHit:
                playerOneHealth -= 1
                BulletHitSound.play()

            if event.type == PlayerTwoHit:
                playerTwoHealth -= 1
                BulletHitSound.play()

        winner_text = ""
        if playerOneHealth <= 0:
            ExplosionSound.play()
            winner_text = "Player Two Wins!"
        if playerTwoHealth <= 0:
            ExplosionSound.play()
            winner_text = "Player One Wins!"
        if winner_text != "":
            draw_winner(winner_text)
            break

        keys_pressed = pygame.key.get_pressed()
        playerOne_handle_movement(keys_pressed, playerOne)
        playerTwo_handle_movement(keys_pressed, playerTwo)

        handle_bullets(playerOneBullets, playerTwoBullets, playerOne, playerTwo)
        draw_window(playerOne, playerTwo, playerOneBullets, playerTwoBullets, playerOneHealth, playerTwoHealth)

    main()


if __name__ == "__main__":
    main()
