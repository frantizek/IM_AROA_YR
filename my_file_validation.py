from pathlib import Path

def file_exist(my_file) -> bool:
    try:
        Path(my_file).resolve(strict=True)
    except FileNotFoundError:
        print('ERROR: The file does not exist.')
        return False
    else:
        # print('File does exist.')
        return True


def file_size(my_file) -> bool:
    try:
        Path(my_file).stat()
    except FileNotFoundError:
        print('ERROR: The file does not exist.')
        return False
    else:
        if Path(my_file).stat().st_size <= 0:
            print('File does NOT contain information.')
            return False
        else:
            # print(f'File size is {Path(my_file).stat().st_size}.')
            return True


def file_lines(my_file) -> bool:
    if sum(1 for _ in open(my_file)) > 1:
        # print(f'File lines in the file: {sum(1 for _ in open(my_file))}.')
        return True
    else:
        return False


def file_format(my_file) -> bool:
    with open(my_file, mode="r", encoding="utf-8") as f:
        for i, _ in enumerate(f):
            if _.rstrip().find('@') == 0:
                usuario_aroa = _.rstrip().split()
                if len(usuario_aroa) <= 1:
                    print(f'WARNING: The format is invalid for entry {i}, please correct.')
                    print('HINT: The line does not contains the minimum number of values.')
                    return False
                else:
                    telegram_user_name = usuario_aroa[0]
                    indices = [i for i in range(len(usuario_aroa)) if i > 0]
                    swgoh_user_name = " ".join([usuario_aroa[i] for i in indices])
                    # print(f'{swgoh_user_name} lo puedes encontrar en Telegram como {telegram_user_name}')
            else:
                print(f'WARNING: The format is invalid for entry {i}, please correct.')
                print('HINT: The line does not starts with @.')
                return False
    return True
