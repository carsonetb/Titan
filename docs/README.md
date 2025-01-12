# Titan Engine

## Overview

The Titan Game Engine is a 2D game engine aimed at 
creating linear, level-based games. It is created
by Carson Bates.

I estimate this project is estimated to be 6% finished, so half that and you have an optimistic estimate!

## Speed

In general python is pretty slow but in a game you can
get 5000+ FPS. How? The project wraps two C libraries 
which handle rendering and
physics (Raylib and Chipmunk). Only the high level logic
is done in Python, making it pretty fast.

## Links

- Github: https://github.com/EpimetheusGames/Titan
- Email: epimetheusgamesogpc@gmail.com

## Nodes

- Position: Base node for all other nodes, stores position, scale, and rotation.
- Sprite: Displays an image from a file.
- Shape: Node for displaying shapes like polygons, lines, circles, and rectangles.
- PhysicsShape: Inherits Shape and helps handle velocity of physics objects.
- RigidBody: Inherits PhysicsShape and has rigid collisions.
- StaticBody: Inherits PhysicsShape and objects can collide with it. The position stays the same.

## Scripting

The scripting is done in pure Python. This comes
with the perk of being able to use any Python module
(whether it comes with Python or has been 
installed with PyPi or another third party Python
package installation tool) in a script. A single
script can be attached to a node (or multiple) 
nodes, as long as the node inherits the script's
specified node type. 
