import enum
from dataclasses import dataclass
from typing import Optional


class Ya360OrderType(enum.Enum):
    by_id = 'id'
    by_name = 'name'


@dataclass
class Ya360RequestParams:
    page: Optional[int] = None
    per_page: Optional[int] = None
    parentID: Optional[str] = None
    pageToken: Optional[str] = None
    pageSize: Optional[int] = None
    orderBy: Optional[Ya360OrderType] = None

    def to_json(self) -> dict:
        result = dict()
        if self.page is not None:
            result['page'] = self.page
        if self.per_page is not None:
            result['perPage'] = self.per_page
        if self.parentID is not None:
            result['parentID'] = self.parentID
        if self.orderBy is not None:
            result['orderBy'] = self.orderBy.value
        if self.pageToken is not None:
            result['pageToken'] = self.pageToken
        if self.pageSize is not None:
            result['pageSize'] = self.pageSize
        return result
