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



class Reconciler(Protocol):

    @abstractmethod
    def reconcile(self, object: str) -> str:
        """
        The `reconcile` function is the main entry point for the reconciler.
        It takes a JSON input and returns a JSON output or an error.
        """
        raise NotImplementedError

