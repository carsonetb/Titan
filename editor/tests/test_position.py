from node_types.position import Position
import tests.test_framework as test_framework
import pygame

def run_tests(framework: test_framework.TestFramework):

    # DEFAULTS

    test_position = Position()
    framework.check_eq(test_position.node_type, "Position")
    framework.check_eq(test_position.position, pygame.Vector2(0, 0))
    framework.check_eq(test_position.scale, pygame.Vector2(1, 1))
    framework.check_eq(test_position.children, [])
    framework.check_eq(test_position.parent, "Root")
    framework.check_eq(test_position.mouse_dragging, False)
    framework.check_eq(test_position.selected, False)
    framework.check_eq(test_position.just_moved, False)
    framework.check_eq(test_position.eligable_for_dragging, False)

    # TEST ADD CHILD

    parent = Position()
    child = Position()

    parent.add_child(child)
    framework.check_eq(parent.children[0], child)
    framework.check_eq(child.parent, parent)

    # TEST GENERATE ENGINE INTERACTABLE

    test_position = Position()
    interactable = test_position.generate_engine_interactable()
    framework.check_eq(interactable.children, test_position.children)
    framework.check_eq(interactable.parent, test_position.parent)
    framework.check_eq(interactable.position, test_position.position)
    framework.check_eq(interactable.global_position, test_position.global_position)
    framework.check_eq(interactable.rotation, test_position.rotation)
    framework.check_eq(interactable.rotation_degrees, test_position.rotation_degrees)

    # TEST UPDATE ENGINE INTERACTABLE

    interactable.position = pygame.Vector2(5, 5)
    interactable.rotation = 128
    interactable.scale = pygame.Vector2(0.5, 0.5)
    test_position.update_variables_from_interactable(interactable)
    framework.check_eq(test_position.position, pygame.Vector2(5, 5))
    framework.check_eq(test_position.rotation, 128)
    framework.check_eq(test_position.scale, pygame.Vector2(0.5, 0.5))

    # TEST GLOBAL POSITION

    parent = Position()
    child = Position()
    parent.add_child(child)

    parent.editor_update()
    child.editor_update()
    framework.check_eq(parent.position, pygame.Vector2(0, 0))
    framework.check_eq(parent.global_position, pygame.Vector2(0, 0))
    framework.check_eq(child.position, pygame.Vector2(0, 0))
    framework.check_eq(child.global_position, pygame.Vector2(0, 0))

    child.add_position(pygame.Vector2(5, 5))
    parent.editor_update()
    child.editor_update()
    framework.check_eq(child.position, pygame.Vector2(5, 5))
    framework.check_eq(child.global_position, pygame.Vector2(5, 5))

    parent.add_position(pygame.Vector2(7, 7))
    parent.editor_update()
    child.editor_update()
    framework.check_eq(parent.position, pygame.Vector2(7, 7))
    framework.check_eq(parent.global_position, pygame.Vector2(7, 7))
    framework.check_eq(child.position, pygame.Vector2(5, 5))
    framework.check_eq(child.global_position, pygame.Vector2(12, 12))


