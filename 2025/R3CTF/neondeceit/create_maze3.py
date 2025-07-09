# def create_maze():
#     rows = 21
#     cols = 51
#     grid = [['#' for _ in range(cols)] for _ in range(rows)]
    
#     # Fill grid cells
#     for i in range(1, rows - 1):
#         for j in range(1, cols - 1):
#             if i % 2 == 1 and j % 2 == 1:
#                 grid[i][j] = ' '

#     # Initialize walls between cells
#     walls = []
#     for i in range(1, rows - 1):
#         for j in range(1, cols - 1):
#             if i % 2 == 0 and j % 2 == 1:
#                 walls.append((i, j))
#             elif i % 2 == 1 and j % 2 == 0:
#                 walls.append((i, j))
    
#     # Shuffle walls
#     for k in range(len(walls)-1, 0, -1):
#         r = randint(0, k)
#         walls[k], walls[r] = walls[r], walls[k]
    
#     # Map each cell to unique ID
#     def cell_id(i, j):
#         return ((i // 2) * ((cols // 2))) + (j // 2)
    
#     num_cells = ((rows - 1) // 2) * ((cols - 1) // 2)
#     parent = [i for i in range(num_cells)]
    
#     def find(u):
#         while parent[u] != u:
#             parent[u] = parent[parent[u]]
#             u = parent[u]
#         return u

#     def union(u, v):
#         pu = find(u)
#         pv = find(v)
#         if pu != pv:
#             parent[pv] = pu
#             return True
#         return False
    
#     # Process walls
#     for i, j in walls:
#         if i % 2 == 0:
#             # Horizontal wall between (i-1,j) and (i+1,j)
#             u = cell_id(i - 1, j)
#             v = cell_id(i + 1, j)
#         else:
#             # Vertical wall between (i,j-1) and (i,j+1)
#             u = cell_id(i, j - 1)
#             v = cell_id(i, j + 1)
#         if union(u, v):
#             grid[i][j] = ' '

#     # Set start and end positions
#     grid[1][0] = 'S'     # (1,0)
#     grid[19][50] = 'E'   # (19,50)

#     # Convert grid to strings
#     return [''.join(row) for row in grid]

def create_maze():
    maze = """###################################################
S                         # #                 # # #
# ##### ### # # # ####### # # # ####### # ### # # #
#     # # # # # # #           # #     # #   #     #
# ### ### # # # ########### # # # # # ########### #
#   # #     # # # #   # # # # # # # #             #
# # # # # # # ### # # # # # ##### # # ### ##### # #
# # # # # # #       # # #   #   # # # #     #   # #
# # ### # # # # ##### # ### # ########### ####### #
# #   # # # # # #     #   # # # # # # # # # # # # #
######################### # # # # # # # # # # # # #
#                               #             # # #
####### ############# ##### # # # ### # ### ### # #
#             #         #   # # # #   #   #     # #
# # # # # ############# ###########################
# # # # # #                                       #
# ### # # # # ### # # # # # # # # # # ### ### ### #
#   # # # # #   # # # # # # # # # # #   #   # #   #
# # ##### # # # # ##### # # # # # ### # # # # # # #
# #     # # # # # #     # # # # #   # # # # # # # E
###################################################""".splitlines()
    return maze 

def solve_maze(maze, start_coords=None, end_coords=None):
    """
    Solve a maze using BFS.
    
    :param maze: 2D list representing the maze
    :param start_coords: (x, y) coordinates of start position, defaults to first empty cell
    :param end_coords: (x, y) coordinates of end position, defaults to last empty cell
    :return: String of UDLR directions to solve the maze
    """
    width = len(maze)
    height = len(maze[0])
    
    # Find start and end if not provided
    if start_coords is None:
        # Find first empty cell for start
        for x in range(width):
            for y in range(height):
                if maze[x][y] == ' ' or maze[x][y] == 'S':
                    start_coords = (x, y)
                    break
            if start_coords:
                break
    
    if end_coords is None:
        # Find last empty cell for end
        for x in range(width-1, -1, -1):
            for y in range(height-1, -1, -1):
                if maze[x][y] == ' ' or maze[x][y] == 'E':
                    end_coords = (x, y)
                    break
            if end_coords:
                break
    
    # BFS to find shortest path
    queue = [(start_coords, [])]  # (position, path)
    visited = {start_coords}
    
    # Directions: up, down, left, right
    directions = [
        (0, -1, 'U'),
        (0, 1, 'D'),
        (-1, 0, 'L'),
        (1, 0, 'R')
    ]
    
    while queue:
        (x, y), path = queue.pop(0)
        
        if (x, y) == end_coords:
            return ''.join(path)
        
        for dx, dy, direction in directions:
            nx, ny = x + dx, y + dy
            
            if (0 <= nx < width and 0 <= ny < height and 
                (maze[nx][ny] == ' ' or maze[nx][ny] == 'E') and 
                (nx, ny) not in visited):
                queue.append(((nx, ny), path + [direction]))
                visited.add((nx, ny))
    
    return "No path found"

def mark_path_in_maze(maze, start_coords, end_coords, path):
    """
    Mark the solution path in the maze.
    
    :param maze: 2D list representing the maze
    :param start_coords: (x, y) coordinates of start position
    :param end_coords: (x, y) coordinates of end position
    :param path: String of UDLR directions
    :return: Modified maze with path marked
    """
    # Create a deep copy of the maze
    marked_maze = [row[:] for row in maze]
    
    # Mark start and end
    x, y = start_coords
    marked_maze[x][y] = 'S'
    
    x, y = end_coords
    marked_maze[x][y] = 'E'
    
    # Follow the path and mark it
    x, y = start_coords
    for move in path:
        if move == 'U':
            y -= 1
        elif move == 'D':
            y += 1
        elif move == 'L':
            x -= 1
        elif move == 'R':
            x += 1
        
        # Only mark cells that aren't start or end
        if (x, y) != start_coords and (x, y) != end_coords:
            marked_maze[x][y] = '.'
    
    return marked_maze

# Example usage:
if __name__ == "__main__":
    maze = create_maze()
    for row in maze:
        print(''.join(row))
    
    path = solve_maze(maze)
    path = ''.join([
        {
            'D': 'R',
            'R': 'D',
            'L': 'U',
            'U': 'L'
        }[i] for i in path
    ])
    print("Path found:", path)

    bits = ""
    for i in path:
        if i == 'U':
            bits += '00'
        elif i == 'D':
            bits += '01'
        elif i == 'L':
            bits += '10'
        elif i == 'R':
            bits += '11'

    byts = b''
    for b in range(0, len(bits), 8):
        byts += bytes([int(bits[b:b+8], 2)])
    
    print(byts.hex())