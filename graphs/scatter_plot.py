import pandas as pd
import argparse
import sys
import matplotlib.pyplot as plt
import numpy as np

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
    parser.add_argument("-c", 
                        "--course", 
                        type=str, 
                        choices=COURSES,
                        help=f'Provides highest correlated course with course provided as argument. Must be one of: {", ".join(COURSES)}',
                        required=False)

    parser.add_argument("-c2", 
                        "--course2", 
                        type=str, 
                        nargs=2,
                        choices=COURSES,
                        help=f'Provides plot of the 2 courses passed as option. Must be one of: {", ".join(COURSES)}',
                        required=False)

    args = parser.parse_args()

    return args


def main(args):
    args = parse_args(args)
    df = pd.read_csv(args.file_path)

    # put to list to keep order constant
    courses = list(COURSES)
    df = df.loc[:, courses]  # keep only relvant columns

    figure, axis = plt.subplots(1, 2)
    # to find max, we need to remove lower triangular + diagonal
    # holds all correlations pairs, from highest to lowest
    corr_m = df.corr()
    sol = (corr_m.abs()
        .where(np.triu(corr_m, k=1).astype(bool))
        .stack()
        .sort_values(ascending=False)
    )
    print(type(sol))

    for index, value in sol.items():
        print(f"{index}: {value}")

    # we select the highest pair f1 and f2 in which args.course is present
    if args.course: 
        f1, f2 = next(index for index in sol.index if args.course in index)
    elif args.course2:
        f1, f2 = tuple(args.course2)
    else:
        # we select the highest index overall
        f1, f2 = sol.index[0]

    axis[0].scatter(df[f1], df[f2], s=1)
    correlation = df[f1].corr(df[f2])
    axis[0].set_title(f'Correlation {correlation:.3f}')

    axis[0].set_xlabel(f1)
    axis[0].set_ylabel(f2)

    axis[1].matshow(df.corr())
    plt.colorbar(axis[1].matshow(df.corr()), ax=axis[1], fraction=0.046, pad=0.04)

    axis[1].tick_params(axis='x', which='major', pad=15)
    axis[1].xaxis.set_ticks([i for i in range(0, len(courses))])
    axis[1].yaxis.set_ticks([i for i in range(0, len(courses))])
    axis[1].set_xticklabels(courses, rotation=90)
    axis[1].set_yticklabels(courses)
    # plt.matshow(df.corr())
    plt.subplots_adjust(wspace=0.7)
    plt.show()


if __name__ == "__main__":
    main(sys.argv)
