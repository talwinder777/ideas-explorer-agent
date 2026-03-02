from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class RawItem:
    source: str
    source_type: str
    title: str
    url: str
    text: str = ""
    author: str | None = None
    created_at: str | None = None
    score: int | None = None
    comments_count: int | None = None
    tags: list[str] = field(default_factory=list)
    extra: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
