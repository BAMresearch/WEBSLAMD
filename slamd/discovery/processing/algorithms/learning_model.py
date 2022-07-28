from dataclasses import dataclass
import pandas as pd


@dataclass
class UserInput:
    curiosity: float = 1.0
    model: str = 'lolo Random Forest'


class ModelData:

    def __init__(self, user_input, curiosity=1.2000):
        self.curiosity = curiosity
        self.dataframe = None  # pd.read
        self.user_input = user_input


class LearningModel:

    @classmethod
    def run(cls):
        # Run the model on the given dataset
        print("Running....")
        user_input = UserInput(curiosity=2.0)
        data = ModelData(user_input=user_input)
        return []


if __name__ == "__main__":
    LearningModel.run()
