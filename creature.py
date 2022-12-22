import random
import pygame as pg
from math import sqrt


class Creature:
    def __init__(self, display, border_rect, start_speed, start_sense,
        start_energy, speed_mutation, sense_mutation, nutrition):
        self.display = display
        self.border_rect = border_rect

        self.color = (0, 0, 255)  # Blue

        self.mutation_chance = 10
        self.speed = start_speed
        self.sense = start_sense
        self.food_count = 0
        self.radius = 10
        self.energy_cost = self.speed ** 2 + self.sense / 25
        self.energy_used = 0
        self.energy = start_energy
        self.speed_mutation = speed_mutation
        self.sense_mutation = sense_mutation
        self.nutrition = nutrition

        self.border_x, self.border_y, self.border_w, self.border_h = self.border_rect

    def spawn(self):
        # Choose a random position on the border for the creature
        self.side = random.choice(["top", "bottom", "left", "right"])

        # Choose a random side of the border
        if self.side == "top":
            self.x = random.randint(self.border_x, self.border_x + self.border_w)
            self.y = self.border_y - self.radius
        elif self.side == "bottom":
            self.x = random.randint(self.border_x, self.border_x + self.border_w)
            self.y = self.border_y + self.border_h + self.radius
        elif self.side == "left":
            self.x = self.border_x - self.radius
            self.y = random.randint(self.border_y, self.border_y + self.border_h)
        elif self.side == "right":
            self.x = self.border_x + self.border_w + self.radius
            self.y = random.randint(self.border_y, self.border_y + self.border_h)
            
        self.x_spawn = self.x
        self.y_spawn = self.y
            
    def reset(self):
        self.x = self.x_spawn
        self.y = self.y_spawn

    def draw(self):
        self.circle = pg.draw.circle(self.display, self.color,\
                      (self.x, self.y), self.radius)

    def move(self, food_pallets, WIDTH, HEIGHT):
        # The creatures move to the nearest food item if it is in reach of 
        # their sensor, they have enough energy and they have not eaten more
        # than three food items which ensures that there is no competiton
        # if the food is enough. Creatures will move randomly if 
        # no food item is in sense reach.
        
        # Find the nearest food item and move towards it
        nearest_food = None
        nearest_distance = float("inf")
        for food in food_pallets:
            food_x, food_y = food.center
            distance = sqrt((food_x - self.x) ** 2 + (food_y - self.y) ** 2)
            if distance < nearest_distance:
                nearest_food = food
                nearest_distance = distance

        # Move towards the nearest food
        if self.sense >= nearest_distance and self.energy_used < self.energy:
            food_x, food_y = nearest_food.center
            if self.x < food_x:
                self.x += self.speed
            elif self.x > food_x:
                self.x -= self.speed
            if self.y < food_y:
                self.y += self.speed
            elif self.y > food_y:
                self.y -= self.speed

        # Move random if no food in sight
        else:
            if self.energy_used < self.energy:
                x_ran = random.choice([-self.speed, self.speed])
                y_ran = random.choice([-self.speed, self.speed])
                # Check if moving the creature will keep it inside the border
                self.x += x_ran
                self.y += y_ran

                if self.x + x_ran >= 0 and self.x + x_ran < WIDTH:
                        self.x += x_ran
                if self.y + y_ran >= 0 and self.y + y_ran < HEIGHT:
                    self.y += y_ran

    def check_collision(self, food_pallets):
        # Checks for collision with food, if it happens food count is moved up
        # and the creature gains energy
        indices_to_remove = []
        for i in range(len(food_pallets)):
            if self.circle.colliderect(food_pallets[i]):
                indices_to_remove.append(i)
                self.food_count += 1
                self.energy_used -= self.nutrition

        # Remove the colliding elements from the food_pallets list
        for i in indices_to_remove[::-1]:
            food_pallets.pop(i)
        return food_pallets

    def consume_energy(self):
        self.energy_used += self.energy_cost
            
    def mutate(self):
        # For each mutation there is a chance of 10% each Generation. Native 
        # Selection happens through that creatures die when the traits give 
        # them a disadvantage, replicate if it gives them an advantage and 
        # survive if neither.

        self.chance_speed = random.choice(range(1, 100))
        if self.chance_speed <= self.mutation_chance:
            speed_change = random.choice([-self.speed_mutation, \
            self.speed_mutation])
            if speed_change == -self.speed_mutation:
                self.speed += speed_change
            else:
                self.speed += speed_change
        self.chance_sense = random.choice(range(1, 100))

        if self.chance_sense <= self.mutation_chance:
            sense_change = random.choice([-self.sense_mutation, \
            self.sense_mutation])
            if sense_change == -self.sense_mutation:
                self.sense += sense_change
            else:
                self.sense += sense_change