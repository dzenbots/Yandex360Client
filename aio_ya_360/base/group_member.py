import enum
from dataclasses import dataclass


class Ya360GroupMemberGroupMemberType(enum.Enum):
    user = 'user'
    group = 'group'
    department = 'department'


@dataclass
class Ya360GroupMember:
    id: str
    type: str

    @staticmethod
    def from_json(data: dict):
        return Ya360GroupMember(
            id=data.get('id'),
            type=Ya360GroupMemberGroupMemberType.group.value if data.get(
                'type') == 'group' else Ya360GroupMemberGroupMemberType.department.value if data.get(
                'type') == 'department' else Ya360GroupMemberGroupMemberType.user.value
        )
