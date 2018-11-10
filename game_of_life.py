import tkinter as tk
import pygame
import os
import Cell

game_started = False
mode = "default"
game_of_life_width = 1000
game_of_life_height = 750
grid_cells = []

def create_grid(screen, width, height, margin):
    for i in range(int(game_of_life_height / (height+margin))):
        for j in range(int(game_of_life_width / (width+margin))):
            grid_cells.append(Cell.Cell(margin + j*(width+margin), margin + i*(height+margin), width, height, (0, 0, 0)))

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
    for cell in grid_cells:
        cell.set_dead()

def set_default_mode():
    global mode
    mode = "default"

def set_bacteria_mode():
    global mode
    mode = "bacteria"

def main():
    root = tk.Tk()
    root.title('Game of Life')
    pygameframe = tk.Frame(root, width = game_of_life_width, height = game_of_life_height)
    pygameframe.grid(columnspan=(game_of_life_width), rowspan=game_of_life_height)  # Adds grid
    pygameframe.pack(side = tk.BOTTOM)
    uiframe =  tk.Frame(root)
    uiframe.pack()
    os.environ['SDL_WINDOWID'] = str(pygameframe.winfo_id())
    os.environ['SDL_VIDEODRIVER'] = 'windib'
    screen = pygame.display.set_mode((game_of_life_width, game_of_life_height))
    screen.fill(pygame.Color(10, 10, 10)) # black background colour

    start_button = tk.Button(uiframe, text = "Start", command=start_game_of_life)
    start_button.pack(side = tk.LEFT)
    pause_button = tk.Button(uiframe, text = "Pause", command=pause_game_of_life)
    pause_button.pack(side=tk.LEFT)
    reset_button = tk.Button(uiframe, text="Reset", command=reset_game_of_life)
    reset_button.pack(side=tk.LEFT)
    menubar = tk.Menu(root)
    mode_menu = tk.Menu(menubar, tearoff=0) # For choosing the program mode
    mode_menu.add_command(label="Default Game of Life", command=set_default_mode)
    mode_menu.add_command(label="Bacteria (cells get evaluated in order)", command=set_bacteria_mode)
    menubar.add_cascade(label="Mode", menu=mode_menu)
    root.config(menu=menubar)

    cell_width = 6
    cell_height = 6
    cell_margin = 1

    pygame.display.init()
    create_grid(screen, cell_width, cell_height, cell_margin)
    pygame.display.update()

    k = 0
    while True:
        if game_started:
            if k % 10 == 0:
                if mode == "default":
                    update_game_of_life_default(int(game_of_life_width / (cell_width+cell_margin)), int(game_of_life_height / (cell_height+cell_margin)))
                elif mode == "bacteria":
                    update_game_of_life_bacteria(int(game_of_life_width / (cell_width+cell_margin)), int(game_of_life_height / (cell_height+cell_margin)))
        else:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN or (event.type == pygame.MOUSEMOTION and pygame.mouse.get_pressed() == (1,0,0)):
                    grid_index = int(pygame.mouse.get_pos()[0] /(cell_width+cell_margin)) + int(pygame.mouse.get_pos()[1]/(cell_height+cell_margin)) * int(game_of_life_width / (cell_width+cell_margin))
                    grid_cells[grid_index].set_alive()  # marks cells as alive if clicked on them
                if event.type == pygame.MOUSEBUTTONDOWN or (event.type == pygame.MOUSEMOTION and pygame.mouse.get_pressed() == (0,0,1)):
                    grid_index = int(pygame.mouse.get_pos()[0] /(cell_width+cell_margin)) + int(pygame.mouse.get_pos()[1]/(cell_height+cell_margin)) * int(game_of_life_width / (cell_width+cell_margin))
                    grid_cells[grid_index].set_dead()  # marks cells as alive if clicked on them
        if k % 10 == 0:
            for cell in grid_cells:
                pygame.draw.rect(screen, cell.color, (cell.x, cell.y, cell.width, cell.height))

        pygame.display.update()
        root.update()
        k += 1

if __name__ == "__main__":
    main()