from enum import Enum
from pydantic import BaseModel, Field, model_validator
from typing import List


class JiraTicketType(Enum):
    US = "User Story"
    TASK = "Task"
    BUG = "Bug"
    REFACTOR = "Refacto"
    SPIKE = "Spike"
    PR = "Pull Request"
    CD = "Code Review"
    DOCUMENTATION = "Documentation"


class OperationType(Enum):
    CREATE = "CREATE"
    UPDATE = "UPDATE"
    READ = "READ"


class JiraTicket(BaseModel):
    feature: str
    assignees: List[str]
    type: JiraTicketType
    story_points: int

    operation_name: OperationType = Field(default=None)
    operation_value: int = Field(default=None)

    @model_validator(mode="before")
    def set_operation_based_on_ticket_type(cls, values):
        ticket_type = values.get("type")
        if ticket_type in (JiraTicketType.US, JiraTicketType.TASK):
            values["operation_name"] = OperationType.CREATE
            values["operation_value"] = 4
        if ticket_type in (JiraTicketType.BUG, JiraTicketType.REFACTOR):
            values["operation_name"] = OperationType.UPDATE
            values["operation_value"] = 2
        if ticket_type in (
            JiraTicketType.SPIKE,
            JiraTicketType.PR,
            JiraTicketType.CD,
            JiraTicketType.DOCUMENTATION,
        ):
            values["operation_name"] = OperationType.READ
            values["operation_value"] = 1
        return values
