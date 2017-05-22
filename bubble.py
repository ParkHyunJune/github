def bubble_sort():
    bubble = [ i for i in range(0,100) ]
    for x in range(0, 100):
        import random
        num = random.randint(0,100)
        bubble[x] = num
    bubble.sort()
    print(bubble)
bubble_sort()


