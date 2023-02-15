import numpy as np
from coord import *


class PathFindingNode:
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


class AStartAlg:
    def __init__(self, weight_map: np.array):
        self.weight_map = weight_map

    def compute_path(self, start: Coordinate, end: Coordinate) -> Path:
        generated_path = Path()
        start_cell = ((start.x + TABLE_WIDTH / 2) // 100, (start.y + TABLE_HEIGHT / 2) // 100)
        end_cell = ((end.x + TABLE_WIDTH / 2) // 100, (end.y + TABLE_HEIGHT / 2) // 100)

        board_width, board_height = np.shape(self.weight_map)
        assert 0 <= start_cell[0] < board_width and 0 <= end_cell[0] < board_width
        assert 0 <= start_cell[1] < board_height and 0 <= end_cell[1] < board_height

        """Returns a list of tuples as a path from the given start to the given end in the given maze"""

        # Create start and end node
        start_node = PathFindingNode(None, start)
        start_node.g = start_node.h = start_node.f = 0
        end_node = PathFindingNode(None, end)
        end_node.g = end_node.h = end_node.f = 0

        # Initialize both open and closed list
        open_list = []
        closed_list = []

        # Add the start node
        open_list.append(start_node)

        # Loop until you find the end
        while len(open_list) > 0:

            # Get the current node
            current_node = open_list[0]
            current_index = 0
            for index, item in enumerate(open_list):
                if item.f < current_node.f:
                    current_node = item
                    current_index = index

            # Pop current off open list, add to closed list
            open_list.pop(current_index)
            closed_list.append(current_node)

            # Found the goal
            if current_node == end_node:
                travel_path = Path()
                current = current_node
                while current is not None:
                    travel_path.add_steps(current.position)
                    current = current.parent
                return travel_path[::-1]  # Return reversed path

            # Generate children
            children = []
            for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1),
                                 (1, 1)]:  # Adjacent squares

                # Get node position
                node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

                # Make sure within range
                width, height = np.shape(self.weight_map)
                if node_position[0] > height \
                        or node_position[0] < 0 \
                        or node_position[1] > width \
                        or node_position[1] < 0:
                    continue

                # Make sure walkable terrain
                if self.weight_map[node_position[0], node_position[1]] != 0:
                    continue

                # Create new node
                new_node = PathFindingNode(current_node, node_position)

                # Append
                children.append(new_node)

            # Loop through children
            for child in children:

                # Child is on the closed list
                for closed_child in closed_list:
                    if child == closed_child:
                        continue

                # Create the f, g, and h values
                child.g = current_node.g + 1
                child.h = ((child.position[0] - end_node.position[0]) ** 2) + (
                        (child.position[1] - end_node.position[1]) ** 2)
                child.f = child.g + child.h

                # Child is already in the open list
                for open_node in open_list:
                    if child == open_node and child.g > open_node.g:
                        continue

                # Add the child to the open list
                open_list.append(child)

        return generated_path
