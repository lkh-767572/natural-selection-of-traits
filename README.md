# natural-selection-of-traits
inspired by primer

# How does it work?
- Creatures are spawned randomly on the border. The simulation runs each generation for 8 seconds, then resets the creatures to the starting position. 
- In the simulation the creatures have a sense, a radius how far they can see. If food is in theís radius, they will go the nearest way to it. If no food is in sight they will move randomly.
- The creatures also have energy, which can be modified, and an energy cost per time, which equals e = speed ** 2 + sense / 25. If they have no energy left, they will stop moving. This way it is ensured, that a higher sense or speed has an penalty.
- If the creatures have not found any food, they die and get removed, if they found one piece of food, they manage to survive and of they found two or more pieces they survive and replicate
- The replicate is an exact clone of the creature and has a 10% chance that a mutation happens, in which case the speed (50%) or the sensor (50%) change by a given value. The cances are 50/50 for either an neagtive or positive change it the values.
- Natural selection happens because the creatures with random changes, that give them a benefit survive and reproduce, and those with changes that make them worse adapted die and wont pass off their genes
- At the end of the simulation a graph will show up displaying the number of creatures and the average speed and sense value each generation
