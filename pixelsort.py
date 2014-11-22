#simple script to sort every row in the image and save its state every n iterations during sorting

import cv2
import os
import math
import random
import numpy as np

#for the sorting steps storing
global steps
global current_row 
global current_iteration 

#the input image
input_image_path = 'input.jpg'

#where to save the glitched image
output_image_path = 'glitched.jpg'

#record the state of the sorting every num iterations
save_every_num_sort_iterations = 50

#where to save the frames later used to generate the gif
output_directory = 'gen/'

#the intensity given rgb
def value(c):    
    return (float(c[0]) + float(c[1]) + float(c[2])) / 3.

#quick sort implementation taken from http://www.geekviewpoint.com/python/sorting/quicksort
#by Isai Damier
def quicksort(line):
    _quicksort(line, 0, len(line) - 1)
 
def _quicksort(line, first, last):
    if first < last:
      pivot = partition(line, first, last)
      _quicksort(line, first, pivot - 1)
      _quicksort(line, pivot + 1, last)
  
def partition(line, first, last) :
    pivot = first + random.randrange(last - first + 1)
    swap(line, pivot, last)

    for i in xrange(first, last):
        if value(line[i]) <= value(line[last]):
            swap(line, i, first)
            first += 1
 
    swap(line, first, last)

    return first
 
def swap(A, x, y):
  tmp = A[x][0]
  tmp1 = A[x][1]
  tmp2 = A[x][2]

  A[x][0] = A[y][0]
  A[x][1] = A[y][1]
  A[x][2] = A[y][2]

  A[y][0] = tmp
  A[y][1] = tmp1
  A[y][2] = tmp2

  global current_iteration
  global current_row
  global steps

  current_iteration += 1

  if (current_iteration % save_every_num_sort_iterations == 0):
    steps[current_row].append(A.copy())

#if the output folder doesn't exist
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

#the image is read from input.jpg
input_image = cv2.imread(input_image_path)

cv2.namedWindow("input", cv2.cv.CV_WINDOW_NORMAL)
cv2.imshow('input', input_image)

steps = list()

#loop through each row of the image
for r in xrange(input_image.shape[0]):
    current_line = input_image[r]
    
    #here we'll save the sorting steps for each row
    steps.append(list())

    current_iteration = 0
    current_row = r

    #initial row
    steps[current_row].append(input_image[r].copy())

    #call the sorting
    quicksort(input_image[r])

    #display the current state of the image
    cv2.imshow('input', input_image)
    cv2.waitKey(10)

    print 'sorting row', r, '/', input_image.shape[0]

#save glitched image
cv2.imwrite(output_image_path, input_image)

#the rows are sorted in different number of steps
max_len = 0
for i in xrange(len(steps)):
    if len(steps[i]) > max_len:
        max_len = len(steps[i])

#loop from glitched to original and save frames
it = 0 
for i in reversed(xrange(max_len)):
    for r in xrange(input_image.shape[0]):

        if (len(steps[r]) <= i):
            input_image[r] = steps[r][-1]
        else:
            input_image[r] = steps[r][i]

    print i, '/', max_len

    cv2.imshow('input', input_image)
    cv2.waitKey(10)

    name = str(it).zfill(5)
    it += 1

    cv2.imwrite(os.path.join(output_directory, name + '.jpg'), input_image)

last = it

#loop from original to glitched and save frames again
for i in xrange(max_len):
    for r in xrange(input_image.shape[0]):

        if (len(steps[r]) <= i):
            input_image[r] = steps[r][-1]
        else:
            input_image[r] = steps[r][i]

    print i, '/', max_len

    cv2.imshow('input', input_image)
    cv2.waitKey(10)

    name = str(i + last).zfill(5)

    cv2.imwrite(os.path.join(output_directory, name + '.jpg'), input_image)

print 'Done.'
print 'To create gif, run: convert *.jpg out.gif'
print 'Press enter!'

cv2.waitKey(0)