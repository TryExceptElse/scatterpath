def translate(in_path='data.csv', out_path='data.dat'):
    with open(in_path, 'r') as in_f, open(out_path, 'w') as out_f:
        out_f.writelines([f'{x} {y}\n' for x, y, *_ in
                          [line.split(', ') for line in in_f.readlines()]])


if __name__ == '__main__':
    translate()
