from enum import Enum
from pydantic import BaseModel, Field, model_validator
from typing import List
from consts import Assignee
import statistics


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
    # feature: str  # Waterloo : Not sure if should be in this class
    assignees: List[Assignee]
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


class JiraFeature(BaseModel):
    name: str
    tickets: List[JiraTicket]

    def get_assignee_KQ(self, assignee: Assignee) -> float:
        return sum(
            [
                max(ticket.story_points, 1)
                * ticket.operation_value
                / len(ticket.assignees)
                for ticket in self.tickets
                if assignee in ticket.assignees
            ]
        )

    def get_assignee_KS(self, assignee: Assignee) -> float:
        return self.get_assignee_KQ(assignee) / sum(
            [self.get_assignee_KQ(assignee) for assignee in Assignee]
        )

    def get_mean(self) -> float:
        return statistics.mean(
            [self.get_assignee_KQ(assignee) for assignee in Assignee]
        )

    def get_stdev(self) -> float:
        return statistics.stdev(
            [self.get_assignee_KQ(assignee) for assignee in Assignee]
        )
