from pydantic import BaseModel, Field
from typing import Optional, List
from apis.meta.v1.types import clean_description, TypeMeta, ObjectMeta, Conditions
from apis.infra.v1alpha1.physical import PhysicalInfraModel
from apis.infra.v1alpha1.location import Location

class NodeSpec(PhysicalInfraModel):
    node: str = Field(
        ...,
        description=clean_description('''
            Node defines the short name of the node
        '''),
    )

    location: Optional[Location] = Field(
        None,
        description=clean_description('''
            Location defines the location information where this resource is located
	        in lon/lat coordinates
        '''),
    )

    provider: Optional[str] = Field(
        None,
        description=clean_description('''
            Provider defines the software provider inplementing the resource
        '''),
    )

    version: Optional[str] = Field(
        None,
        description=clean_description('''
            Version defines the version of the provider implementing the resource
        '''),
    )

class NodeStatus(Conditions):
    systemID: str = Field(
        None,
        description=clean_description('''
            System ID define the unique system id of the node
        '''),
    )

class Node(TypeMeta):
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
    
    kind: str = Field("Node")
    
    metadata: ObjectMeta = Field(...)
    
    spec: Optional[NodeSpec] = Field(
        None,
        description=clean_description('''
            Spec defines the desired state of the Node.
        '''),
    )
    
    status: Optional[NodeStatus] = Field(
        None,
        description=clean_description('''
            Status defines the observed state of the Node.
        '''),
    )