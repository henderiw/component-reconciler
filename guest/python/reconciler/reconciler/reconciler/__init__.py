"""
Represents the reconciler world
"""
from typing import TypeVar, Generic, Union, Optional, Protocol, Tuple, List, Any, Self
from types import TracebackType
from enum import Flag, Enum, auto
from dataclasses import dataclass
from abc import abstractmethod
import weakref

from .types import Result, Ok, Err, Some


def get(name: str) -> str:
    raise NotImplementedError


@dataclass
class ReconcileResult:
    """
    import wasi:cli/stdout@0.2.0;
    import wasi:random/random@0.2.0;
    import wasi:cli/environment@0.2.0;
    import wasi:cli/stderr@0.2.0;
    import wasi:cli/stdin@0.2.0;
    import wasi:clocks/monotonic-clock@0.2.0;
    import wasi:clocks/wall-clock@0.2.0;
    import wasi:filesystem/types@0.2.0;
    import wasi:filesystem/preopens@0.2.0;
    """
    requeue: bool
    requeue_after: int
    object: str

@dataclass
class ReconcileError:
    code: int
    message: str

class Reconciler(Protocol):

    @abstractmethod
    def reconcile(self, object: str) -> ReconcileResult:
        """
        The `reconcile` function is the main entry point for the reconciler.
        It takes a JSON input and returns a JSON output or an error.
        
        Raises: `reconciler.types.Err(reconciler.imports.ReconcileError)`
        """
        raise NotImplementedError

