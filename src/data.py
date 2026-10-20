# src/data.py

STUDENTS = list("ABCDEFGHIJKL")

# 排偏好：row_pref[学生][排] ，排从 1 到 4
ROW_PREF = {
    "A": {1: 5, 2: 4, 3: 2, 4: 1},
    "B": {1: 5, 2: 4, 3: 3, 4: 1},
    "C": {1: 5, 2: 3, 3: 2, 4: 1},
    "D": {1: 3, 2: 5, 3: 4, 4: 2},
    "E": {1: 3, 2: 5, 3: 4, 4: 2},
    "F": {1: 2, 2: 4, 3: 5, 4: 3},
    "G": {1: 2, 2: 4, 3: 5, 4: 3},
    "H": {1: 4, 2: 3, 3: 2, 4: 5},
    "I": {1: 3, 2: 4, 3: 3, 4: 4},
    "J": {1: 2, 2: 5, 3: 5, 4: 2},
    "K": {1: 2, 2: 5, 3: 5, 4: 2},
    "L": {1: 1, 2: 2, 3: 5, 4: 5},
}

# 列偏好：col_pref[学生][列] ，列从 1 到 5
COL_PREF = {
    "A": {1: 4, 2: 3, 3: 2, 4: 3, 5: 4},
    "B": {1: 4, 2: 3, 3: 2, 4: 3, 5: 4},
    "C": {1: 3, 2: 4, 3: 5, 4: 4, 5: 3},
    "D": {1: 5, 2: 2, 3: 3, 4: 2, 5: 5},
    "E": {1: 5, 2: 2, 3: 3, 4: 2, 5: 5},
    "F": {1: 2, 2: 4, 3: 5, 4: 4, 5: 2},
    "G": {1: 2, 2: 4, 3: 5, 4: 4, 5: 2},
    "H": {1: 5, 2: 3, 3: 2, 4: 3, 5: 5},
    "I": {1: 2, 2: 5, 3: 3, 4: 5, 5: 2},
    "J": {1: 4, 2: 2, 3: 4, 4: 2, 5: 4},
    "K": {1: 4, 2: 2, 3: 4, 4: 2, 5: 4},
    "L": {1: 3, 2: 4, 3: 3, 4: 4, 5: 3},
}

NUM_ROWS = 4
NUM_COLS = 5
SEATS = list(range(1, 21))  # 座位号 1..20


def seat_to_row_col(s):
    """座位号 -> (排, 列)，排/列都从 1 开始"""
    r = (s - 1) // NUM_COLS + 1
    c = (s - 1) % NUM_COLS + 1
    return r, c


def seats_in_row(r):
    return [s for s in SEATS if seat_to_row_col(s)[0] == r]


def seats_in_col(c):
    return [s for s in SEATS if seat_to_row_col(s)[1] == c]


def left_right_neighbors(s):
    """左右相邻座位（同一排、列号差 1）"""
    r, c = seat_to_row_col(s)
    res = []
    if c > 1:
        res.append(s - 1)
    if c < NUM_COLS:
        res.append(s + 1)
    return res


def front_back_neighbors(s):
    """前后相邻座位（同一列、排号差 1）"""
    r, c = seat_to_row_col(s)
    res = []
    if r > 1:
        res.append(s - NUM_COLS)
    if r < NUM_ROWS:
        res.append(s + NUM_COLS)
    return res


def all_adjacent_pairs():
    """所有相邻座位对（左右或前后），返回无重复的 (s, t) 且 s < t"""
    pairs = set()
    for s in SEATS:
        for t in left_right_neighbors(s) + front_back_neighbors(s):
            if s < t:
                pairs.add((s, t))
    return sorted(pairs)


def satisfaction(i, s):
    """学生 i 坐座位 s 的满意度 = 排偏好 + 列偏好"""
    r, c = seat_to_row_col(s)
    return ROW_PREF[i][r] + COL_PREF[i][c]