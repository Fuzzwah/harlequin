from __future__ import annotations

from typing import Any, Iterable, Iterator, Literal, Mapping, Type, TypeVar

from .compute import CastOptions
from .types import DataType as DataType
from .types import string as string

class MemoryPool: ...
class Schema: ...
class Field: ...
class NativeFile: ...

class Scalar:
    def as_py(self) -> Any: ...

A = TypeVar("A", bound="_PandasConvertible")

class _PandasConvertible:
    @property
    def type(self) -> DataType: ...  # noqa: A003
    def cast(
        self: A,
        target_type: DataType | None = None,
        safe: bool = True,
        options: CastOptions | None = None,
    ) -> A: ...
    def __getitem__(self, index: int) -> Scalar: ...
    def to_pylist(self) -> list[Any]: ...
    def fill_null(self: A, fill_value: Any) -> A: ...

class Array(_PandasConvertible): ...
class ChunkedArray(_PandasConvertible): ...

class StructArray(Array):
    def flatten(self, memory_pool: MemoryPool | None = None) -> list[Array]: ...

T = TypeVar("T", bound="_Tabular")

class _Tabular:
    @classmethod
    def from_arrays(
        cls: Type[T],
        arrays: list[_PandasConvertible],
        names: list[str] | None = None,
        schema: Schema | None = None,
        metadata: Mapping | None = None,
    ) -> T: ...
    @classmethod
    def from_pydict(
        cls: Type[T],
        mapping: Mapping,
        schema: Schema | None = None,
        metadata: Mapping | None = None,
    ) -> T: ...
    def __getitem__(self, index: int) -> _PandasConvertible: ...
    def __len__(self) -> int: ...
    @property
    def column_names(self) -> list[str]: ...
    @property
    def columns(self) -> list[_PandasConvertible]: ...
    @property
    def num_rows(self) -> int: ...
    @property
    def num_columns(self) -> int: ...
    @property
    def schema(self) -> Schema: ...
    def append_column(
        self: T, field_: str | Field, column: Array | ChunkedArray
    ) -> T: ...
    def column(self, i: int | str) -> _PandasConvertible: ...
    def itercolumns(self) -> Iterator[_PandasConvertible]: ...
    def set_column(
        self: T, i: int, field_: str | Field, column: Array | ChunkedArray
    ) -> T: ...
    def sort_by(
        self: T,
        sorting: str | list[tuple[str, Literal["ascending", "descending"]]],
        **kwargs: Any,
    ) -> T: ...
    def slice(  # noqa: A003
        self: T,
        offset: int = 0,
        length: int | None = None,
    ) -> T: ...
    def to_pylist(self) -> list[dict[str, Any]]: ...

class RecordBatch(_Tabular): ...

class Table(_Tabular):
    @classmethod
    def from_batches(
        cls,
        batches: Iterable[RecordBatch],
        schema: Schema | None = None,
    ) -> "Table": ...
    def to_batches(self) -> list[RecordBatch]: ...

def array(
    obj: Iterable,
    type: DataType | None = None,  # noqa: A002
    mask: Array | None = None,
    size: int | None = None,
    from_pandas: bool | None = None,
    safe: bool = True,
    memory_pool: MemoryPool | None = None,
) -> Array | ChunkedArray: ...
def nulls(
    size: int,
    type: DataType | None = None,  # noqa: A002
    memory_pool: MemoryPool | None = None,
) -> Array: ...
def concat_arrays(
    arrays: Iterable[Array], memory_pool: MemoryPool | None = None
) -> Array: ...
