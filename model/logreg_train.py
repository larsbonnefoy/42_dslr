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


class SoftMaxReg():
    def stable_softmax(X):
        exps = np.exp(X - np.max(X))
        return exps / np.sum(exps)

    def __init__(self, c, f, lr):
        """
        c is the number of classes
        f is the number of features
        lr is the learning rate
        """
        self.w = np.random.random((f, c))
        self.b = np.random.random()
        pass


def parse_args(args):
    parser = argparse.ArgumentParser(description="Process some command-line options.")

    parser.add_argument("file_path", type=str, help="Path to csv file")

    args = parser.parse_args()

    return args


def encode_labels(label: str):
    """
    One-hot encoding of labels
    """
    vector = np.zeros(4, dtype=int)
    match label:
        case "Ravenclaw":
            vector[0] = 1
        case "Slytherin":
            vector[1] = 1
        case "Gryffindor":
            vector[2] = 1
        case "Hufflepuff":
            vector[3] = 1
        case _ as error:
            raise ValueError(f"{error} does not exist")
    return vector


def sigmoid(x, theta):
    z = np.dot(x, theta)
    return 1.0 / (1 + np.exp(-z))


"""
1. features => remove high correlation, could use VIF
2. onehot enc
"""
def main(args):
    args = parse_args(args)
    df = pd.read_csv(args.file_path)
    df["Best Hand"] = df["Best Hand"].apply(lambda hand: 1 if hand == "Right" else 0)
    df["Hogwarts House"] = df["Hogwarts House"].apply(
        lambda house: encode_labels(house)
    )
    print(df.head())


if __name__ == "__main__":
    main(sys.argv)
