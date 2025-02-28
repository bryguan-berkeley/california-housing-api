from pydantic import BaseModel, Field, field_validator
from typing import List

class Pydantic_Single_Input(BaseModel):
    MedInc: float = Field(..., description = 'Median income in the block group')
    HouseAge: float = Field(..., description = 'Median house age in the block group')
    AveRooms: float = Field(..., description = 'Average number of rooms per household')
    AveBedrms: float = Field(..., description = 'Average number of bedrooms per household')
    Population: float = Field(..., description = 'Block group population')
    AveOccup: float = Field(..., description = 'Average number of household members')
    Latitude: float = Field(..., description = 'Block group latitude')
    Longitude: float = Field(..., description = 'Block group longitude')

    @field_validator('MedInc', 'HouseAge', 'AveRooms', 'AveBedrms', 'Population', 'AveOccup', mode = 'after')
    @classmethod
    def check_positive(cls, value, info):
        if value < 0:
            raise ValueError(f'{info.field_name} Must Be Non-Negative')
        return value

    @field_validator('Latitude', mode = 'after')
    @classmethod
    def validate_latitude(cls, value):
        if not (-90 <= value <= 90):
            raise ValueError('Latitude Must Be Between -90 and 90')
        return value

    @field_validator('Longitude', mode = 'after')
    @classmethod
    def validate_longitude(cls, value):
        if not (-180 <= value <= 180):
            raise ValueError('Longitude Must Be Between -180 and 180')
        return value

    def vectorize(self):
        return [[
            self.MedInc, self.HouseAge, self.AveRooms, self.AveBedrms, self.Population, self.AveOccup, self.Latitude, self.Longitude
        ]]

class Pydantic_Multiple_Inputs(BaseModel):
    houses: List[Pydantic_Single_Input]

    def vectorize(self):
        return [
            [
                house.MedInc, house.HouseAge, house.AveRooms, house.AveBedrms, house.Population, house.AveOccup, house.Latitude, house.Longitude
            ]
            for house in self.houses
        ]

class Pydantic_Single_Output(BaseModel):
    prediction: float

class Pydantic_Multiple_Outputs(BaseModel):
    predictions: List[float]
