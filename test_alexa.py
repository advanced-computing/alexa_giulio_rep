# $pip install pytest

import pandas as pd
from project_pt3 import name_cleaning

#test 1
def test_1():
    df = pd.DataFrame({"names": 
                       ["Lady Gaga, Bruno Mars",
                        "ROSÉ, Bruno Mars"
                        ]})
    cleaned_names = name_cleaning(df, "names") 
    assert cleaned_names == ["Lady Gaga", 
                             "Bruno Mars", 
                             "ROSÉ", 
                             "Bruno Mars"
                             ] 

#test 2
def test_2():
    df = pd.DataFrame({"names": 
                       ["Alexa Chan, Giulio Trombin",
                        "Beyoncé, Jay-Z, Aidan Feldman, Roberto Zuniga Valladares", 
                        "Hillary Clinton, Barack Obama"
                        ]})
    cleaned_names = name_cleaning(df, "names") 
    assert cleaned_names == ["Alexa Chan", 
                             "Giulio Trombin",
                             "Beyoncé", 
                             "Jay-Z",
                             "Aidan Feldman", 
                             "Roberto Zuniga Valladares",
                             "Hillary Clinton", 
                             "Barack Obama"
                             ]

#test 3
def test_3():
    df = pd.DataFrame({"names": ["Sabrina Carpenter, Rich Brian, Justin Timberlake",
                                 "Taylor Swift",
                                 "Justin Bieber, bbno$"
                                 ]})
    cleaned_names = name_cleaning(df, "names") 
    assert cleaned_names == ["Sabrina Carpenter", 
                             "Rich Brian", 
                             "Justin Timberlake", 
                             "Taylor Swift", 
                             "Justin Bieber", 
                             "bbno$"
                             ]

#python -m pytest test_alexa.py
