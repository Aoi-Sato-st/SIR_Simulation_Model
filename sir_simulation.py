import random
import math
import csv
import pandas as pd
import matplotlib.pyplot as plt

#state
S, I , R = 0, 1, 2

#paramaters
BETA_RATE = 0.3
GAMMA_RATE = 0.05
HEIGHT = 50
WIDTH = 50


def init_board():
    board = [[S for _ in range(WIDTH)] for _ in range(HEIGHT)]
    y = random.randint(0, HEIGHT - 1)
    x = random.randint(0, WIDTH - 1)
    board[y][x] = I

    return board


def count_infected_neighbors(board, x, y):
    count = 0
    for dy in range(-1, 2):
        for dx in range(-1, 2):
            if dx == 0 and dy == 0:
                continue
            nx = x + dx
            ny = y + dy

            if 0 <= nx < WIDTH and 0 <= ny < HEIGHT:
                if board[ny][nx] == I:
                    count += 1
    
    return count


def update_board(board):
    next_board = [[S for _ in range(WIDTH)] for _ in range(HEIGHT)]

    for y in range(HEIGHT):
        for x in range(WIDTH):
            state = board[y][x]
            I_count = count_infected_neighbors(board, x, y)
            transition = random.random()

            if state == S:
                if I_count == 0:
                    next_board[y][x] = S
                elif I_count == 1:
                    if transition < BETA_RATE:
                        next_board[y][x] = I
                    else:
                        next_board[y][x] = S
                else:
                    if transition < (1 - (1 - BETA_RATE) ** I_count):
                        next_board[y][x] = I
                    else:
                        next_board[y][x] = S

            elif state == I:
                if transition < GAMMA_RATE:
                    next_board[y][x] = R
                else:
                    next_board[y][x] = I

            else:
                next_board[y][x] = R
    return next_board

def calc_SIR(board):
    S_count = sum(cell == S for row in board for cell in row)
    I_count = sum(cell == I for row in board for cell in row)
    R_count = sum(cell == R for row in board for cell in row)

    total = WIDTH*HEIGHT
    return S_count/total, I_count/total, R_count/total

def write_file(file, step, sir):
    s, i, r = sir
    file.write(f"{step},{s},{i},{r}\n")

def plot_sir(filename="sir.csv"):
    df = pd.read_csv(filename)

    plt.plot(df["step"], df["S"], label="Susceptible")
    plt.plot(df["step"], df["I"], label="Infected")
    plt.plot(df["step"], df["R"], label="Recovered")

    plt.xlabel("Step")
    plt.ylabel("Ratio")
    plt.title("SIR Model Simulation")

    plt.legend()
    plt.grid()
    
    plt.savefig("sir_graph.png")  # ← 追加
    plt.show()

def main():
    board = init_board()

    with open("sir.csv", "w") as f:
        f.write("step,S,I,R\n")

        step = 0

        while True:
            sir = calc_SIR(board)
            write_file(f, step, sir)
            step += 1

            if sum(cell == I for row in board for cell in row) == 0:
                break

            board = update_board(board)

    plot_sir("sir.csv")
    
if __name__ == "__main__":
    main()