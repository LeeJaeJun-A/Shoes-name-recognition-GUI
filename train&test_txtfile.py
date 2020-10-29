import os
from random import shuffle

gdrive_path = '/content/gdrive/My Drive/darknet/custom/'
image_path = 'C:/Users/msi/Desktop/openCV project/train'

test_per = 0.2
paths = []

os.chdir(image_path)
for a, b, files in os.walk('.'):
    for i in files:
        if i.endswith('.jpg'):
            paths.append(gdrive_path + i + '\n')
            shuffle(paths)

#path중 8:2로 train과 test로 나눔.
paths_test = paths[:int(len(paths)*test_per)]
path_train = paths[int(len(paths)*test_per):]

with open('my_train.txt', 'w') as my_train_txt:
    for path in path_train:
        my_train_txt.write(path)

with open('my_test.txt', 'w') as my_test_txt:
    for path in paths_test:
        my_test_txt.write(path)

