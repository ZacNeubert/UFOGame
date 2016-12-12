![](https://github.com/ZacNeubert/UFOGame/blob/master/stats/logo.png?raw=true)
##Abstract:
The purpose of this project is to test different methods of machine learning and different features to play a real-time obstacle avoidance game. Many methods have been tried, including neural networks and several different types of classifiers. 

##Problem Description:
UFO Game is a game written in python where the player uses the arrow keys to control a ufo in a window. The objective is to avoid collisions with asteroids for as long as possible. Both the ufo and the player bounce off the edges of the window, conserving all of their momentum. Asteroids also bounce off of each other. Because the player is in control of the acceleration, rather than the velocity, the game has a slippery feel to it. The game awards a point for every frame that the player survives.

![Game](https://github.com/ZacNeubert/UFOGame/blob/master/stats/game.png?raw=true)

##Method:
Because I had direct access to the game’s source code, I decided to build the learning directly into the game.
I refactored the keystroke reading to allow keystrokes from other sources. Then, I created a “random” player for the game, that inputs up, down, left, right, or nothing randomly every frame.
I tested the average score of this player to compare against the various machine learning techniques. 
I set about altering the game to make it easier to measure. I changed the number of asteroids to 1, in order to get results faster. I also changed the game to skip rendering unimportant frames so that it could test itself quicker. I also added an average score display and eliminated the need to press keys to start or restart a round. 
Then, I built a template for a machine learning game player. This player would take data produced by the random game player, or a human game player, and produce a keystroke every frame. This template could be filled in by any classifier.
I then implemented this for many different classifiers. I used several classifiers from Sci-Kit Learn, as well as the Keras wrapper for tensorflow neural networks to test this.

##Challenges:
This game had several things that made it challenging for machine learning to learn well. 

Firstly, the game is slow. To obtain the truth data, the game has to be run for a long time. Much of my time was spent changing the game to gather truth data faster. There are also basically an infinite number of states the game can be in, leading options like a decision tree to be very ineffective with certain feature sets. Thirdly, the original control scheme was based on acceleration, which creates a whole new dimension of states that the UFO can be in at any given time. Finally, the asteroid's collisions have some RNG in them, causing them to change speed sometimes, which can drastically throw off the machine learning if it expects a specific speed.

Iteration was very slow, because of the massive amounts of truth data needed to create a competent AI.

Finally, there are many more okay decisions than bad ones. Generally, it is a series of bad decisions that leads to death in this game. Therefore, it is difficult to classify which decisions are bad ones, especially with more asteroids.

##Feature Extraction:
Because I had access to the source code for this game, I was able to extract the features directly from the objects. I had a few different sets of features to try. The first one was the x and y locations and velocities for both the ufo and the asteroid. 

*Initial Features:* 
UFO X Position, UFO Y Position, UFO X Velocity, UFO Y Velocity, Asteroid X Position, Asteroid Y Position, Asteroid X Velocity, Asteroid Y Velocity

The second set of features I tried was an attempt to make simpler, easier to understand features. The first set of features had too much variation for something like a decision tree to understand. Good results took gigabytes of data to achieve. I separated the play area into a grid. Where before, I gave the exact location of each object, now I would give the learning algorithm a grid, with the UFO’s location marked with a 1 and an asteroid’s location with a 2. A zone containing both will be marked with a 3. This was attempted both containing the velocities of the ufo/asteroid and without them.

*New Features:*

![New Features](https://github.com/ZacNeubert/UFOGame/blob/master/stats/features2.png?raw=true)

To teach the classifiers to win, rather than to imitate a random number generator, all frames within 150 frames of dying were forgotten. Because there are far more good moves than bad in a 1-asteroid scenario, it should be most important to learn the moves that do not kill the player.

##Results:
The Random Forest classifier and the Kernelizer from sci-kit learn did fairly well, but the Random Forest did better, so I focused on training that.

It is important to note that the game gets exponentially harder to learn the more asteroids that are added. Each added asteroid adds another dimension of possible situations, requiring exponentially more truth data. Here are the results of the trained classifier and random player with various asteroid counts.

![Results By Asteroid Count](https://github.com/ZacNeubert/UFOGame/blob/master/stats/asteroidcount.png?raw=true)

Human input was, in general, far better than machine input. This is likely because I had already learned the game, and was able to input the best keystrokes rather than just the ones that will survive.
![Human Training vs RNG](https://github.com/ZacNeubert/UFOGame/blob/master/stats/humaninputvsrng.png?raw=true)
![Random Training Vs RNG](https://github.com/ZacNeubert/UFOGame/blob/master/stats/randominputvsrng.png?raw=true)

##Conclusion:

**Why the Random Forest did well:** The Random Forest is a very effective tool for classifying on specific discrete data points. For example, a boolean piece of data is easier for it to use than a number from 0-100. When I changed the features to a zone grid instead of the actual numbers, the Random Forest's performance skyrocketed. With a game like this with fairly simple rules, it is okay to generalize the information given to the classifier.

**Why the First Feature Set Failed:** The first feature set was too complex for it to be easily understood. Although for a human, the numbers were easy to follow, there were actually many things that needed to be 'inferred' for it to work well. One example might be the dimensions of the arena. They were not included, and if they were included, would only be constants for the classifiers to throw away as unimportant. There were also so many possible values for each number (floating points!) that a tree-style classifier could not learn without huge amounts of redundant data.

**Why the UFO still Eventually Dies:** The truth data is generated by a random number generator making moves in a simulation. Because of this, the most common situations in the simulation will be learned many times over. Situations like the asteroid being at the center of the screen (the spawn location) will be learned every single time the random player dies. However, situations that are uncommon will easily lead to death because they have not been learned thousands of times. 

**The Next Step:** The next step of this project I think would be to adjust the data gathering for larger amounts of asteroids. With more asteroids, there are exponentially more situations. However, I think that with smaller zones and a better way of gathering survival truth, it could be accomplished. Because it is a long series of moves that leads to death, I think a stricter limit for keeping survival truth would help it to learn quicker. For example, I could tell the program to throw out all games that die before 1000 frames have passed. If it does this, then the classifier would learn better games, and learn many fewer negative moves.

##Miscellaneous Stats:

*Laptop Memory Failures:* 2

*Total Truth Files Generated:* 62

*Total Truth Data Generated:* 13.4 GB
