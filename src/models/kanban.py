from dataclasses import dataclass
from typing import Optional

@dataclass
class KanbanTask:
    id: Optional[int]
    title: str
    description: str
    category: str
    priority: str  # 'low', 'medium', 'high', 'critical'
    column_name: str  # 'backlog', 'in_progress', 'review', 'done'
    assignee: Optional[str] = None
    lead_time_hours: float = 0.0
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict):
        if not data:
            return None
        return cls(
            id=data.get('id'),
            title=data.get('title'),
            description=data.get('description', ''),
            category=data.get('category', 'General'),
            priority=data.get('priority', 'medium'),
            column_name=data.get('column_name', 'backlog'),
            assignee=data.get('assignee'),
            lead_time_hours=float(data.get('lead_time_hours', 0.0)),
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at')
        )

@dataclass
class WIPLimit:
    column_name: str
    wip_limit: int

    @classmethod
    def from_dict(cls, data: dict):
        if not data:
            return None
        return cls(
            column_name=data.get('column_name'),
            wip_limit=int(data.get('wip_limit', 5))
        )
