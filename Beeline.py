#Author: Prayash Das
#Date: 02/29/2024
#Description: This program contains the main function, imports the functionalities from the BeeFunctions.py file required
# to play the Beeline game.
from BeeFunctions import load_flower_list, create_field, copy_field, game_intro, check_bee_area, print_field
def main():
    '''
    The main function where all the functions are being called from the BeeFunctions.py file, handles exception correctly,
    repeatedly loops until the user has no worker bees left or harvests enough plowers, displays information related to
    number of bees and harvested flowers, and correctly informs the user if they have won or lost based on the number of
    worker bees and amount of pollen harvested.
    :return:
    '''
    try:
        # Load flower list file
        flower_info_dict = load_flower_list()

        # Create the hidden field (may raise TypeError)
        try:
            hidden_field = create_field(flower_info_dict)
        except TypeError as e:
            print(f"Error: {e}")
            exit(-1)

        # Make a copy of the hidden field to create the visible field
        visible_field = copy_field(hidden_field)

        # Game variables
        num_scouts = 5
        num_workers = 5
        harvested_pollen = 0
        pollen_needed_to_win = 20

        # Output introductory information
        game_intro(flower_info_dict, num_scouts, num_workers, pollen_needed_to_win)

        # Main game loop
        while num_workers > 0 and harvested_pollen < pollen_needed_to_win:
            print(f"You have {num_scouts} scout bees left, {num_workers} worker bees left, and have harvested {harvested_pollen} units of pollen.")
            print("H is the hive, U is a used flower")

            # Display the visible field
            print_field(visible_field)

            # Prompt user for bee type
            bee_type = input("What type of bee would you like to send out (S for scout, W for worker):").upper()

            # Check user input
            if bee_type not in ['S', 'W']:
                print("This is not a valid bee type!")
                continue

            # Send out the bee and update variables
            if bee_type == 'S':
                if num_scouts > 0:
                    # Prompt user for coordinates
                    print("Where would you like to send the bee")
                    try:
                        x = int(input("0 <= x < 10:"))
                        y = int(input("0 <= y < 10:"))
                    except ValueError:
                        print("Invalid coordinates. Please enter valid integers.")
                        continue
                    num_scouts -= 1
                    print("Sending out the scout")
                    harvested_pollen += check_bee_area(hidden_field, visible_field, x, y, 'scout', flower_info_dict)
                else:
                    print("You do not have any more scout bees!")
            elif bee_type == 'W':
                if num_workers > 0:
                    # Prompt user for coordinates
                    print("Where would you like to send the bee")
                    try:
                        x = int(input("0 <= x < 10:"))
                        y = int(input("0 <= y < 10:"))
                    except ValueError:
                        print("Invalid coordinates. Please enter valid integers.")
                        continue
                    num_workers -= 1
                    print("Sending out the worker")
                    harvested_pollen += check_bee_area(hidden_field, visible_field, x, y, 'worker', flower_info_dict)
                else:
                    print("You do not have any more worker bees!")

        # End of game
        if harvested_pollen >= pollen_needed_to_win:
            print("Good work! You made enough honey for the hive. Just in time for winter!")
        else:
            print("Oh no! You have not made enough honey. You have been deposed as queen.")
    except Exception as e:
        print(f"Error occurred - {e}")


if __name__ == "__main__":
    main()
