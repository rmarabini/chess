xMapper = {}
yMapper = {}
xMapperT = {}
yMapperT = {}
for k, v in zip([1, 2, 3, 4, 5, 6, 7, 8, 9],
                [0, 1, 2, 3, 4, 5, 6, 7, 9]):
    yMapper[k] = v
for k, v in zip(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i'],
                [0, 1, 2, 3, 4, 5, 6, 7, 8]):
    xMapper[k] = v
for k, v in zip([0, 1, 2, 3, 4, 5, 6, 7],
                [1, 2, 3, 4, 5, 6, 7, 8]
                ):
    yMapperT[k] = v
for k, v in zip([0, 1, 2, 3, 4, 5, 6, 7],
                ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']):
    xMapperT[k] = v



