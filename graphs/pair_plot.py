import pandas as pd
import argparse
import sys
import matplotlib.pyplot as plt
import seaborn as sns

COURSES = {
    # "Arithmancy",
    # "Herbology",
    # "Defense Against the Dark Arts",
    # "Divination",
    # "Muggle Studies",
    # "Ancient Runes",
    # "History of Magic",
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

    args = parser.parse_args()

    return args


def main(args):
    args = parse_args(args)
    df = pd.read_csv(args.file_path)

    # put to list to keep order constant
    courses = list(COURSES) + ["Hogwarts House"]
    df = df.loc[:, courses]  # keep only relvant columns
    g = sns.pairplot(df, plot_kws={"s": 3}, hue="Hogwarts House")
    # Customize the axes
    for ax in g.axes.flat:
        # Set x-labels with clear formatting
        ax.set_xlabel(ax.get_xlabel(), fontsize=10, labelpad=10)
        # Set y-labels with clear formatting
        ax.set_ylabel(ax.get_ylabel(), fontsize=10, labelpad=10, rotation=360)
        ax.set_xticks([])  # Remove x-ticks
        ax.set_yticks([])  # Remove y-ticks

    # plt.tight_layout()

    plt.show()


if __name__ == "__main__":
    main(sys.argv)
