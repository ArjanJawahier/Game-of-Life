import tkinter as tk
import pygame
import os
import Cell
import math

# Quick note: program only works on windows

game_started = False
mode = "defautl"
DEFAULT_GAME_WIDTH = 1000
DEFAULT_GAME_HEIGHT = 750
DEFAULT_CELL_WIDTH = 5
DEFAULT_CELL_HEIGHT = 5
DEFAULT_CELL_MARGIN = 1

game_of_life_width = 1000
game_of_life_height = 750
cell_width = 5
cell_height = 5
cell_margin = 0

grid_cells = []

def create_grid(cell_width, cell_height, cell_margin, grid_width, grid_height, screen):
    print(grid_width, grid_height)
    for i in range(grid_height):
        for j in range(grid_width):
            grid_cells.append(Cell.Cell(cell_margin + j*(cell_width + cell_margin), cell_margin + i*(cell_height + cell_margin), cell_width, cell_height, (0, 0, 0), screen))

def update_cell_translated_position():
    for cell in grid_cells:
        cell.translated_x = cell.x
        cell.translated_y = cell.y

def translate_grid(translate_pos, screen):
    current_x_diff = pygame.mouse.get_pos()[0] - translate_pos[0]
    current_y_diff = pygame.mouse.get_pos()[1] - translate_pos[1]
    screen.fill(pygame.Color(10, 10, 10))  # dark-greyish background colour
    for cell in grid_cells:
        cell.x = cell.translated_x + current_x_diff
        cell.y = cell.translated_y + current_y_diff
        pygame.draw.rect(screen, cell.color, (cell.x, cell.y, cell.width, cell.height))

def update_game_of_life_default(grid_width, grid_height):
    for i, cell in enumerate(grid_cells):
        neightbours = [grid_cells[i-grid_width-1], grid_cells[i-grid_width], grid_cells[i-grid_width+1], grid_cells[i-1], grid_cells[(i+1)%(grid_width*grid_height)], grid_cells[(i+grid_width-1)%(grid_width*grid_height)], grid_cells[(i+grid_width)%(grid_width*grid_height)], grid_cells[(i+grid_width+1)%(grid_width*grid_height)]]
        number_of_alive_neightbours = 0
        for neighbour in neightbours:
            if neighbour.state == "alive":
                number_of_alive_neightbours += 1
        cell.number_of_alive_neightbours = number_of_alive_neightbours
    # Another for loop cause this has to be done after all the alive neighbours have been counted of each cell
    for cell in grid_cells:
        # Rule 1: Any live cell with fewer than two live neighbours dies, as if by underpopulation.
        if cell.state == "alive" and cell.number_of_alive_neightbours < 2:
            cell.set_dead()
        # Rule 2: Any live cell with two or three live neighbors lives on to the next generation.
            # don't have to write any code here
        # Rule 3: Any live cell with more than three live neighbors dies, as if by overpopulation.
        if cell.state == "alive" and cell.number_of_alive_neightbours > 3:
            cell.set_dead()
        # Rule 4: Any dead cell with exactly three live neighbors becomes a live cell, as if by reproduction.
        if cell.state == "dead" and cell.number_of_alive_neightbours == 3:
            cell.set_alive()

def update_game_of_life_bacteria(grid_width, grid_height):
    for i, cell in enumerate(grid_cells):
        neightbours = [grid_cells[i-grid_width-1], grid_cells[i-grid_width], grid_cells[i-grid_width+1], grid_cells[i-1], grid_cells[(i+1)%(grid_width*grid_height)], grid_cells[(i+grid_width-1)%(grid_width*grid_height)], grid_cells[(i+grid_width)%(grid_width*grid_height)], grid_cells[(i+grid_width+1)%(grid_width*grid_height)]]
        number_of_alive_neightbours = 0
        for neighbour in neightbours:
            if neighbour.state == "alive":
                number_of_alive_neightbours += 1
        # Cells get evaluated 1 by 1
        # Rule 1: Any live cell with fewer than two live neighbours dies, as if by underpopulation.
        if cell.state == "alive" and number_of_alive_neightbours < 2:
            cell.set_dead()
        # Rule 2: Any live cell with two or three live neighbors lives on to the next generation.
            # don't have to write any code here
        # Rule 3: Any live cell with more than three live neighbors dies, as if by overpopulation.
        if cell.state == "alive" and number_of_alive_neightbours > 3:
            cell.set_dead()
        # Rule 4: Any dead cell with exactly three live neighbors becomes a live cell, as if by reproduction.
        if cell.state == "dead" and number_of_alive_neightbours == 3:
            cell.set_alive()

def start_game_of_life():
    global game_started
    game_started = True

def pause_game_of_life():
    global game_started
    game_started = False

def reset_game_of_life():
    pause_game_of_life()
    game_of_life_width = DEFAULT_GAME_WIDTH
    game_of_life_height = DEFAULT_GAME_HEIGHT
    cell_width = DEFAULT_CELL_WIDTH
    cell_height = DEFAULT_CELL_HEIGHT
    cell_margin = DEFAULT_CELL_MARGIN
    for cell in grid_cells:
        cell.reset_to_defaults()


def set_default_mode():
    global mode
    mode = "default"

def set_bacteria_mode():
    global mode
    mode = "bacteria"

def zoom(grid_width, grid_height, grid_mouse_column, grid_mouse_row, size_change, screen):
    global cell_width
    global cell_height
    screen.fill(pygame.Color(10, 10, 10))  # dark-greyish background colour
    if (cell_width < 80 and size_change > 0) or (cell_width > 1 and size_change < 0):
        cell_width += size_change
        cell_height += size_change
        for idx, cell in enumerate(grid_cells):
            cell.width += size_change
            cell.height += size_change
            # calculations for the new position of a cell
            idx_cell_column = idx % grid_width
            idx_cell_row = math.floor(idx / grid_width)
            col_diff = idx_cell_column - grid_mouse_column
            row_diff = idx_cell_row - grid_mouse_row
            cell.x += col_diff * size_change
            cell.y += row_diff * size_change
            cell.translated_x = cell.x
            cell.translated_y = cell.y
            pygame.draw.rect(screen, cell.color, (cell.x, cell.y, cell.width, cell.height))


def main():
    root = tk.Tk()
    root.title('Game of Life')
    pygameframe = tk.Frame(root, width = game_of_life_width, height = game_of_life_height)
    pygameframe.grid(columnspan=(game_of_life_width), rowspan=game_of_life_height)  # Adds grid
    pygameframe.pack(side = tk.BOTTOM)
    uiframe =  tk.Frame(root)
    uiframe.pack()
    os.environ['SDL_WINDOWID'] = str(pygameframe.winfo_id())
    os.environ['SDL_VIDEODRIVER'] = 'windib'    # Windows driver
    screen = pygame.display.set_mode((game_of_life_width, game_of_life_height))
    screen.fill(pygame.Color(10, 10, 10)) # dark-greyish background colour

    start_button = tk.Button(uiframe, text = "Start", command=start_game_of_life)
    start_button.pack(side = tk.LEFT)
    pause_button = tk.Button(uiframe, text = "Pause", command=pause_game_of_life)
    pause_button.pack(side=tk.LEFT)
    reset_button = tk.Button(uiframe, text="Reset", command=reset_game_of_life)
    reset_button.pack(side=tk.LEFT)
    menubar = tk.Menu(root)
    mode_menu = tk.Menu(menubar, tearoff=0) # menu button for choosing the program mode
    mode_menu.add_command(label="Default Game of Life", command=set_default_mode)
    mode_menu.add_command(label="Bacteria (cells get evaluated in order)", command=set_bacteria_mode)
    menubar.add_cascade(label="Mode", menu=mode_menu)
    root.config(menu=menubar)

    grid_width = int(game_of_life_width / (cell_width + cell_margin))
    grid_height = int(game_of_life_height / (cell_height + cell_margin))

    pygame.display.init()
    create_grid(cell_width, cell_height, cell_margin, grid_width, grid_height, screen)
    pygame.display.update()
    clock = pygame.time.Clock()
    translate_pos = (game_of_life_width/2, game_of_life_height/2)

    while True:
        if game_started:
            if mode == "default":
                update_game_of_life_default(grid_width, grid_height)
            elif mode == "bacteria":
                update_game_of_life_bacteria(grid_width, grid_height)

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 2:
                    # click the middle mouse button , used for translating the grid
                    translate_pos = pygame.mouse.get_pos()
                if event.button == 4:
                    # scroll up with middle mouse wheel
                    zoom(grid_width, grid_height, grid_mouse_column, grid_mouse_row, 1, screen)
                if event.button == 5:
                    # scroll down with middle mouse wheel
                    zoom(grid_width, grid_height, grid_mouse_column, grid_mouse_row, -1, screen)
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 2:
                    # released the middle mouse button, so each cell's translated position gets updated
                    update_cell_translated_position()
            if event.type == pygame.MOUSEMOTION and pygame.mouse.get_pressed() == (0, 1, 0):
                translate_grid(translate_pos, screen)
            if game_started == False:
                grid_mouse_column = int(
                    (pygame.mouse.get_pos()[0] - grid_cells[0].x - cell_margin) / (cell_width + cell_margin))
                grid_mouse_row = int(
                    (pygame.mouse.get_pos()[1] - grid_cells[0].y - cell_margin) / (cell_height + cell_margin))
                grid_index = grid_mouse_column + grid_mouse_row * grid_width
                if event.type == pygame.MOUSEMOTION and pygame.mouse.get_pressed() == (1, 0, 0):
                    grid_cells[grid_index].set_alive()  # marks cells as alive if clicked on them
                if event.type == pygame.MOUSEMOTION and pygame.mouse.get_pressed() == (0, 0, 1):
                    grid_cells[grid_index].set_dead()  # marks cells as dead if clicked on them

        pygame.display.update()
        root.update()
        if game_started:
            clock.tick(10)
        else:
            clock.tick(120)

if __name__ == "__main__":
    main()