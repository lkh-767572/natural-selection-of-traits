import pygame as pg
from time import time
from analyze import analyze
from methods import draw_creatures, check_survival, spawn_food, avg_of_list
from creature import Creature


# Simulation Settings cental
start_speed = 1.00 
start_sense = 100
start_energy = 1000
gen_len = 8
FOOD = 200
CREATURES = 100
speed_mutation = 0.05
sense_mutation = 5
nutrition = 100 # How much energy creatures gain from eating food


def main():

    pg.init()

    # Settings
    FPS = 30
    HEIGHT = 1000
    WIDTH = 1000
    GENERATIONS = 0
    generations_list = []
    num_list = []
    speed_list = []
    sense_list = []
    avg_speed_list = []
    avg_sense_list = []
    running = True
    speed_avg = None
    speed_txt = start_speed
    sense_avg = None
    sense_txt = start_sense

    display = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption("natural selection in python")
    clock = pg.time.Clock()

    # Border
    border = pg.draw.rect(display, (0, 0, 0), (50, 50, 900, 900), 10)

    # Food
    food_pallets = spawn_food(display, FOOD, 10, 10)

    # Creatures
    creatures = []
    for i in range(CREATURES):
        creature_ind = Creature(display, border, start_speed, start_sense,\
             start_energy, speed_mutation, sense_mutation, nutrition)
        creatures.append(creature_ind)
    
    for creature in creatures:
        creature.spawn()

    generations_list.append(GENERATIONS)
    num_list.append(len(creatures))
    avg_speed_list.append(start_speed)
    avg_sense_list.append(start_sense)

    # Text
    font = pg.font.Font(None, 36)

    t0 = time()


    while running:
        t1 = time()
        clock.tick(FPS)
        display.fill((255, 255, 255))

        # track time
        dt = t1 - t0

        if dt >= gen_len:
            food_pallets = spawn_food(display, FOOD, 10, 10)
            # logic for death, survival, rep, mutation
            creatures = check_survival(creatures, display, border,\
                start_speed, start_sense, start_energy, speed_mutation,\
                sense_mutation, nutrition)

            for creature in creatures:
                speed_list.append(creature.speed)
                sense_list.append(int(round(creature.sense)))
                creature.reset()

            speed_avg = avg_of_list(speed_list)
            avg_speed_list.append(speed_avg)
            sense_avg = avg_of_list(sense_list)
            avg_sense_list.append(sense_avg)
            generations_list.append(GENERATIONS)
            num_list.append(len(creatures))
            if creatures:
                GENERATIONS += 1
            t0 = t1

        if speed_avg:
            speed_txt = speed_avg    
        if sense_avg:
            sense_txt = sense_avg

        # Text
        text_surface = font.render(f"Generation: {GENERATIONS}; Number: {len(creatures)};   Food: {len(food_pallets)};    Speed: {speed_txt};   Sense: {round(sense_txt)}", True, (0, 0, 0))
        display.blit(text_surface, (43, 950))

        # draw creatures
        draw_creatures(creatures)

        # draw food pallets
        for pallet in food_pallets:
            pg.draw.rect(display, (0, 255, 0), pallet)

        # Border
        border = pg.draw.rect(display, (0, 0, 0), (50, 50, 900, 900), 10)

        # remove food if collision
        for i in range(len(creatures)):
            food_pallets = creatures[i].check_collision(food_pallets)
        
        # move creatures and calculate energy
        for i in range(len(creatures)):
            creatures[i].move(food_pallets, WIDTH, HEIGHT)
            creatures[i].consume_energy()  
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        pg.display.flip()

        if not creatures:
            running = False

    analyze("simulation_data.txt", generations_list, num_list, avg_speed_list,\
        avg_sense_list)
  
  
if __name__ == '__main__':
        main()
    