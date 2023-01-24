import os
import shutil
import sys
from PIL import Image, ImageDraw, ImageFont
import imageio.v2 as imageio
import structures
import time
#set Arial as the font for htmlize
font = ImageFont.truetype("arial.ttf", 15)




#FUNCTIONS
# -*- coding: utf-8 -*-
def htmlize(array):
    s = []
    for row in array:
        for cell in row:
            s.append('▓▓' if cell else '░░')
        s.append('\n')
    return ''.join(s)

# Get the number of rows and columns in the array
def duplicate_array(array):
    rows = len(array)
    cols = len(array[0])

    # Create a new, empty array to hold the duplicate
    duplicate = []

    # Iterate over the rows
    for i in range(rows):
        # Create an empty row
        row = []
        # Iterate over the columns
        for j in range(cols):
            row.append(array[i][j])
        duplicate.append(row)

    return duplicate


#Add 2x layers to the cells
def add_layer(cells):
    for row in cells:
        row.append(0)
        row.append(0)
        row.insert(0, 0)
        row.insert(0, 0)
    row_length = len(cells[0])
    new_row = []
    for i in range(row_length):
        new_row.append(0)
    cells.append(new_row)
    cells.append(new_row)
    cells.insert(0, new_row)
    cells.insert(0, new_row)
    
    
#check the numnber of neighbours the cell has
def neighbours(table, rowcoord, colcoord):
    neighbour_count = 0
    item_counter = 0
    for row in table[rowcoord - 1: rowcoord + 2]:
        for value in row[colcoord - 1: colcoord + 2]:
            item_counter = item_counter + 1
            if item_counter == 5:
                continue
            else:     
                if value == 1:
                    neighbour_count = neighbour_count + 1
    return neighbour_count
                
            
#checks if the cell is alive 
def islive(table, rowcoord, colcoord):
    if table[rowcoord][colcoord] == 1:
        return True
    else:
        return False


#prints an array nicely for testing purposes           
def print_array(array):
    for row in array:
        print(row)
        
        
#creates an array of size rows x cols
def create_array(rows, cols):
    return [[0 for _ in range(cols)] for _ in range(rows)]




#makes the array as small as possible
def smallest_rectangle(array):
    # Step 1
    indices = []
    for i in range(len(array)):
        for j in range(len(array[i])):
            if array[i][j] == 1:
                indices.append((i, j))
    # Step 2
    smallest_row = min(indices, key=lambda x: x[0])[0]
    largest_row = max(indices, key=lambda x: x[0])[0]
    smallest_col = min(indices, key=lambda x: x[1])[1]
    largest_col = max(indices, key=lambda x: x[1])[1]
    # Step 3
    new = [array[i][smallest_col:largest_col + 1] for i in range(smallest_row,largest_row + 1)]
    return new


def create_image_array(number):
    image_array = []
    for i in range(number):
        image_array.append(f"Gen{i}.jpeg")
    return image_array


#find the largest height and width of an image in pixels
def pxmaxmin(widths, heights):
    maxw = max(widths)
    maxh = max(heights)
    return maxw, maxh


def link(uri, label=None):
    if label is None: 
        label = uri
    parameters = ''

    # OSC 8 ; params ; URI ST <name> OSC 8 ;; ST 
    escape_mask = '\033]8;{};{}\033\\{}\033]8;;\033\\'

    return escape_mask.format(parameters, uri, label)


def get_generation(cells, generations):

    #create directory for output
    os.mkdir("Output")
    os.chdir("Output")

    #create list of image files for gif
    image_files = create_image_array(generations)

    #create list for heights and widths of images
    pxwidths_list = []
    pxheights_list = []

    #print starting generation       
    #print("Starting")
    #print(htmlize(cells))
    #print("\n")

    #determine widths of colored chars
    #Work out the size of the image needed
    left, top, right, bottom = font.getbbox("▓▓")
    text_width = right - left
    text_height = bottom - top

    #create a working duplicate
    dup = duplicate_array(cells)
     
        
    for i in range(generations):
        add_layer(dup)
        new_array = create_array(len(dup), len(dup[0]))
        
        
        for row in range(len(dup)): # equals 
            for column in range(len(dup[row])): # equals
                if row != 0 and column != 0 and row != len(dup)-1 and column != len(dup[row])-1:
                    #print(row, column, " with neighbours: ", neighbours(cells, row, column))
                    #rules
                    liveordead = islive(dup, row, column)
                    numneighbours = neighbours(dup, row, column)
                    
                    if liveordead == True and numneighbours < 2:
                        new_array[row][column] = 0
                    elif liveordead == True and numneighbours > 3:
                        new_array[row][column] = 0
                    elif liveordead == True and (numneighbours == 2 or numneighbours == 3):
                        new_array[row][column] = 1
                    elif liveordead == False and numneighbours == 3:
                        new_array[row][column] = 1 
                    else:
                        continue
                        

        dup = smallest_rectangle(new_array)

        #Printing in terminal
        #print("Generation: ", i)
        #print_array(dup) in terminal
        #print(htmlize(dup))

        #create .txt file
        with open(f"Gen{i}.txt", "w") as output_file:
            print(htmlize(dup), file = output_file)


        #create .jpeg from .txt file
        with open(f"Gen{i}.txt", "r") as file:
        # Read the contents of the file
            text = file.read() 

        #Work out the size of the image needed
        #left, top, right, bottom = font.getbbox("▓▓")
        #text_width = right - left
        #text_height = bottom - top

        pxwidth = text_width * len(dup[0])
        pxwidths_list.append(pxwidth)

        pxheight =  text_height * len(dup)
        pxheights_list.append(pxheight)


        # Create an image with a white background
        image = Image.new("RGB", (pxwidth, pxheight), (255, 255, 255))
        # Get a drawing context
        draw = ImageDraw.Draw(image)
        # Draw the text on the image
        draw.text((0, 0), text, fill=(0, 0, 0), font = font, spacing = 5, align = "left")
        # Save the image to a file
        image.save(f"Gen{i}.jpeg", "JPEG")

        #remove the txt file
        os.remove(f"Gen{i}.txt")

        sys.stdout.write(f"\rCompleted Generation {i + 1} / {generations} generations")
        sys.stdout.flush()




    print("Creating gif \n")
    
    #resize all jpeg images
    maximumw, maximumh = pxmaxmin(pxwidths_list,pxheights_list)
    cwd = os.getcwd()
    for filename in os.listdir(cwd):
        im = Image.open(filename)
        im = im.resize((maximumw, maximumh))
        im.save(filename)




    #create gif
    images = []
    for file in image_files:
        images.append(imageio.imread(file))

    #save to downloads folder
    download_folder = os.path.expanduser("~/Downloads")
    imageio.mimsave(f"{download_folder}/animation.gif", images)

    #cleanup and delete Output folder
    # Get the current working directory
    current_dir = os.getcwd()
    # Get the parent directory of the current working directory
    parent_dir = os.path.dirname(current_dir)
    # Change the current working directory to the parent directory
    os.chdir(parent_dir)
    #remove Output folder
    shutil.rmtree("Output")


    return dup


#End of Functions
####################################################################################



#main
hyperlink = link("https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life", "Conway's Game of Life")
print(f"Welcome to {hyperlink}!\n")
time.sleep(0.8)
print("These are the structures that you can choose from:")
#Get structures from structures
only_vars = [var for var in dir(structures) if not callable(getattr(structures, var)) and not var.startswith("__")]
list = "\n".join(only_vars)
print(list + "\n")
time.sleep(0.8)

while True:
    structure_choice = input("What structure would you like to chooose?\n")
    if structure_choice.lower() not in only_vars:
        print("Sorry, you need to choose a structure from the list\n")
        time.sleep(0.8)
    else:
        break
print("\n")

while True:
    generation_choice = int(input("And how many generations would you like?\n"))
    if generation_choice > 2000 or generation_choice <= 0:
        print("Please pick a number between 1 and 2000")
        time.sleep(0.8)
    else:
        break
print("\n")

print("Okay, starting now!\n")



get_generation(getattr(structures, structure_choice.lower()), generation_choice)

print("\n")
print(f"The gif of {structure_choice} for {generation_choice} generations has been saved to your downloads folder\n")