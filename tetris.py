# import libraries
import pygame
from main import *


def update_graphics(block, next_block, playing_field, player):
    # Sets black background and text
    DISPLAY_SCREEN.blit(background_img, (0, 0))
    pygame.draw.rect(DISPLAY_SCREEN, black, (off_set_x, off_set_y, playing_field_width, playing_field_height))
    font = pygame.font.SysFont("comicsansms", 48)
    rendered_text = font.render("Tetris", 1, orange)
    DISPLAY_SCREEN.blit(rendered_text, (width / 2 - 80, 10))

    # Displays Current score and time
    player.time_since_start = pygame.time.get_ticks() - player.start_time
    font = pygame.font.SysFont("comicsansms", 20)
    rendered_text_time = font.render("Time: " + str(player.time_since_start), 1, orange)
    DISPLAY_SCREEN.blit(rendered_text_time, (playing_field_width + tile_length * 2, playing_field_height - 80))
    rendered_text_score = font.render("Score: " + str(player.score), 1, orange)
    DISPLAY_SCREEN.blit(rendered_text_score, (playing_field_width + tile_length * 2, playing_field_height - 50))
    # Draw the small screen for the next block
    draw_small_screen(next_block)

    # Set tiles
    y = off_set_y
    for i in range(20):
        for tile in playing_field.tiles["row" + str(i + 1)][y]:
            tile.draw_tile()
        y += tile_length

    # Blocks while falling
    for tile in block.tiles:
        if tile.y >= off_set_y:
            tile.draw_tile()

    # Sets borders
    pygame.draw.line(DISPLAY_SCREEN, blue, (off_set_x - 2, off_set_y - 3),
                     (playing_field_width + off_set_x + 1, off_set_y - 3), 4)  # horizontal line top
    pygame.draw.line(DISPLAY_SCREEN, blue, (off_set_x - 2, off_set_y + playing_field_height + 1),
                     (playing_field_width + off_set_x + 1, off_set_y + playing_field_height + 1),
                     4)  # horizontal line bottom
    pygame.draw.line(DISPLAY_SCREEN, blue, (off_set_x - 3, off_set_y - 3),
                     (off_set_x - 3, off_set_y + playing_field_height + 1), 4)  # vertical line left
    pygame.draw.line(DISPLAY_SCREEN, blue, (playing_field_width + off_set_x + 1, off_set_y - 3),
                     (playing_field_width + off_set_x + 1, off_set_y + playing_field_height + 1),
                     4)  # vertical line right

    # Sets Grid
    current_y_horizontal_lines = off_set_y
    current_x_vertical_lines = off_set_x
    for i in range(19):
        current_y_horizontal_lines += 33
        pygame.draw.line(DISPLAY_SCREEN, white, (off_set_x, current_y_horizontal_lines),
                         (playing_field_width + off_set_x - 1, current_y_horizontal_lines))  # horizontal line top
    for j in range(9):
        current_x_vertical_lines += 33
        pygame.draw.line(DISPLAY_SCREEN, white, (current_x_vertical_lines - 1, off_set_y),
                         (current_x_vertical_lines - 1, playing_field_height + off_set_y))  # horizontal line top

    pygame.display.update()


def draw_small_screen(next_block):
    # Sets background
    pygame.draw.rect(DISPLAY_SCREEN, black,
                     (playing_field_width + tile_length * 2, height / 2 - 20, 6 * tile_length, 6 * tile_length))

    # Sets borders
    pygame.draw.line(DISPLAY_SCREEN, blue, (playing_field_width + tile_length * 2 - 2, height / 2 - 20 - 2),
                     ((6 * tile_length) + (playing_field_width + tile_length * 2), (height / 2 - 20 - 2)),
                     3)  # horizontal line top
    pygame.draw.line(DISPLAY_SCREEN, blue,
                     (playing_field_width + tile_length * 2 - 2, height / 2 - 20 + (6 * tile_length)),
                     ((6 * tile_length) + (playing_field_width + tile_length * 2), height / 2 - 20 + (6 * tile_length)),
                     3)  # horizontal line bottom
    pygame.draw.line(DISPLAY_SCREEN, blue, (playing_field_width + tile_length * 2 - 2, height / 2 - 20 - 2),
                     (playing_field_width + tile_length * 2 - 2, height / 2 - 20 + (6 * tile_length)),
                     3)  # vertical line left
    pygame.draw.line(DISPLAY_SCREEN, blue,
                     ((6 * tile_length) + (playing_field_width + tile_length * 2), height / 2 - 20 - 2),
                     ((6 * tile_length) + (playing_field_width + tile_length * 2), height / 2 - 20 + (6 * tile_length)),
                     3)  # vertical line right

    # Sets text
    font = pygame.font.SysFont("comicsansms", 30)
    rendered_text = font.render("Next Block", 1, orange)
    DISPLAY_SCREEN.blit(rendered_text, (playing_field_width + tile_length * 2, height / 2 - 70))

    # Displays next block
    temp_block = Block(next_block.shape, next_block.color)
    temp_block.tiles = [Tile(playing_field_width + tile_length * 2 + 2 * tile_length, height / 2 - 20 + 4 * tile_length,
                             next_block.color), Tile(0, 0, next_block.color), Tile(0, 0, next_block.color),
                        Tile(0, 0, next_block.color)]
    temp_block.complete_block()

    for tile in temp_block.tiles:
        tile.draw_tile()


def is_game_over(playing_field, player):
    y = off_set_y
    for i in range(20):
        for tile in playing_field.tiles["row" + str(i + 1)][y]:
            if not tile.empty and tile.y <= off_set_y:
                temp_y = off_set_y
                for j in range(20):
                    for tile in playing_field.tiles["row" + str(j + 1)][temp_y]:
                        tile.draw_tile()
                    temp_y += tile_length

                font = pygame.font.SysFont("comicsansms", 48)
                rendered_text = font.render("GAME OVER", 1, white)
                DISPLAY_SCREEN.blit(rendered_text, (off_set_x + 20, playing_field_height / 2))
                pygame.display.update()

                time.sleep(2)
                introduction(player)
        y += tile_length


def start_game():
    global best_score
    global longest_time

    rand_index = random.randint(0, 6)
    block = Block(shapes[rand_index], block_colors[rand_index])

    next_rand_index = random.randint(0, 6)
    next_block = Block(shapes[next_rand_index], block_colors[next_rand_index])

    playing_field = PlayingField()
    start_time = pygame.time.get_ticks()
    player = Player(start_time)

    while True:
        update_graphics(block, next_block, playing_field, player)

        (block, next_block, is_new) = block.get_new_block(next_block, playing_field, player)
        if is_new:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            pygame.event.clear()

        manage_events(block, next_block, playing_field, player)
        update_graphics(block, next_block, playing_field, player)

        block.block_is_falling(next_block, playing_field, player)
        update_graphics(block, next_block, playing_field, player)

        playing_field.destory_full_row(player)
        update_graphics(block, next_block, playing_field, player)

        if player.score > best_score:
            best_score = player.score
        if player.time_since_start > longest_time:
            longest_time = player.time_since_start

        is_game_over(playing_field, player)
        update_graphics(block, next_block, playing_field, player)

        pygame.display.update()
        clock.tick(60)


def manage_events(block, next_block, playing_field, player):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                # move the block to the left
                block.move_left(playing_field)
            elif event.key == pygame.K_RIGHT:
                # move the block to the right
                block.move_right(playing_field)
            elif event.key == pygame.K_UP:
                # rotate block
                block.rotate(next_block, playing_field, player)
            if event.key == pygame.K_SPACE:
                # let the block fall completely
                block.fall_completely(next_block, playing_field, player)
            if event.key == pygame.K_DOWN:
                # let the block fall down faster
                block.block_is_falling(next_block, playing_field, player, "faster")

    update_graphics(block, next_block, playing_field, player)


def introduction(player=None):
    button_width = 300
    button_height = 90

    # start_x_button = width/2-button_width/2
    play_button = Button(blue, orange, -400, height / 2, button_width, button_height, 32, black, white, "PLAY")
    instructions_button = Button(blue, orange, width + 150, height / 2 + button_height + 10, button_width,
                                 button_height, 32, black, white, "INSTRUCTIONS")
    quit_button = Button(blue, orange, -400, height / 2 + button_height * 2 + 20, button_width, button_height, 32,
                         black, white, "QUIT")

    font = pygame.font.SysFont("comicsansms", 48)
    rendered_text = font.render("Tetris", 1, black)
    rendered_text_y = height

    # To draw the Tetris text in an animated way
    while rendered_text_y > 10:
        DISPLAY_SCREEN.blit(background_img, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        rendered_text_y -= 1.5
        DISPLAY_SCREEN.blit(rendered_text, (width / 2 - 80, rendered_text_y))
        pygame.display.update()

    # To draw the score and time texts in an animated way
    if player:
        font_small = pygame.font.SysFont("comicsansms", 30)
        rendered_current_score = font_small.render("Current Score: " + str(player.score), 1, orange)
        rendered_best_score = font_small.render("Best Score: " + str(best_score), 1, orange)
        rendered_current_time = font_small.render("Current Time: " + str(player.time_since_start), 1, orange)
        rendered_longest_time = font_small.render("Longest Time: " + str(longest_time), 1, orange)

        rendered_current_score_y = height
        rendered_best_score_y = height + 40
        rendered_current_time_y = height + 80
        rendered_longest_time_y = height + 120

        while rendered_current_score_y > 150:
            DISPLAY_SCREEN.blit(background_img, (0, 0))
            DISPLAY_SCREEN.blit(rendered_text, (width / 2 - 80, rendered_text_y))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            rendered_current_score_y -= 1.5
            rendered_best_score_y -= 1.5
            rendered_current_time_y -= 1.5
            rendered_longest_time_y -= 1.5

            DISPLAY_SCREEN.blit(rendered_current_score, (off_set_x, rendered_current_score_y))
            DISPLAY_SCREEN.blit(rendered_best_score, (off_set_x + 45, rendered_best_score_y))
            DISPLAY_SCREEN.blit(rendered_current_time, (off_set_x + 15, rendered_current_time_y))
            DISPLAY_SCREEN.blit(rendered_longest_time, (off_set_x + 15, rendered_longest_time_y))

            pygame.display.update()

    # To draw the buttons in an animated way
    while play_button.x < width / 2 - button_width / 2 or instructions_button.x > width / 2 - button_width / 2:
        DISPLAY_SCREEN.blit(background_img, (0, 0))
        DISPLAY_SCREEN.blit(rendered_text, (width / 2 - 80, rendered_text_y))
        if player:
            DISPLAY_SCREEN.blit(rendered_current_score, (off_set_x, rendered_current_score_y))
            DISPLAY_SCREEN.blit(rendered_best_score, (off_set_x + 45, rendered_best_score_y))
            DISPLAY_SCREEN.blit(rendered_current_time, (off_set_x + 15, rendered_current_time_y))
            DISPLAY_SCREEN.blit(rendered_longest_time, (off_set_x + 15, rendered_longest_time_y))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if play_button.x < width / 2 - button_width / 2:
            play_button.x += 3
            quit_button.x += 3
        if instructions_button.x > width / 2 - button_width / 2:
            instructions_button.x -= 3

        play_button.blit(DISPLAY_SCREEN)
        instructions_button.blit(DISPLAY_SCREEN)
        quit_button.blit(DISPLAY_SCREEN)
        pygame.display.update()

    run = True
    while run:
        DISPLAY_SCREEN.blit(background_img, (0, 0))
        DISPLAY_SCREEN.blit(rendered_text, (width / 2 - 80, rendered_text_y))
        if player:
            DISPLAY_SCREEN.blit(rendered_current_score, (off_set_x, rendered_current_score_y))
            DISPLAY_SCREEN.blit(rendered_best_score, (off_set_x + 45, rendered_best_score_y))
            DISPLAY_SCREEN.blit(rendered_current_time, (off_set_x + 15, rendered_current_time_y))
            DISPLAY_SCREEN.blit(rendered_longest_time, (off_set_x + 15, rendered_longest_time_y))

        # Get the position of the mouse
        mouse_position = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.is_clicked(mouse_position, event):
                    start_game()
                    run = False
                elif instructions_button.is_clicked(mouse_position, event):
                    instructions(player)
                    run = False
                elif quit_button.is_clicked(mouse_position, event):
                    pygame.quit()
                    sys.exit()

        if play_button.is_hovered_over(mouse_position):
            play_button.blit_hovered_over(DISPLAY_SCREEN)
        else:
            play_button.blit(DISPLAY_SCREEN, gray)
        if instructions_button.is_hovered_over(mouse_position):
            instructions_button.blit_hovered_over(DISPLAY_SCREEN)
        else:
            instructions_button.blit(DISPLAY_SCREEN, gray)
        if quit_button.is_hovered_over(mouse_position):
            quit_button.blit_hovered_over(DISPLAY_SCREEN)
        else:
            quit_button.blit(DISPLAY_SCREEN, gray)

        clock.tick(60)
        pygame.display.update()

