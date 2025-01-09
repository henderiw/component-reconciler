from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from apis.meta.v1.types import clean_description, TypeMeta, ObjectMeta, Conditions, Relationship
from apis.infra.v1alpha1.physical import AdminState
    

class LinkSpec(BaseModel):
    endpoints: List["LinkEndpoint"] = Field(
        ...,
        max=2,
        min=2,
        description=clean_description('''
            Endpoints define the 2 endpoint identifiers of the link
            // +listType:=atomic
        '''),
    )

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

    labels: Optional[Dict[str, str]] = Field(
        None,
        description=clean_description('''
            Map of string keys and values that can be used to organize and categorize
	        the resource. 
        ''')
    )

    def get_named(self):
        """
        Returns a concatenated string representation of all non-None attributes
        of all endpoints in the format: "node=node1,port=1,adaptor=ad1;node=node2,port=2".
        """
        parts = []
        for endpoint in self.endpoints:           
            for key, value in endpoint.dict(exclude_unset=True).items():
                if value is not None:
                    parts.append(f"{value}")
            
        # Join all endpoint strings with a separator
        return ".".join(parts)


class LinkEndpoint(BaseModel):
    node: str = Field(
        ...,
        description=clean_description('''
            Node defines the node on which the endpoint resides
        '''),
    )
    moduleBay: Optional[int] = Field(
        None,
        ge=0,
        description=clean_description('''
            ModuleBay defines the moduleBay on which the endpoint resides
        '''),
    )
    module: Optional[int] = Field(
        None,
        ge=0,
        description=clean_description('''
            Module defines the module on which the endpoint resides
        '''),
    )
    port: int = Field(
        ...,
        ge=0,
        description=clean_description('''
            Port defines the port id on which the endpoint resides
        '''),
    )
    adaptor: Optional[str] = Field(
        None,
        description=clean_description('''
            Adaptor defines the adaptor on which the endpoint resides
        '''),
    )
    endpoint: int = Field(
        None,
        ge=0,
        description=clean_description('''
            Endpoint defines the endpoint id on which the endpoint resides
        '''),
    )
    

class LinkStatus(Conditions):
    __doc__ = clean_description('''
        A Node represents a fundamental unit that implements compute, storage, and/or networking within your environment.
        Nodes can embody physical, virtual, or containerized entities, offering versatility in deployment options to suit
        diverse infrastructure requirements.
        Nodes are logically organized within racks and sites/regions, establishing a hierarchical structure for efficient
        resource management and organization. Additionally, Nodes are associated with nodeGroups, facilitating centralized
        management and control within defined administrative boundaries.
        Each Node is assigned a provider, representing the entity responsible for implementing the specifics of the Node.
    ''')
    

class Link(TypeMeta):
    __doc__ = clean_description('''
        A Node represents a fundamental unit that implements compute, storage, and/or networking within your environment.
        Nodes can embody physical, virtual, or containerized entities, offering versatility in deployment options to suit
        diverse infrastructure requirements.
        Nodes are logically organized within racks and sites/regions, establishing a hierarchical structure for efficient
        resource management and organization. Additionally, Nodes are associated with nodeGroups, facilitating centralized
        management and control within defined administrative boundaries.
        Each Node is assigned a provider, representing the entity responsible for implementing the specifics of the Node.
    ''')
    
    apiVersion: str = Field("infra.kuid.dev/v1alpha1")
    
    kind: str = Field("Link")
    
    metadata: ObjectMeta = Field(...)
    
    spec: Optional[LinkSpec] = Field(
        None,
        description=clean_description('''
            Spec defines the desired state of the Node.
        '''),
    )
    
    status: Optional[LinkStatus] = Field(
        None,
        description=clean_description('''
            Status defines the observed state of the Node.
        '''),
    )