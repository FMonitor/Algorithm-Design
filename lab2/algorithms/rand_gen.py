import random
import os

def rand_gen(n: int, lb: int = 0, ub: int = 100) -> list:
    """
    生成 n 个随机点对（x, y），x 和 y 的范围在 [lb, ub] 之间。
    生成的点对将保存在一个名为 "rand.txt" 的文件中用于检验，文件格式如下：
    第一行：随机点对的数量和范围
    后续每行：一个随机点对，格式为 "x y"。

    :param n: 随机点对的数量
    :param lb: 随机点对的下界
    :param ub: 随机点对的上界
    """
    file_path = "./lab2/data/"
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    file_name = os.path.join(file_path, f"rand{n}.txt")
    points = set()  # 使用集合存储点对以避免重复
    while len(points) < n:
        x = random.randint(lb, ub)
        y = random.randint(lb, ub)
        points.add((x, y))  # 集合会自动去重

    with open(file_name, "w") as f:
        f.write(f"Random point counts: {n}. Ranged within [{lb}, {ub}]\n")
        for x, y in points:
            f.write(f"{x} {y}\n")

    print(f"生成 {n} 个随机点对，范围在 [{lb}, {ub}] 之间，已保存到 {file_name}。")

    return list(points)


if __name__ == "__main__":
    rand_gen(10, 0, 100)
