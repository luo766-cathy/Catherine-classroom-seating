# src/constraints.py

from pyscipopt import quicksum
from src.data import (
    STUDENTS, SEATS, NUM_ROWS, NUM_COLS,
    seat_to_row_col, seats_in_row, seats_in_col,
    left_right_neighbors, all_adjacent_pairs,
)


def add_basic_constraints(model, x):
    """约束 1、2：每人恰好一个座位；每个座位最多一人"""
    for i in STUDENTS:
        model.addCons(quicksum(x[i, s] for s in SEATS) == 1, name=f"one_seat_{i}")
    for s in SEATS:
        model.addCons(quicksum(x[i, s] for i in STUDENTS) <= 1, name=f"seat_cap_{s}")


def add_fixed_position_constraints(model, x):
    """约束 3-8：固定位置类"""
    # 3. A、B 必须前两排
    for i in ("A", "B"):
        for s in SEATS:
            r, _ = seat_to_row_col(s)
            if r >= 3:
                model.addCons(x[i, s] == 0, name=f"{i}_front_{s}")

    # 4. C 必须第一排
    for s in SEATS:
        r, _ = seat_to_row_col(s)
        if r != 1:
            model.addCons(x["C", s] == 0, name=f"C_row1_{s}")

    # 6. H 必须靠窗（第 1 或第 5 列）
    for s in SEATS:
        _, c = seat_to_row_col(s)
        if c not in (1, 5):
            model.addCons(x["H", s] == 0, name=f"H_window_{s}")

    # 7. I 必须靠过道（第 2 或第 4 列）
    for s in SEATS:
        _, c = seat_to_row_col(s)
        if c not in (2, 4):
            model.addCons(x["I", s] == 0, name=f"I_aisle_{s}")


def add_d_e_adjacent(model, x):
    """约束 5：D 和 E 必须左右相邻"""
    for s in SEATS:
        neighbors = left_right_neighbors(s)
        # 如果 D 坐 s，则 E 必须坐在 s 的左右邻座之一
        model.addCons(
            x["D", s] <= quicksum(x["E", t] for t in neighbors),
            name=f"DE_D_at_{s}",
        )
        # 对称：如果 E 坐 s，则 D 必须坐在 s 的左右邻座之一
        model.addCons(
            x["E", s] <= quicksum(x["D", t] for t in neighbors),
            name=f"DE_E_at_{s}",
        )


def add_f_g_not_adjacent(model, x):
    """约束 6：F 和 G 不能左右相邻，也不能前后相邻"""
    for s, t in all_adjacent_pairs():
        model.addCons(x["F", s] + x["G", t] <= 1, name=f"FG_{s}_{t}_a")
        model.addCons(x["F", t] + x["G", s] <= 1, name=f"FG_{s}_{t}_b")


def add_j_k_same_row_not_adjacent(model, x):
    """约束 9：J 和 K 同一排，但两人不能相邻"""
    # 同一排：对每一排，两人在该排的指示变量相等
    for r in range(1, NUM_ROWS + 1):
        row_seats = seats_in_row(r)
        model.addCons(
            quicksum(x["J", s] for s in row_seats) == quicksum(x["K", s] for s in row_seats),
            name=f"JK_same_row_{r}",
        )
    # 不相邻：同一排内，J 和 K 不能占据相邻列
    for r in range(1, NUM_ROWS + 1):
        row_seats = sorted(seats_in_row(r))
        for idx in range(len(row_seats) - 1):
            s, t = row_seats[idx], row_seats[idx + 1]
            model.addCons(x["J", s] + x["K", t] <= 1, name=f"JK_not_adj_{s}_{t}_a")
            model.addCons(x["K", s] + x["J", t] <= 1, name=f"JK_not_adj_{s}_{t}_b")


def add_row_capacity_constraints(model, x):
    """约束 10、11：每排最多 4 人；第 2 排至少 3 人"""
    for r in range(1, NUM_ROWS + 1):
        row_seats = seats_in_row(r)
        model.addCons(
            quicksum(x[i, s] for i in STUDENTS for s in row_seats) <= 4,
            name=f"row_max4_{r}",
        )
    row2 = seats_in_row(2)
    model.addCons(
        quicksum(x[i, s] for i in STUDENTS for s in row2) >= 3,
        name="row2_min3",
    )


def add_a_c_diff_col(model, x):
    """约束 12：A 和 C 不能坐在同一列"""
    for c in range(1, NUM_COLS + 1):
        col_seats = seats_in_col(c)
        model.addCons(
            quicksum(x["A", s] for s in col_seats) + quicksum(x["C", s] for s in col_seats) <= 1,
            name=f"AC_diff_col_{c}",
        )


def add_b_l_diff_row(model, x):
    """约束 13：B 和 L 不能坐在同一排"""
    for r in range(1, NUM_ROWS + 1):
        row_seats = seats_in_row(r)
        model.addCons(
            quicksum(x["B", s] for s in row_seats) + quicksum(x["L", s] for s in row_seats) <= 1,
            name=f"BL_diff_row_{r}",
        )


def add_all_constraints(model, x):
    """一次性添加所有硬约束"""
    add_basic_constraints(model, x)
    add_fixed_position_constraints(model, x)
    add_d_e_adjacent(model, x)
    add_f_g_not_adjacent(model, x)
    add_j_k_same_row_not_adjacent(model, x)
    add_row_capacity_constraints(model, x)
    add_a_c_diff_col(model, x)
    add_b_l_diff_row(model, x)