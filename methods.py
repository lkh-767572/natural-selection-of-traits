import random
import pygame as pg
from creature import Creature

def draw_creatures(list):
    i= 0
    for i in range(len(list)):
        list[i].draw()

def replication(creatures, display, border_rect, start_speed,\
    start_sense, start_energy, speed_mutation, sense_mutation, nutrition):
    for creature in creatures:
        if creature.food_count >= 2:
            new_creature = Creature(display, border_rect, start_speed, start_sense,\
             start_energy, speed_mutation, sense_mutation, nutrition)
            new_creature.speed = creature.speed
            new_creature.radius = creature.radius
            new_creature.sense = creature.sense
            new_creature.mutate()
            creatures.append(new_creature)
    return creatures

def check_survival(creatures, display, border_rect, start_speed, start_sense,\
    start_energy, speed_mutation, sense_mutation, nutrition):
    creatures = list(filter(lambda creature: creature.food_count > 0, creatures))
    creatures = replication(creatures, display, border_rect, start_speed,\
                start_sense, start_energy, speed_mutation, sense_mutation, \
                nutrition)
    for creature in creatures:
        creature.food_count = 0
        creature.energy_used = 0
        creature.spawn()
    return creatures

def spawn_food(display, num, WIDTH, HEIGHT):
    color = (0, 255, 0)
    rectangles = []
    for i in range(num):
        x = random.randint(100, 900)
        y = random.randint(100, 900)
        rect = pg.draw.rect(display, color, (x, y, WIDTH, HEIGHT))
        collides = False
        for r in rectangles:
            if rect.colliderect(r):
                collides = True
        if not collides:
            rectangles.append(rect)
    return rectangles

def avg_of_list(list):
        avg_list  = sum(list) / len(list)
        avg = float("%.2f" % avg_list)
        return avg