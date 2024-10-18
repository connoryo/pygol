from pygol.board import Board


def check_next_state(init_state, expected_next_state):
    board = Board(1, 1)
    board.set_state(init_state)
    board.iterate_state()
    board_state = board.get_state()
    print(board_state)
    print(expected_next_state)
    assert board_state == expected_next_state


def test_board_dead():
    init_state = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    expected_next_state = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    check_next_state(init_state, expected_next_state)


def test_board_alive():
    init_state = [[0, 0, 1], [0, 1, 1], [0, 0, 0]]
    expected_next_state = [[0, 1, 1], [0, 1, 1], [0, 0, 0]]
    check_next_state(init_state, expected_next_state)


def test_edge_underpopulation():
    # A live cell at the edge with fewer than 2 neighbors dies due to underpopulation
    init_state = [[1, 0, 0], [0, 0, 0], [0, 0, 0]]
    expected_next_state = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    check_next_state(init_state, expected_next_state)


def test_edge_survival():
    # A live cell at the edge with exactly 2 neighbors survives
    init_state = [[1, 1, 0], [0, 1, 0], [0, 0, 0]]
    expected_next_state = [[1, 1, 0], [1, 1, 0], [0, 0, 0]]
    check_next_state(init_state, expected_next_state)


def test_corner_reproduction():
    # A dead cell at the corner with exactly 3 neighbors comes to life due to reproduction
    init_state = [[0, 1, 0], [1, 0, 1], [0, 0, 0]]
    expected_next_state = [[0, 1, 0], [0, 1, 0], [0, 0, 0]]
    check_next_state(init_state, expected_next_state)


def test_corner_overpopulation():
    # A live cell at the corner with more than 3 neighbors dies from overpopulation
    init_state = [[1, 1, 1], [1, 1, 0], [0, 0, 0]]
    expected_next_state = [[1, 0, 1], [1, 0, 1], [0, 0, 0]]
    check_next_state(init_state, expected_next_state)


def test_dead_board():
    # Test with all dead cells, no cells should change state
    init_state = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    expected_next_state = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    check_next_state(init_state, expected_next_state)


def test_full_live_board():
    # Test with all live cells, all cells with more than 3 neighbors should die
    init_state = [[1, 1, 1], [1, 1, 1], [1, 1, 1]]
    expected_next_state = [[1, 0, 1], [0, 0, 0], [1, 0, 1]]
    check_next_state(init_state, expected_next_state)
