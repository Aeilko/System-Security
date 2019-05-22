
def to_binary_string(array):
    result = ""
    for x in array:
        result += '1' if x else '0'

    return result

def print_as_binary_string(array):
    print(to_binary_string(array))