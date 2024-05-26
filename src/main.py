from jira import JiraFeature, JiraTicket, JiraTicketType
from consts import Assignee

feature = JiraFeature(
    name="Rapport Globalisé",
    tickets=[
        JiraTicket(
            feature="Rapport Globalisé",
            assignees=[Assignee.TRAN, Assignee.POIRIER],
            type=JiraTicketType.US,
            story_points=5,
        ),
        JiraTicket(
            feature="Rapport Globalisé",
            assignees=[Assignee.GOURDEAU, Assignee.POIRIER],
            type=JiraTicketType.US,
            story_points=8,
        ),
        JiraTicket(
            feature="Rapport Globalisé",
            assignees=[Assignee.POIRIER],
            type=JiraTicketType.US,
            story_points=3,
        ),
        JiraTicket(
            feature="Rapport Globalisé",
            assignees=[Assignee.DUBREU],
            type=JiraTicketType.US,
            story_points=13,
        ),
    ],
)


def main():
    for assignee in Assignee:
        print(
            f"{assignee=} : {feature.get_assignee_KS(assignee)*100:.2f}%"
        )  # Waterloo : create a repr

    print(f"Mean : {feature.get_mean()}")
    print(f"Standard Deviation : {feature.get_stdev()}")


if __name__ == "__main__":
    main()
