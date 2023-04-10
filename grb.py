import pandas as pd


class GRB:
    df = pd.read_csv("data/gbmdatacleaned.csv", index_col=0)

    def __init__(self, name):
        self.name = name
        self.number = self.name[3:]
        self.year = self.get_year()
        self.ra, self.dec = self.get_radec()

    def get_year(self):
        return int(GRB.df[GRB.df["name"] == self.name]["trigger_time"].iloc[0][:4])

    def get_radec(self):
        row = GRB.df[GRB.df["name"] == self.name]
        return row["ra_val"].values[0], row["dec_val"].values[0]

    def __str__(self):
        return f"Name : {self.name} Year : {self.year} RA : {self.ra:.2f} DEC : {self.dec:.2f}"
