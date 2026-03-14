import pandas as pd
import argparse
import sys
import matplotlib.pyplot as plt
import numpy as np

# NOTE: What happens when a class is removed from the training set?
COURSES = {
    "Arithmancy",
    "Herbology",
    "Defense Against the Dark Arts",
    "Divination",
    "Muggle Studies",
    "Ancient Runes",
    "History of Magic",
    "Transfiguration",
    "Potions",
    "Care of Magical Creatures",
    "Charms",
    "Flying",
}


def parse_args(args):
    parser = argparse.ArgumentParser(
        description="Process some command-line options.")
    parser.add_argument("file_path", type=str, help="Path to csv file")

    #TODO: Check if provided argument is in COURSES -> Should be ok with parser
    parser.add_argument("-c", 
                        "--course", 
                        type=str, 
                        choices=COURSES,
                        help=f'Configuration option. Must be one of: {", ".join(COURSES)}',
                        required=False)

    args = parser.parse_args()
    return args

def main(args):
    args = parse_args(args)
    df = pd.read_csv(args.file_path)
    # only keep relevant cols for computing histogram
    relevant = list(COURSES) + ["Hogwarts House"]
    df: pd.DataFrame = df.loc[:, relevant]  # keep only relvant columns

    # make a deepcopy of df to plot original and not processed df
    df_original = df.copy()

    if args.course is not None:
        selected = args.course
    else:
        # get std per class per house
        grouped_df = df.groupby(["Hogwarts House"]).std()
        print(f"Std for each class for each House:\n{grouped_df}\n=================")

        # compute coefficient of variation
        cv = grouped_df.std() / grouped_df.mean()  # get variance of std between each house for each house
        print(f"Coefficient of variation for each course :\n{cv.sort_values()}\n=================")

        selected = cv.idxmin()

    distribs = (
        df_original[[selected, "Hogwarts House"]]
        .groupby("Hogwarts House")[selected]
        .apply(lambda x: x.values)
    )

    # Plot the histograms
    plt.hist(distribs["Gryffindor"], bins=10, color='red', alpha=0.5, label='Gryffindor')
    plt.hist(distribs["Hufflepuff"], bins=10, color='yellow', alpha=0.5, label='Hufflepuff')
    plt.hist(distribs["Ravenclaw"], bins=10, color='blue', alpha=0.5, label='Ravenclaw')
    plt.hist(distribs["Slytherin"], bins=10, color='green', alpha=0.5, label='Slytherin')

    # Add labels and legend
    plt.xlabel('Grade')
    plt.ylabel('Frequency')
    plt.title(f'Histogram of {selected}')
    plt.legend()
    # Show the plot
    plt.show()


if __name__ == "__main__":
    main(sys.argv)
