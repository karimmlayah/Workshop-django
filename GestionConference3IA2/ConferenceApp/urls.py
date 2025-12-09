from django.urls import path
from . import views
from .views import *

urlpatterns = [
    # Conférences
    path("liste/", ConferenceList.as_view(), name="liste_conferences"),
    path("<int:pk>/", ConferenceDetails.as_view(), name="conference_details"),
    path("add/", ConferenceCreate.as_view(), name="conference_add"),
    path("<int:pk>/update/", ConferenceUpdate.as_view(), name="conference_update"),
    path("<int:pk>/delete/", ConferenceDelete.as_view(), name="conference_delete"),

    # Soumissions
    path(
        "conference/<int:conference_id>/submissions/",
        SubmissionList.as_view(),
        name="conference_submissions",
    ),
    path(
        "conference/<int:conference_id>/submissions/add/",
        SubmissionCreate.as_view(),
        name="submission_add",
    ),
    path(
        "submissions/mine/",
        MySubmissions.as_view(),
        name="my_submissions",
    ),
    path(
        "submissions/add/",
        SubmissionCreateGlobal.as_view(),
        name="submission_add_global",
    ),
    path(
        "submissions/<str:pk>/",
        SubmissionDetails.as_view(),
        name="submission_details",
    ),
    path(
        "submissions/<str:pk>/update/",
        SubmissionUpdate.as_view(),
        name="submission_update",
    ),
    path(
        "submissions/<str:pk>/pay/",
        SubmissionPay.as_view(),
        name="submission_pay",
    ),
    path(
        "submissions/<str:pk>/status/",
        SubmissionUpdateStatus.as_view(),
        name="submission_update_status",
    ),
]
