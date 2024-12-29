from pydantic import BaseModel, Field, ValidationError, model_validator
from typing import Optional, List, Dict
from apis.meta.v1.types import clean_description, TypeMeta, ObjectMeta, Relationships, Conditions
from apis.infra.v1alpha1.link_types import LinkEndpoint
from apis.infra.v1alpha1.node_types import NodeSpec, Node
from apis.infra.v1alpha1.link_types import Link, LinkSpec
from apis.infra.v1alpha1.physical import AdminState

#Joins a list of items with a delimiter, filtering out any None values
def join(delimiter, items):
  """
  Joins a list of items with a delimiter, filtering out None or empty values.
  """
  return delimiter.join([item for item in items if item])

class TopologyNode(BaseModel):
    name: Optional[str] = Field(
        None,
        description=clean_description('''
            Name define the node name
            // ignored when used in the default section
        '''),
    )

    region: Optional[str] = Field(
        None,
        description=clean_description('''
            Region defines the region this resource is located in
        '''),
    )

    site: Optional[str] = Field(
        None,
        description=clean_description('''
            Site defines the site this resource is located in
        '''),
    )

    rack: Optional[str] = Field(
        None,
        description=clean_description('''
            Rack defines the rack this resource is located in
        '''),
    )

    position: Optional[str] = Field(
        None,
        description=clean_description('''
            Position defines the rack position this resource is located in
        '''),
    )

    labels: Dict[str, str] = Field(
        None,
        description=clean_description('''
            Map of string keys and values that can be used to organize and categorize
	        the resource. 
        ''')
    )

    type: Optional[str] = Field(
        None, 
        description=clean_description('''
            Type names the item with the manufacturer specific type
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


class TopologyLink(BaseModel):
    endpoints: Optional[List[LinkEndpoint]] = Field(
        None,
        max=2,
        min=2,
        description=clean_description('''
            Endpoints define the 2 endpoint identifiers of the link
            // +listType:=atomic
        '''),
    )


class TopologySpec(Relationships):
    defaults: Optional[TopologyNode] = Field(
        None,
        description=clean_description('''
            Defaults define the node defaults
        '''),
    )

    nodes: Optional[List[TopologyNode]] = Field(
        None,
        description=clean_description('''
            Nodes define the node belonging to the topology
        '''),
    )

    links: Optional[List[TopologyLink]] = Field(
        None,
        description=clean_description('''
            Links define the links belonging to the topology
        '''),
    )

class TopologyStatus(Conditions):
    __doc__ = clean_description('''
        Topology defines the observed state of the topology
    ''')

class Topology(TypeMeta):
    __doc__ = clean_description('''
        Topology defines the Schema for the Topology API
    ''')
    
    apiVersion: str = Field("topo.kubenet.dev/v1alpha1")
    
    kind: str = Field("Topology")
    
    metadata: ObjectMeta = Field(...)
    
    spec: Optional[TopologySpec] = Field(
        None,
        description=clean_description('''
            Spec defines the desired state of the Topology.
        '''),
    )
    
    status: Optional[TopologyStatus] = Field(
        None,
        description=clean_description('''
            Status defines the observed state of the Topology.
        '''),
    )

    def _prepare_nodes(self):
        """
        Prepare a list of nodes by merging defaults, renaming keys, and adding additional defaults.
        Returns a list of prepared node dictionaries.
        """
        prepared_nodes = []

        # Extract defaults
        defaults = self.spec.defaults.dict(exclude_unset=True) if self.spec.defaults else {}

        for topo_node in self.spec.nodes:
            # Merge defaults with node-specific data
            node_data = {**defaults, **topo_node.dict(exclude_unset=True)}

            # Rename 'name' to 'node'
            node_data = {("node" if k == "name" else k): v for k, v in node_data.items()}

            # Add default values
            node_data.setdefault("serialNumber", "dummy")
            node_data.setdefault("manufacturer", "Nokia")
            node_data.setdefault("adminState", AdminState.AdminState_Enabled)

            prepared_nodes.append(node_data)

        return prepared_nodes

    def _prepare_links(self):
        """
        Prepare a list of links based on the linkspec
        """
        prepared_links = []

        for topo_link in self.spec.links:
            
            link_data = LinkSpec(
                endpoints=topo_link.endpoints,
                adminState=AdminState.AdminState_Enabled,
            )

            prepared_links.append(link_data)

        return prepared_links

    # Custom validator to check the consistency of multiple fields
    @model_validator(mode="after")
    def validate_links(cls, model):
        node_names = {node.name for node in model.spec.nodes}
        for link in model.spec.links:
            for endpoint in link.endpoints:
                if endpoint.node not in node_names:
                    raise ValueError(f"Endpoint references unknown node: {endpoint.node}")
        return model

    @model_validator(mode="after")
    def validate_nodes(cls, model):
        """
        Validate nodes by using the prepared node data.
        """
        errors = []
        prepared_nodes = model._prepare_nodes()

        for idx, node_data in enumerate(prepared_nodes):
            try:
                NodeSpec.model_validate(node_data)
            except ValidationError as e:
                for error in e.errors():
                    errors.append(
                        {
                            "loc": ("spec", "nodes", idx, *error["loc"]),
                            "msg": error["msg"],
                            "type": error["type"],
                            **({"ctx": error["ctx"]} if "ctx" in error else {}),
                        }
                    )
        if errors:
            raise ValidationError(errors, Topology)

        return model

    def construct_nodes(self):
        """
        Constructs validated NodeSpec objects from the topology spec.
        This assumes the topology has already passed validation.
        """
        nodes = []
        prepared_nodes = self._prepare_nodes()
        
        for node_data in prepared_nodes:
            nodes.append(Node(
                metadata=ObjectMeta(
                    name=".".join([self.metadata.name, node_data.get("node", "")]),
                    namespace=self.metadata.namespace,
                ),
                spec=NodeSpec.model_validate(node_data),
            ))
        return nodes

    def construct_links(self):
        """
        Constructs validated NodeSpec objects from the topology spec.
        This assumes the topology has already passed validation.
        """
        links = []
        prepared_links = self._prepare_links()
        
        for link_data in prepared_links:
            link_spec = LinkSpec.model_validate(link_data)

            links.append(Link(
                metadata=ObjectMeta(
                    name=".".join([self.metadata.name, link_spec.get_named()]),
                    namespace=self.metadata.namespace,
                ),
                spec=link_spec,
            ))
        return links

    def reconcile(self):
        """
        Reconciles the topology data and returns structured nodes and links.
        """
        if not self.spec:
            return {"nodes": [], "links": []}
        
        nodes = self.construct_nodes()
        links = self.construct_links()
        return {"nodes": nodes, "links": links} 