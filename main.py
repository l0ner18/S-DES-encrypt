from tkinter import *
from tkinter.messagebox import showerror, showinfo
import random, os
import xlsxwriter

# создание окна
ws = Tk()
ws.title('S-DES')
ws.geometry('355x200')
ws["bg"] = "gray80"

Label(ws, bg='gray81', text="Проверка").place(x=60, y=10)
Label(ws, bg='gray81', text="Фраза").place(x=30, y=30)
decimal_number_ = Entry(ws)
decimal_number_.place(x=30, y=50)

Label(ws, bg='gray81', text="Ключ").place(x=30, y=75)
decimal_number_key_ = Entry(ws)
decimal_number_key_.place(x=30, y=95)

Label(ws, bg='gray81', text="Генерация").place(x=225, y=10)
Label(ws, bg='gray81', text="Количество данных").place(x=200, y=30)
decimal_count_ = Entry(ws)
decimal_count_.place(x=200, y=50)

def Decimal_number(number):
    x=''
    decimal_number = number
    if decimal_number != '':
        decimal_number = int(decimal_number)
        binary_representation = bin(int(decimal_number))[2:]
        if len(binary_representation) < 8:
            x = '0' * (8 - len(binary_representation)) + binary_representation
        else:
            x = binary_representation
    return x

def Decimal_number_key(key):
    k=''
    decimal_number_key = key
    if decimal_number_key != '':
        decimal_number_key = int(decimal_number_key)
        binary_representation = bin(decimal_number_key)[2:]
        if len(binary_representation) < 10:
            k = '0' * (10 - len(binary_representation)) + binary_representation
        else:
            k = binary_representation
    return k

def input_number():
    decimal_number = decimal_number_.get()
    return decimal_number

def input_key():
    decimal_number_key = decimal_number_key_.get()
    return decimal_number_key

def input_count():
    decimal_count = decimal_count_.get()
    return decimal_count

dict1 = {
        '0000': '01', '0001': '00', '0010': '11', '0011': '10',
        '0100': '11', '0101': '10', '0110': '01', '0111': '00',
        '1000': '00', '1001': '10', '1010': '01', '1011': '11',
        '1100': '11', '1101': '01', '1110': '11', '1111': '01'
}

dict2 = {
    '0000': '01', '0001': '01', '0010': '10', '0011': '11',
    '0100': '10', '0101': '00', '0110': '01', '0111': '11',
    '1000': '11', '1001': '00', '1010': '01', '1011': '00',
    '1100': '10', '1101': '01', '1110': '00', '1111': '11'
}

keyE1 = "41232341" # перестановка E
keyE2 = "2431" # перестановка P
def cyclic_shift(input_str, positions):
    length = len(input_str)
    positions %= length

    shifted_str = input_str[positions:] + input_str[:positions]
    return shifted_str

def permutation_with_expansion(data_for_permutation, keyE1): #перестановка с расширением
    result = ''
    for i in range(0, 8):
        result = result + data_for_permutation[int(keyE1[i]) - 1]
    return result

def summ_with_key(data, key): # сумма с ключем
    result = ''
    for i in range(0, 8):
        if data[i] == key[i]:
            result += "0"
        else:
            result += "1"
    return result

def summ_with_side(data, key): # сумма с другой частью
    result = ''
    for i in range(0, 4):
        if data[i] == key[i]:
            result += "0"
        else:
            result += "1"
    return result

def permutation(data_for_permutation, key): #перестановка
    result = ''
    for i in range(0, 4):
        result = result + data_for_permutation[int(key[i]) - 1]
    return result

def f(string, key):
    test = permutation_with_expansion(string, keyE1)  # перестановка с расширением
    summ = summ_with_key(test, key)  # сложение с ключем
    a = dict1[summ[0] + summ[3] + summ[1] + summ[2]]
    b = a + dict2[summ[4] + summ[7] + summ[5] + summ[6]]
    v = permutation(b, keyE2)
    return v

def Answer(data, key):
    x = data
    k = key

    permutation = [3, 5, 2, 7, 4, 10, 1, 9, 8, 6]

    result = ''

    for i in range(10):
        index = permutation[i]
        result = result + k[index - 1]

    left_side = result[:5]
    right_side = result[-5:]

    shifted_str1 = cyclic_shift(left_side, 1)
    shifted_str2 = cyclic_shift(right_side, 1)

    result_for_permutation = shifted_str1 + shifted_str2
    permutation = [6, 3, 7, 4, 8, 5, 10, 9]
    key1 = ''

    for i in range(8):
        index = permutation[i]
        key1 = key1 + result_for_permutation[index - 1]

    shifted1 = cyclic_shift(shifted_str1, 2)
    shifted2 = cyclic_shift(shifted_str2, 2)

    result_for_permutation2 = shifted1 + shifted2
    key2 = ''

    for i in range(8):
        index = permutation[i]
        key2 = key2 + result_for_permutation2[index - 1]

    permutation = [2, 6, 3, 1, 4, 8, 5, 7] # перестановка IP


    result_ip = ''
    for i in range(8):
        index = permutation[i]
        result_ip = result_ip + x[index - 1]

    left_side = str(result_ip[-4:] * 2)
    right_side = result_ip[-4:]

    result_before_f1 = summ_with_side(f(left_side, key1), result_ip[:4])

    result_before_f2 = summ_with_side(f(result_before_f1 * 2, key2), result_ip[4:])

    permutation_last = [4, 1, 3, 5, 7, 2, 8, 6]
    answer = permutation_with_expansion(result_before_f2 + result_before_f1, permutation_last)
    return answer

def generate_number():
    return random.randint(0, 255)

def generate_key():
    return random.randint(0, 1023)
def Generate(count):
    try:
        workbook = xlsxwriter.Workbook('dataSDES.xlsx')
        worksheet = workbook.add_worksheet()
        worksheet.write('A1', 'X')
        worksheet.write('B1', 'K')
        worksheet.write('C1', 'Answer')

        for i in range(1, int(count) + 1):
            x = str(Decimal_number(generate_number()))
            k = str(Decimal_number_key(generate_key()))
            answer = Answer(x, k)

            worksheet.write(f'A{i + 1}', int(x, 2))
            worksheet.write(f'B{i + 1}', int(k, 2))
            worksheet.write(f'C{i + 1}', int(answer, 2))

        workbook.close()

        # Проверяем, существует ли файл после закрытия
        if os.path.exists('dataSDES.xlsx'):
            showinfo("Информация", "Данные успешно сгенерированы и сохранены в dataSDES.xlsx")
        else:
            showerror("Ошибка", "Не удалось создать файл")

    except Exception as e:
        showerror("Ошибка", f"Произошла ошибка при генерации данных: {str(e)}")

def check():
    data = input_number()
    key = input_key()

    if data == '' or key == '':
        showerror(title="Ошибка", message="Заполните все поля")
    else:
        data_to_answer = Decimal_number(data)
        key_to_answer = Decimal_number_key(key)
        answer = Answer(str(data_to_answer), str(key_to_answer))
        Label(ws, bg='gray81', text=f'Результат: {int(answer, 2)}').place(x=50, y=170)
def check_generate():
    count = input_count()

    if count == '':
        showerror(title="Ошибка", message="Заполните поле")
    else:
        Generate(count)

btn = Button(ws, text="Зашифровать", command=check)
btn.place(x=50, y=135)
btn_generate = Button(ws, text="Сгенерировать", command=check_generate)
btn_generate.place(x=215, y=135)
ws.mainloop()