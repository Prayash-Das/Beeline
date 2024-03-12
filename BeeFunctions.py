#Author: Prayash Das
#Date: 02/29/2024
#Description: This program contains all the functions required to run the main file in Beeline.py program.
import os

def load_flower_list():
    '''
    A function to load the flower list file, that has no parameters, returns Dictionary of Tuples, and
    prompts the user for the filename and checks for the filename
    if it exists and repeatedly ask the user for the file unless the correct filename given.
    :return: Dictionary of Tuples based on the information in the user specified file.
    '''
    flower_dict = {}

    while True:
        # Prompt the user for the flower list file name
        flower_list_file_name = input("Please enter the name of the file containing your flower to points mapping:")

        # Check if the file exists
        if os.path.exists(flower_list_file_name):
            break
        else:
            print(f"{flower_list_file_name} does not exist!")

    with open(flower_list_file_name, 'r') as file:
        for line in file:
            # Remove leading and trailing whitespace and split the line by comma
            row = line.strip().split(',')

            # Extract information from the row
            flower_letter, flower_name, pollen_count = [item.strip() for item in row]

            # Store information in the dictionary
            flower_dict[flower_letter] = (flower_letter, flower_name, int(pollen_count))

    return flower_dict
def create_field(flower_info_dict):
    '''
    A function to create the field, that takes in a Dictionary of Tuples containing flower information, and repeatedly reprompt for a
    new filename if the file does not exist. Raises a Typeerror exception if a flower not in the Dictionary is detected in the input file.

    :param flower_info_dict:Dictionary of tuples containing flower information.
    :return:Newly constructed two-dimensional list.
    '''
    field = []

    while True:
        # Prompt the user for the field file name
        field_file_name = input("Please enter the name of the file containing your field:")

        # Check if the file exists
        if os.path.exists(field_file_name):
            break
        else:
            print(f"{field_file_name} does not exist!")

    with open(field_file_name, 'r') as file:
        for line in file:
            # Remove leading and trailing whitespace and split the line by comma
            row = line.strip().split(',')

            # Validate each character in the row
            for char in ''.join(row):
                if char not in ['H', 'P', ' ', *flower_info_dict.keys()]:
                    raise TypeError(f"{char} is not a known flower type for this field!")

            # Append the row to the field
            field.append(row)

    return field



def copy_field(original_field):
    '''
    A function to make a copy of the field, that takes in a two-dimensional list as a parameter, correctly
    creates, and returns a two-dimensional list.
    :param original_field:It takes in a two-dimensional list as a parameter and generates a copy of the passed in
    two-dimensional list.
    :return:Newly constructed two-dimensional list.
    '''
    copied_field = []

    for row in original_field:
        # Create a new row with the same dimensions as the original
        new_row = []

        for char in row:
            # Convert flowers and pitcher plants to spaces
            if char.isalpha() and char.upper() != 'H':
                new_row.append(' ')
            else:
                new_row.append(char)

        # Add the new row to the copied field
        copied_field.append(new_row)

    return copied_field

def print_field(field):
    '''
    A function to print the field, taking in one, two-dimensional list, outputting the field in a pleasing grid format and,
    outputs the index values along top and left of the grid.
    :param field:One two-dimensional list.
    :return:None.
    '''
    # Print column indices along the top
    print("   ", end="")
    for col_index in range(len(field[0])):
        print(f"{col_index:2}", end="  ")
    print("\n")

    # Print the rows with row indices
    for row_index, row in enumerate(field):
        print(f"{row_index:2}|", end="")
        for char in row:
            print(f"{char:2}|", end=" ")
        print("\n")
def game_intro(flower_info_dict, num_scouts, num_workers, pollen_needed):
    '''
    A function to output the game's introductory information along with all of the requisite information.
    :param flower_info_dict:Dictionary of Tuples containing flower information.
    :param num_scouts:Number of scout bees.
    :param num_workers:Number of worker bees.
    :param pollen_needed:Amount of pollen needed to win the game.
    :return:None.
    '''
    print("Welcome to Beeline!")
    print("You are the queen bee tasked with ensuring your hive produces enough honey.")
    print("Honey is created from pollen in flowers, which you will need to send bees out to find and harvest!")
    print("You have two kinds of bees: scout bees and worker bees.")
    print("Scout bees fly out to a location in the field and reveal 3x3 area around the specified location.")
    print("Workers fly out to a location, harvest flowers in a 3x3 area around the specified location,\nand also reveal the area they have harvested. However, you only have 5 scout bees and")
    print("5 worker bees to obtain the 20 units of pollen you need to produce enough honey. Note, once a bee has been\nsent out it cannot be used again and a flower can be only harvested once! Oh, and watch out for pitcher plants!")
    print("They will trap your bees and prevent them from returning to the hive. Good luck!")
    print("The flower contains the following units of pollen:")
    print("Letter | Name           | Pollen")
    print("-------|----------------|-------")
    for flower_data in flower_info_dict.values():
        flower_letter, flower_name, pollen_count = flower_data
        print(f"   {flower_letter}   | {flower_name:14} |   {pollen_count:2}")

def check_bee_area(hidden_field, visible_field, x, y, bee_type, flower_info_dict):
    '''
    A function to check the area a bee is sent to, determined if the user specified x,y coordinates are outside
    the bounds of the field, informing the user of it, determines if the bee jas been trapped by a pitcher plant, informing
    the user of it, correctly reveal flowers from the hidden field to the visible field if the player uses a scout bee, and harvests
    any unwanted flowers by updating them from their respective letters to U in both lists.
    :param hidden_field:One two-dimensional list representing the hidden list.
    :param visible_field:One two-dimensional list representing the visible list.
    :param x:Integer coordinates.
    :param y:Integer coordinates.
    :param bee_type:A string containing a single character representing the type of bee.
    :param flower_info_dict:Dictionary of Tuples containing flower information.
    :return:Integer count of the amount of pollen harvested.
    '''
    pollen_harvested = 0

    # Check if the coordinates are outside the bounds
    if not (0 <= x < len(hidden_field[0]) and 0 <= y < len(hidden_field)):
        print("Your bee has flown outside the field and gotten lost!")
        return 0

    # Check for pitcher plants in the 3x3 grid
    for i in range(max(0, x - 1), min(len(hidden_field[0]), x + 2)):
        for j in range(max(0, y - 1), min(len(hidden_field), y + 2)):
            if hidden_field[j][i].upper() == 'P':
                print("Your bee must have fallen into a pitcher plant because it never returned!")
                return pollen_harvested

    # Examine the 3x3 grid
    for i in range(max(0, x - 1), min(len(hidden_field[0]), x + 2)):
        for j in range(max(0, y - 1), min(len(hidden_field), y + 2)):
            if bee_type == 'scout' and (hidden_field[j][i].upper() in flower_info_dict or hidden_field[j][i] == 'U'):
                visible_field[j][i] = hidden_field[j][i]
            elif bee_type == 'worker' and hidden_field[j][i] == 'U':
                visible_field[j][i] = 'U'
            elif bee_type == 'worker' and hidden_field[j][i].upper() in flower_info_dict:
                flower_letter = hidden_field[j][i].upper()
                pollen_harvested += flower_info_dict[flower_letter][2]
                hidden_field[j][i] = 'U'
                visible_field[j][i] = 'U'


    return pollen_harvested
