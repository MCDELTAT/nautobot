from nautobot.core.apps import HomePageItem, HomePagePanel
from nautobot.extras.choices import JobResultStatusChoices
from nautobot.extras.models import GitRepository, JobResult, ObjectChange


def get_job_results(request):
    """Callback function to collect job history for panel."""
    return (
        JobResult.objects.filter(status__in=JobResultStatusChoices.READY_STATES)
        .restrict(request.user, "view")
        .only("id", "name", "status", "date_done", "user")
        .order_by("-date_done")[:10]
    )


def get_changelog(request):
    """Callback function to collect changelog for panel."""
    return ObjectChange.objects.restrict(request.user, "view").only(
        "id",
        "action",
        "changed_object",
        "changed_object_id",
        "changed_object_type",
        "object_repr",
        "user_name",
        "time",
    )[:15]


layout = (
    HomePagePanel(
        name="Data Sources",
        weight=700,
        items=(
            HomePageItem(
                name="Git Repositories",
                link="extras:gitrepository_list",
                model=GitRepository,
                description="Collections of data and/or job files",
                permissions=["extras.view_gitrepository"],
                weight=100,
            ),
        ),
    ),
    HomePagePanel(
        name="Job History",
        permissions=["extras.view_jobresult"],
        weight=800,
        custom_data={"job_results": get_job_results},
        custom_template="panel_jobhistory.html",
    ),
    HomePagePanel(
        name="Change Log",
        permissions=["extras.view_objectchange"],
        weight=900,
        custom_data={"changelog": get_changelog},
        custom_template="panel_changelog.html",
    ),
)
