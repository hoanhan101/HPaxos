def split_string(string, delimeter):
    string_array = string.split(delimeter)
    return string_array

def is_first_id_larger(id_1, id_2):
    if int(id_1[0]) >= int(id_2[0]) and ord(id_1[1]) >= ord(id_2[1]):
        return True
    else:
        return False

if __name__ == '__main__':
    permitted_id = "2,A"
    data = "2,B"
    print(ord('A') > ord('B'))

    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    for char in alphabet:
        print(char, ord(char))


    new_permitted_id = split_string(permitted_id, ',')
    new_data = split_string(data, ',')
    print(new_permitted_id)
    print(new_data)

    print(ord(new_data[1]), ord(new_permitted_id[1]))
    # 12 > 2, A>=A


    if int(new_data[0]) >= int(new_permitted_id[0]) and ord(new_data[1]) >= ord(new_permitted_id[1]):
        print("True")
    else:
        print("False")

    if is_first_id_larger(new_data, permitted_id):
        print("True")