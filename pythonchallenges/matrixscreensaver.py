import random, sys, time

WIDTH = 200

try:
    columns = [0] * WIDTH
    while True:
        for i in range(WIDTH):
            if random.random() < 0.1:
                columns[i] = random.randint(20, 25)
            if columns[i] == 0:
                print(" ", end="")
            else:
                print(random.choice([0,1]), end=" ")
                columns[i] -= 1
        print()
        time.sleep(0.1)
except KeyboardInterrupt:
    sys.exit()