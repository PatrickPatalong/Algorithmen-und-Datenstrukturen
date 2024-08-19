def read_pgm(filename):
    # read data into a 'bytes' object
    with open(filename, 'rb') as f:
        d = f.read()
    lines = d.split(b'\n')

    # parse the file header
    # check first header field for valid PGM
    first_header = lines[0]
    if first_header != b'P5':
        raise ValueError("'%s' is not a valid PGM file" % filename)
    # find second header field and read image size and value range
    k = 1
    while lines[k][:1] == b'#':
        k += 1          # skip comment lines starting with '#'
    second_header = lines[k]
    w, h, c = [int(i) for i in second_header.split()]

    # convert the data behind the second header field
    data_start = sum([len(l)+1 for l in lines[:k+1]])
    data = [int(i) for i in d[data_start:]]

    return w, h, data

def write_pgm(width, height, data, filename):
    # create the header fields
    s = 'P5\n# width height max_col\n%d %d %d\n' % (width, height, 255)

    # concatenate header fields and data into a 'bytes' object
    import array
    t = bytes(s, "ascii") + array.array('B', data)

    # write the bytes to the file
    with open(filename, 'wb') as f:
        f.write(t)

def test_pgm():
    w, h, d = read_pgm('cells.pgm')
    write_pgm(w, h, d, 'test_output.pgm')
    import filecmp
    # check that both files are identical
    assert filecmp.cmp('cells.pgm', 'test_output.pgm')
