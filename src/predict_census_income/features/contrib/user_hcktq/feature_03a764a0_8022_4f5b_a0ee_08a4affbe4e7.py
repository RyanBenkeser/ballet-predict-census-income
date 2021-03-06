from ballet import Feature
from ballet.eng import BaseTransformer, NullFiller
from ballet.eng.external import SimpleImputer, StandardScaler
import pandas as pd
import numpy as np


class MedianIncomeForGroup(BaseTransformer):
    def __init__(self, targetcol="PINCP"):
        self.targetcol = targetcol

    def fit(self, X, y=None):
        if not isinstance(y, (pd.Series, pd.DataFrame)):
            y = pd.Series(y.ravel(), name=self.targetcol)
        self.income_map_ = (
            X.to_frame().join(y).groupby(by=X.name)[self.targetcol].median().to_dict()
        )
        return self

    def transform(self, X):
        return X.map(self.income_map_)


input = "ANC1P"
transformer = [
    NullFiller(replacement=-1),  # don't appear to be any nans
    MedianIncomeForGroup(),
    SimpleImputer(),
    np.log1p,
]  # TODO - function, transformer-like, or list thereof
name = "log ancestry income"  # TODO - str
description = "replace ancestry with log median income for that ancestry in training data"  # TODO - str
feature = Feature(input, transformer, name=name, description=description)
