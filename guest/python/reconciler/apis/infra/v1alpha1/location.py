from pydantic import BaseModel, Field
from apis.meta.v1.types import clean_description

class Location(BaseModel):
    latitude: str = Field(
        ..., 
        description=clean_description('''
            Latitude of the location in decimal degrees. 
            Valid range is -90.0 to 90.0, where positive values indicate the northern hemisphere 
            and negative values indicate the southern hemisphere.
        '''),
    )
    longitude: str = Field(
        ..., 
        description=clean_description('''
            Longitude of the location in decimal degrees. 
            Valid range is -180.0 to 180.0, where positive values indicate the eastern hemisphere 
            and negative values indicate the western hemisphere.
        '''),
    )
