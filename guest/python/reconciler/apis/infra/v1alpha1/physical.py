from pydantic import BaseModel, Field
from apis.meta.v1.types import clean_description, Relationship
from typing import List, Dict, Optional
from datetime import datetime
from enum import Enum

class PhysicalModel(BaseModel):
    serialNumber: str = Field(
        ..., 
        description=clean_description('''
            Serial number defines the serial number of the item
        '''),
    )
    manufacturer: str = Field(
        ..., 
        description=clean_description('''
            Manufacturer name who produced the item
        '''),
    )
    purshaseDate: Optional[datetime] = Field(
        None, 
        description=clean_description('''
            PurchaseDate defines the date when the item was purchased
        '''),
    )

    type: str = Field(
        ..., 
        description=clean_description('''
            Type names the item with the manufacturer specific type
        '''),
    )

class AdminState(Enum):
    AdminState_Enabled = 'enable'
    AdminState_Maintenance = 'maintenance'
    AdminState_Decomissioned = 'decomissioned'
    AdminState_Standby = 'standby'

class PhysicalInfraModel(PhysicalModel):

    adminState: AdminState = Field(
        ...,
        description=clean_description('''
            AdminState defines the administrative state of the resource
        '''),
    )

    relationships: Optional[List[Relationship]] = Field(
        None,
        description=clean_description('''
            Relationships define the relationships of the resource
        '''),
    )

    labels: Dict[str, str] = Field(
        None,
        description=clean_description('''
            Map of string keys and values that can be used to organize and categorize
	        the resource. 
        ''')
    )