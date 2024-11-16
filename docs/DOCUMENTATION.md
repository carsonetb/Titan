# Titan Game Engine Documentation

A comprehensive documentation of nodes and scripting in the
Titan game engine. Some of this might look wierd if you look
at it in the Github markdown viewer. Look at the raw instead.

## Scripting

Engine state is passed into update and ready functions via
the EngineInteractable class (and its subclasses). It 
exists to provide a layer of abstraction between the actual
engine and the user code. Some values in the node we don't 
want the user to set. This documentation essentially has all 
of the EngineInteractable methods and variables. This class
includes:

- Editable data about the node
- Miscelaneous functions (like keypresses)
- EngineInteractables for children 
- A single EngineInteractable for the parent

## Nodes

Nodes are in-editor objects which are the base objects for 
the game.

### BaseEngineInteractable  

See Scripting
You will never see a node of this type, it will always be 
Position or something that inherits Position.

#### Variables

- children
    Type: array[BaseEngineInteractable]
    Description: An array of all the nodes children.
- parent
    Type: BaseEngineInteractable|str
    Description: The parent of the node. Will be "root" if
                 the parent is the root node.

#### Methods

- is_key_pressed -> bool
    Parameters: 
        key_index (int): Index of the key that we want to check.
                   There are some globals in the 
                   EngineInteractable class to help with this.
    Description: Checks if a certain key is pressed.
- is_key_just_pressed -> bool
    Parameters:
        key_index (int): See is_key_pressed -> key_index.
    Description: Checks if a key was just pressed (the player
                 just put their finger on the key)

### Position

Inherits: BaseEngineInteractable

Base node for storing position in the engine. All nodes
inherit from Position.

#### Variables

- position: 
    Type: pygame.Vector2
    Description: The position of the node RELATIVE to its parent.
- global_position: 
    Type: pygame.Vector2
    Description: The GLOBAL position of the node relative to root.
- rotation:
    Type: float
    Description: The rotation in radians of the node relative to its parent.
- rotation_degrees: 
    Type: float
    Description: The rotation in degrees of the node relative to its parent.
- scale:
    Type: pygame.Vector2
    Description: A scale vector for the node relative to its parent.  

### Sprite

Inherits: Position

Base node for displaying an image/sprite. Can be scaled
and rotated.

#### Variables

- sprite_path:
    Type: str
    Description: Path to the sprite. This can be set, and will work from 
                 any path.
- dimensions:
    Type: pygame.Vector2
    Description: Width and height of the image in pixels.

### Shape

Inherits: Position

Displays a shape like a rectangle, circle, line, or 
polygon. 

#### Variables

- shape_type:
    Type: int
    Description: Shape type, enumerations are provided.
- rect_dimensions:
    Type: pygame.Vector2
    Description: Dimensions of the rect if the shape type is a rect.
- circle_radius:
    Type: float
    Description: Radius if the shape type is a circle.
- points:
    Type: array[pygame.Vector2]
    Description: An array of points if the type is a line or polygon.
- color:
    Type: tuple[int, int, int, int]
    Description: The color of the shape, regardless of type.

### PhysicsShape

Inherits: Shape <- Position

Base class for all physics nodes.

### RigidBody

Inherits: Shape <- PhysicsShape <- Position

Physics shape which can fall and collide with other 
RigidBodies and StaticBodies.

#### Variables

- body:
    Type: pymunk.Body
    Description: I literally just put the pymunk.Body in there, go
                 look up the documentation for it for yourself.

### StaticBody

Inherits: Shape <- PhysicsShape <- Position

Physics shape with which other bodies can collide with
but it remains unmoving.
