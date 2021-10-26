from game import sudoku


def main():
    _, size = map(int, input().split())
    colors = input().split()
    sudoku.make(colors, size)
    for i in range(size):
        sudoku.add_row(input(), i)
    answer = sudoku.start()
    ans = []
    if answer:
        flag = answer
        while flag:
            ans.append(flag)
            flag = flag.parent
        for flag in ans[::-1]:
            print("\n | | |\n ۷ ۷ ۷\n")
            print(flag)
            print("depth: %i" % flag.depth)
        print("\nfinished :)")


if __name__ == "__main__":
    main()
