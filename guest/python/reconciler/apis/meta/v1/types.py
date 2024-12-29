from pydantic import BaseModel, Field, conint
from typing import Dict, List, Literal, Optional
from datetime import datetime
from enum import Enum

# Define Int64 as a constrained integer
Int64 = conint(ge=-2**63, le=2**63 - 1)

def clean_description(description: str) -> str:
    """Strips leading and trailing whitespace and condenses all internal whitespace to a single space."""
    return ' '.join(description.strip().split())

class Condition(BaseModel):
    lastTransitionTime: datetime = Field(
        description=clean_description('''
            lastTransitionTime is the last time the condition
            transitioned from one status to another. This should be when
            the underlying condition changed.  If that is not known, then
            using the time when the API field changed is acceptable.
        '''),
    )
    message: str = Field(
        description=clean_description('''
            message is a human readable message indicating
            details about the transition. This may be an empty string.
        '''),
        max_length=32768,
    )
    observedGeneration: int = Field(
        None,
        description=clean_description('''
            observedGeneration represents the .metadata.generation
            that the condition was set based upon. For instance, if .metadata.generation
            is currently 12, but the .status.conditions[x].observedGeneration
            is 9, the condition is out of date with respect to the current
            state of the instance.
        '''),
        min=0,
        format="int64",
    )
    reason: str = Field(
        description=clean_description('''
            reason contains a programmatic identifier indicating
            the reason for the condition's last transition. Producers
            of specific condition types may define expected values and
            meanings for this field, and whether the values are considered
            a guaranteed API. The value should be a CamelCase string.
            This field may not be empty.
        '''),
        max_length=1024,
        min_length=1,
        pattern="^[A-Za-z]([A-Za-z0-9_,:]*[A-Za-z0-9_])?$",
    )
    status: Literal["True", "False", "unknown"] = Field(
        description=clean_description('''
            status of the condition, one of True, False, Unknown.
        '''),
    )
    type: str = Field(
        description=clean_description('''
            type of condition in CamelCase or in foo.example.com/CamelCase.
            --- Many .condition.type values are consistent across resources
            like Available, but because arbitrary conditions can be useful
            (see .node.status.conditions), the ability to deconflict is
            important. The regex it matches is (dns1123SubdomainFmt/)?(qualifiedNameFmt)
        '''),
        max_length=316,
        #pattern="^([a-z0-9]([-a-z0-9]*[a-z0-9])?(\.[a-z0-9]([-a-z0-9]*[a-z0-9])?)*/)?(([A-Za-z0-9][-A-Za-z0-9_.]*)?[A-Za-z0-9])$",
    )

class Conditions(BaseModel):
    conditions: List[Condition] = Field(
        None,
        description=clean_description('''
            Conditions define a list of conditions related tot he resource
        '''),
        json_schema_extra={
            "x-kubernetes-list-map-keys": ["type"],
            "x-kubernetes-list-type": "map"
        },
    )


class Relationship(BaseModel):
    apiVersion: str = Field(
        ...,
        description=clean_description('''
            APIversion defines the apiVersion of the referent.
        ''')
    )

    kind: str = Field(
        ...,
        description=clean_description('''
            Kind define the kind of the referent.
        ''')
    )

    name: str = Field(
        ...,
        description=clean_description('''
            Name defines the name of the referent.
        ''')
    )

    uid: Optional[str] = Field(
        None,
        description=clean_description('''
            UID defines the uid of the referent.
        ''')
    )

    type: str = Field(
        ...,
        description=clean_description('''
            Type define the type of relationship.
        ''')
    )

    labels: Dict[str, str] = Field(
        None,
        description=clean_description('''
            Map of string keys and values that can be used to organize and categorize
	        (scope and select) objects. 
        ''')
    )


class Relationships(BaseModel):
    relationships: List[Relationship] = Field(None)

class OwnerReference(BaseModel):
    apiVersion: str = Field(
        ...,
        description=clean_description('''
            API version of the referent.
        ''')
    )

    kind: str = Field(
        ...,
        description=clean_description('''
            Kind of the referent.
        ''')
    )

    name: str = Field(
        ...,
        description=clean_description('''
            Name of the referent.
        ''')
    )

    uid: str = Field(
        ...,
        description=clean_description('''
            UID of the referent.
        ''')
    )

    controller: bool = Field(
        None,
        description=clean_description('''
            indication of a managing controller being the owner.
        ''')
    )

    blockOwnerDeletion: bool = Field(
        None,
        description=clean_description('''
            If true, AND if the owner has the "foregroundDeletion" finalizer, then
            the owner cannot be deleted from the key-value store until this
            reference is removed.
            See https://kubernetes.io/docs/concepts/architecture/garbage-collection/#foreground-deletion
            for how the garbage collector interacts with this field and enforces the foreground deletion.
            Defaults to false.
            To set this field, a user needs "delete" permission of the owner,
            otherwise 422 (Unprocessable Entity) will be returned.
            +optional
        ''')
    )


class OwnerReferences(BaseModel):
    ownerReferences: List[OwnerReference] = Field(
        None,
        description=clean_description('''
            List of objects depended by this object. If ALL objects in the list have
            been deleted, this object will be garbage collected. If this object is managed by a controller,
            then an entry in this list will point to this controller, with the controller field set to true.
            There cannot be more than one managing controller.
            +optional
            +patchMergeKey=uid
            +patchStrategy=merge
            +listType=map
            +listMapKey=uid
        ''')
    )

class ManagedFieldsOperationType(Enum):
    ManagedFieldsOperationApply = 'Apply'
    ManagedFieldsOperationUpdate = 'Update'

class ManagedFieldsEntry(BaseModel):
    manager: str = Field(
        ...,
        description=clean_description('''
            Manager is an identifier of the workflow managing these fields.
        ''')
    )

    operation: ManagedFieldsOperationType = Field(
        ...,
        description=clean_description('''
           Operation is the type of operation which lead to this ManagedFieldsEntry being created.
        ''')
    )

    apiVersion: str = Field(
        ...,
        description=clean_description('''
            APIVersion defines the version of this resource that this field set
            applies to. The format is "group/version" just like the top-level
            APIVersion field. It is necessary to track the version of a field
            set because it cannot be automatically converted.
        ''')
    )

    time: datetime = Field(
        None,
        description=clean_description('''
            Time is the timestamp of when the ManagedFields entry was added. The
            timestamp will also be updated if a field is added, the manager
            changes any of the owned fields value or removes a field. The
            timestamp does not update when a field is removed from the entry
            because another manager took it over.
            +optional
        ''')
    )

    fieldsType: str = Field(
        None,
        description=clean_description('''
            FieldsV1 stores a set of fields in a data structure like a Trie, in JSON format.
            
            Each key is either a '.' representing the field itself, and will always map to an empty set,
            or a string representing a sub-field or item. The string will follow one of these four formats:
            'f:<name>', where <name> is the name of a field in a struct, or key in a map
            'v:<value>', where <value> is the exact json formatted value of a list item
            'i:<index>', where <index> is position of a item in a list
            'k:<keys>', where <keys> is a map of  a list item's key fields to their unique values
            If a key maps to an empty Fields value, the field that key represents is part of the set.
            
            The exact format is defined in sigs.k8s.io/structured-merge-diff
            +protobuf.options.(gogoproto.goproto_stringer)=false
        ''')
    )

    fieldsV1: Optional[Dict] = Field(
        None,
        description=clean_description('''
            FieldsV1 stores a set of fields in a data structure like a Trie, in JSON format.
            
            Each key is either a '.' representing the field itself, and will always map to an empty set,
            or a string representing a sub-field or item. The string will follow one of these four formats:
            'f:<name>', where <name> is the name of a field in a struct, or key in a map
            'v:<value>', where <value> is the exact json formatted value of a list item
            'i:<index>', where <index> is position of a item in a list
            'k:<keys>', where <keys> is a map of  a list item's key fields to their unique values
            If a key maps to an empty Fields value, the field that key represents is part of the set.
            
            The exact format is defined in sigs.k8s.io/structured-merge-diff
            +protobuf.options.(gogoproto.goproto_stringer)=false
        ''')
    )

    subresource: str = Field(
        None,
        description=clean_description('''
            Subresource is the name of the subresource used to update that object, or
            empty string if the object was updated through the main resource. The
            value of this field is used to distinguish between managers, even if they
            share the same name. For example, a status update will be distinct from a
            regular update using the same manager name.
            Note that the APIVersion field is not related to the Subresource field and
            it always corresponds to the version of the main resource.
        ''')
    )


class ManagedFields(BaseModel):
    managedFields: List[ManagedFieldsEntry] = Field(
         None,
        description=clean_description('''
            ManagedFields maps workflow-id and version to the set of fields
            that are managed by that workflow. This is mostly for internal
            housekeeping, and users typically shouldn't need to set or
            understand this field. A workflow can be the user's name, a
            controller's name, or the name of a specific apply path like
            "ci-cd". The set of fields is always in the version that the
            workflow used when modifying the object.
            +listType=atomic
        ''')
    )

class Finalizers(BaseModel):
    finalizers: List[str] = Field(
        None,
        description=clean_description('''
            Must be empty before the object is deleted from the registry. Each entry
            is an identifier for the responsible component that will remove the entry
            from the list. If the deletionTimestamp of the object is non-nil, entries
            in this list can only be removed.
            Finalizers may be processed and removed in any order.  Order is NOT enforced
            because it introduces significant risk of stuck finalizers.
            finalizers is a shared field, any actor with permission can reorder it.
            If the finalizer list is processed in order, then this can lead to a situation
            in which the component responsible for the first finalizer in the list is
            waiting for a signal (field value, external system, or other) produced by a
            component responsible for a finalizer later in the list, resulting in a deadlock.
            Without enforced ordering finalizers are free to order amongst themselves and
            are not vulnerable to ordering changes in the list.
            +optional
            +patchStrategy=merge
            +listType=set
        ''')
    )

class Labels(BaseModel):
    labels: Dict[str, str] = Field(
        None,
        description=clean_description('''
            Map of string keys and values that can be used to organize and categorize
	        (scope and select) objects. May match selectors of replication controllers
	        and services.
	        More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/labels
        ''')
    )

class Annotations(BaseModel):
    annotations: Dict[str, str] = Field(
        None,
        description=clean_description('''
            Annotations is an unstructured key value map stored with a resource that may be
	        set by external tools to store and retrieve arbitrary metadata. They are not
	        queryable and should be preserved when modifying objects.
	        More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/annotations
        ''')
    )

class ObjectMeta(BaseModel):
    name: str = Field(
        None, 
        description=clean_description('''
            Name must be unique within a namespace. Is required when creating resources, although
	        some resources may allow a client to request the generation of an appropriate name
	        automatically. Name is primarily intended for creation idempotence and configuration
	        definition.
            Immutable
        '''),
    )
    namespace: Optional[str] = Field(
        None,
        description=clean_description('''
            Namespace defines the space within which each name must be unique. An empty namespace is
	        equivalent to the "default" namespace, but "default" is the canonical representation.
	        Not all objects are required to be scoped to a namespace - the value of this field for
	        those objects will be empty.
            Must be a DNS Label
            Immutable
            Read-Only
        ''')
    )

    uid: str = Field(
        None,
        description=clean_description('''
            UID is the unique in time and space value for this object. Generate by the server.
            Immutable.
            Read-Only
        ''')
    )

    resourceVersion: str = Field(
        None,
        description=clean_description('''
            An opaque value that represents the internal version of this object that can
            be used by clients to determine when objects have changed. May be used for optimistic
            concurrency, change detection, and the watch operation on a resource or set of resources.
            clients must treat these values as opaque and passed unmodified back to the server.
            They may only be valid for a particular resource or set of resources.
            Populated by the system
            Read-Only
        ''')
    )

    generation: Int64 = Field(
        None,
        description=clean_description('''
            A sequence number representing a specific generation of the desired state.
	        Populated by the system. 
            Read-only.
        ''')
    ) 

    creationTimestamp: datetime = Field(
        None,
        description=clean_description('''
            CreationTimestamp is a timestamp representing the server time when this object was
	        created. It is not guaranteed to be set in happens-before order across separate operations.
	        Clients may not set this value. It is represented in RFC3339 form and is in UTC.
            Populated by the system. 
            Read-only.
            Null for list
        ''')
    )

    deletionTimestamp: datetime = Field(
        None,
        description=clean_description('''
            DeletionTimestamp is RFC 3339 date and time at which this resource will be deleted. This
	        field is set by the server when a graceful deletion is requested by the user, and is not
	        directly settable by a client. The resource is expected to be deleted (no longer visible
	        from resource lists, and not reachable by name) after the time in this field, once the
	        finalizers list is empty. As long as the finalizers list contains items, deletion is blocked.
	        Once the deletionTimestamp is set, this value may not be unset or be set further into the
	        future, although it may be shortened or the resource may be deleted prior to this time.
	        For example, a user may request that a pod is deleted in 30 seconds. The Kubelet will react
	        by sending a graceful termination signal to the containers in the pod. After that 30 seconds,
	        the Kubelet will send a hard termination signal (SIGKILL) to the container and after cleanup,
	        remove the pod from the API. In the presence of network partitions, this object may still
	        exist after this timestamp, until an administrator or automated process can determine the
	        resource is fully terminated.
	        If not set, graceful deletion of the object has not been requested.
            Read-only.
            Null for list
        ''')
    )

    labels: Dict[str, str] = Field(
        None,
        description=clean_description('''
            Map of string keys and values that can be used to organize and categorize
	        (scope and select) objects. May match selectors of replication controllers
	        and services.
	        More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/labels
        ''')
    )

    annotations: Dict[str, str] = Field(
        None,
        description=clean_description('''
            Annotations is an unstructured key value map stored with a resource that may be
	        set by external tools to store and retrieve arbitrary metadata. They are not
	        queryable and should be preserved when modifying objects.
	        More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/annotations
        ''')
    )

    finalizers: List[str] = Field(
        None,
        description=clean_description('''
            Must be empty before the object is deleted from the registry. Each entry
            is an identifier for the responsible component that will remove the entry
            from the list. If the deletionTimestamp of the object is non-nil, entries
            in this list can only be removed.
            Finalizers may be processed and removed in any order.  Order is NOT enforced
            because it introduces significant risk of stuck finalizers.
            finalizers is a shared field, any actor with permission can reorder it.
            If the finalizer list is processed in order, then this can lead to a situation
            in which the component responsible for the first finalizer in the list is
            waiting for a signal (field value, external system, or other) produced by a
            component responsible for a finalizer later in the list, resulting in a deadlock.
            Without enforced ordering finalizers are free to order amongst themselves and
            are not vulnerable to ordering changes in the list.
            +optional
            +patchStrategy=merge
            +listType=set
        ''')
    )

    ownerReferences: List[OwnerReference] = Field(
        None,
        description=clean_description('''
            List of objects depended by this object. If ALL objects in the list have
            been deleted, this object will be garbage collected. If this object is managed by a controller,
            then an entry in this list will point to this controller, with the controller field set to true.
            There cannot be more than one managing controller.
            +optional
            +patchMergeKey=uid
            +patchStrategy=merge
            +listType=map
            +listMapKey=uid
        ''')
    )

    managedFields: List[ManagedFieldsEntry] = Field(
         None,
        description=clean_description('''
            ManagedFields maps workflow-id and version to the set of fields
            that are managed by that workflow. This is mostly for internal
            housekeeping, and users typically shouldn't need to set or
            understand this field. A workflow can be the user's name, a
            controller's name, or the name of a specific apply path like
            "ci-cd". The set of fields is always in the version that the
            workflow used when modifying the object.
            +listType=atomic
        ''')
    )

class TypeMeta(BaseModel):
    apiVersion: str = Field(
        None, 
        description=clean_description('''
            APIVersion defines the versioned schema of this representation of an object.
            Servers should convert recognized schemas to the latest internal value, and may
            reject unrecognized values. More info:
            https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources
        '''),
    )
    kind: str = Field(
        None,
        description=clean_description('''
            Kind is a string value representing the REST resource this object represents.
            Servers may infer this from the endpoint the client submits requests to.
            Cannot be updated. In CamelCase. More info:
            https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds
        ''')
    )