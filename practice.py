#x만큼 간격이 있는 n개의 숫자
def number_generator(x, n):
    return [i*x + x for i in range(n)]

print(number_generator(3, 5))



# 핸드폰 번호 가리기
def hide_numbers(s):
    return "*"*(len(s)-4) + s[-4:]

print(hide_numbers('01028437360'))


# 평균 구하기
def average(list):
    sum = 0
    for i in range(len(list)):
        sum += list[i]

    return sum / len(list)


list = [5, 3, 4]
print("평균값 : {}".format(average(list)))