#Author: Prayash Das
#Date: 03/04/2024
#Description: This program will create a randomly generated field to a file using the same format as the example files.
#It will prompt the user for the
#name of the file to save the field to, and ask different aspects of the field and will generate a field with the user specified number and types of flowers randomly dispersed throughout
#the map, as well as the number of pitcher plants and a randomly placed beehive.

import random
import os

def save_field_to_file(field, filename):
    '''
    A function to save the generated field to a file.
    :param field:The field to be saved.
    :param filename:The name of the file to save the field to.
    :return:None.
    '''
    with open(filename, 'w') as file:
        for row in field:
            file.write(','.join(row) + '\n')
def read_flower_list(file_path):
    '''
    A function to read the flower list from a file.
    :param file_path:The path to the flower list file.
    :return:A list of flower letters extracted from the file.
    '''
    try:
        with open(file_path, 'r') as file:
            lines = file.read().splitlines()

        # Extract flower letters from the flower list
        flower_list = [line.split(',')[0] for line in lines]

        return flower_list
    except FileNotFoundError:
        raise FileNotFoundError("Error: Flower list file not found.")
    except Exception as e:
        raise Exception(f"Error reading flower list file: {e}")

def generate_field(dimensions, flower_list, num_pitcher_plants, beehive_position, num_flowers):
    '''
    A function to generate a randomly filled with flowers, pitcher plants, and a beehive.
    :param dimensions:Tuple representing the width and height of the field.
    :param flower_list:List of available flower types.
    :param num_pitcher_plants:Number of pitcher plants to place in the field.
    :param beehive_position:Tuple representing the position of beehive in the field.
    :param num_flowers:Number of flowers to place in the field.
    :return:The generated field as a 2D list.
    '''
    # Create an empty field
    field = [[' ' for _ in range(dimensions[0])] for _ in range(dimensions[1])]

    # Place beehive
    field[beehive_position[1]][beehive_position[0]] = 'H'

    # Place flowers
    placed_flowers = 0
    for _ in range(num_flowers):
        flower = random.choice(flower_list)

        x = random.randint(0, dimensions[0] - 1)
        y = random.randint(0, dimensions[1] - 1)

        while field[y][x] != ' ':
            x = random.randint(0, dimensions[0] - 1)
            y = random.randint(0, dimensions[1] - 1)

        if field[y][x] not in flower_list:
            field[y][x] = flower
            placed_flowers += 1

    # Place pitcher plants
    placed_pitcher_plants = 0
    while placed_pitcher_plants < num_pitcher_plants:
        x = random.randint(0, dimensions[0] - 1)
        y = random.randint(0, dimensions[1] - 1)

        if field[y][x] == ' ':
            field[y][x] = 'P'
            placed_pitcher_plants += 1

    return field

def main():
    '''
    The main function.
    :return:
    '''
    try:
        # Get user input
        filename = input("Enter the name of the file to save the field to: ")
        flowerlist_filename = input("Enter the name of the flower list file: ")

        # Check if the flower list file exists
        if not os.path.isfile(flowerlist_filename):
            raise FileNotFoundError(f"Error: Flower list file '{flowerlist_filename}' not found.")

        # Read flower list from the file
        flower_list = read_flower_list(flowerlist_filename)

        num_flowers = int(input("Enter the number of flowers: "))
        dimensions = (int(input("Enter the width of the field: ")), int(input("Enter the height of the field: ")))
        num_pitcher_plants = int(input("Enter the number of pitcher plants: "))
        beehive_position = (random.randint(0, dimensions[0] - 1), random.randint(0, dimensions[1] - 1))

        # Generate the field
        field = generate_field(dimensions, flower_list, num_pitcher_plants, beehive_position, num_flowers)

        # Save the field to a file
        save_field_to_file(field, filename)

        print(f"Field saved to {filename}")

    except ValueError:
        print("Error: Invalid input. Please enter valid integers.")
    except FileNotFoundError as e:
        print(e)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

