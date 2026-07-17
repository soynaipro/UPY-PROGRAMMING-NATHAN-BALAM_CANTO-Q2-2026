import random
import stddraw

from color import Color

def bubble_sort(numbers):
    #get the lenght of the array
    n = len(numbers)
    for sweep in range(n):
        for pair in range( 0, n-1 - sweep):
            if numbers[pair] > numbers[pair + 1]:
                numbers[pair], numbers[pair + 1] = numbers [pair+1], numbers[pair]

def insertion_sort(numbers):
    #get the lenght of the array
    n = len(numbers)
    for i in range(1, n):
        j = i
        while j > 0 and numbers[j - 1] > numbers[j]:
            numbers[j - 1], numbers[j] = numbers[j], numbers[j - 1]
            j -= 1

def selection_sort(numbers):
    #get the lenght of the array
    n = len(numbers)
    for sweep in range(n):
        min_idx = sweep
        for pair in range(sweep + 1, n):
            if numbers[pair] < numbers[min_idx]:
                min_idx = pair
        if min_idx != sweep:
            numbers[sweep], numbers[min_idx] = numbers[min_idx], numbers[sweep]

def draw_bars (numbers, selected=()):
    stddraw.clear()
    n = len(numbers)
    bar_width = 10.0 / n
    
    for i, number in enumerate(numbers):
        x= i * bar_width + bar_width / 2
        color = Color(255, 90, 90) if i in selected else Color(70, 130, 220)
        stddraw.setPenColor(color)
        stddraw.filledRectangle(x - bar_width / 2, 0, bar_width * 0.9, number)
    stddraw.show(500)
    
# ANIMATED
def bubble_sort_animated(numbers):
    # CONIG - Canvas
    stddraw.setXscale(-0.1, 10)
    stddraw.setYscale(-0.5, max(numbers) + 1)
    #get the lenght of the array
    n = len(numbers)
    
    for sweep in range(n):
        for pair in range( 0, n-1 - sweep):
            #DRAW the rectangles before the swap
            draw_bars(numbers, selected= (pair, pair +1))
            if numbers[pair] > numbers[pair + 1]:
                numbers[pair], numbers[pair + 1] = numbers [pair+1], numbers[pair]
                #DRAW the rentangles after the swap
                draw_bars(numbers, selected= (pair, pair +1))
                
    draw_bars(numbers)
    stddraw.show()

def insertion_sort_animated(numbers):
    # CONIG - Canvas
    stddraw.setXscale(-0.1, 10)
    stddraw.setYscale(-0.5, max(numbers) + 1)
    #get the lenght of the array
    n = len(numbers)
    
    for i in range(1, n):
        j = i
        while j > 0:
            #DRAW the rectangles before the swap
            draw_bars(numbers, selected= (j - 1, j))
            if numbers[j - 1] > numbers[j]:
                numbers[j - 1], numbers[j] = numbers[j], numbers[j - 1]
                #DRAW the rentangles after the swap
                draw_bars(numbers, selected= (j - 1, j))
                j -= 1
            else:
                break
                
    draw_bars(numbers)
    stddraw.show()

def selection_sort_animated(numbers):
    # CONIG - Canvas
    stddraw.setXscale(-0.1, 10)
    stddraw.setYscale(-0.5, max(numbers) + 1)
    #get the lenght of the array
    n = len(numbers)
    
    for sweep in range(n):
        min_idx = sweep
        for pair in range(sweep + 1, n):
            #DRAW the rectangles before checking
            draw_bars(numbers, selected=(pair, min_idx))
            if numbers[pair] < numbers[min_idx]:
                min_idx = pair
                #DRAW the rectangles after a new minimum is found
                draw_bars(numbers, selected=(pair, min_idx))
                
        if min_idx != sweep:
            #DRAW the rectangles before the swap
            draw_bars(numbers, selected=(sweep, min_idx))
            numbers[sweep], numbers[min_idx] = numbers[min_idx], numbers[sweep]
            #DRAW the rentangles after the swap
            draw_bars(numbers, selected=(sweep, min_idx))
                
    draw_bars(numbers)
    stddraw.show()
                
numbers = [random.randint(0,100) for x in range(10)]
print(f"Before: {numbers}")
#bubble_sort(numbers)
#insertion_sort(numbers)
#selection_sort(numbers)
#bubble_sort_animated(numbers)
#insertion_sort_animated(numbers)
selection_sort_animated(numbers)
print(f"After: {numbers}")