NODE_TYPE = "RigidBody"

def update(node):
    if node.is_key_pressed(node.KEY_A):
        node.velocity.x = -250
    if node.is_key_pressed(node.KEY_D):
        node.velocity.x = 250
    if node.is_key_just_pressed(node.KEY_W):
        node.velocity.y = -700