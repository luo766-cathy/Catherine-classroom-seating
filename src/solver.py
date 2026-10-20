# src/solver.py

from pyscipopt import Model, quicksum
from src.data import STUDENTS, SEATS, seat_to_row_col, satisfaction
from src.constraints import add_all_constraints


def build_model():
    model = Model("classroom_seating")

    # 决策变量 x[i, s]：学生 i 是否坐座位 s
    x = {}
    for i in STUDENTS:
        for s in SEATS:
            x[i, s] = model.addVar(vtype="B", name=f"x_{i}_{s}")

    # 添加所有硬约束
    add_all_constraints(model, x)

    # 目标：最大化总满意度
    model.setObjective(
        quicksum(satisfaction(i, s) * x[i, s] for i in STUDENTS for s in SEATS),
        sense="maximize",
    )
    return model, x


def solve():
    model, x = build_model()
    model.optimize()

    status = model.getStatus()
    print(f"求解状态: {status}")

    if status != "optimal":
        print("未找到最优解，请检查约束。")
        return None

    assignment = {}
    total_score = 0
    for i in STUDENTS:
        for s in SEATS:
            if model.getVal(x[i, s]) > 0.5:
                assignment[i] = s
                total_score += satisfaction(i, s)

    print(f"最大总满意度: {total_score}")
    print("\n座位分配结果：")
    for i in STUDENTS:
        s = assignment[i]
        r, c = seat_to_row_col(s)
        print(f"  学生 {i}: 座位 {s:2d}  (第{r}排 第{c}列)  满意度={satisfaction(i, s)}")

    print("\n按排展示：")
    for r in range(1, 5):
        row_info = []
        for c in range(1, 6):
            s = (r - 1) * 5 + c
            who = next((i for i in STUDENTS if assignment[i] == s), "·")
            row_info.append(f"{who}({s:2d})")
        print(f"  第{r}排: " + "  ".join(row_info))

    return assignment, total_score