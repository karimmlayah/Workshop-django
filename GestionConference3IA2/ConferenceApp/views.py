from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Conference, Submission
from .forms import (
    ConferenceForm,
    SubmissionForm,
    SubmissionAdminForm,
    SubmissionFormWithConference,
    SubmissionAdminFormWithConference,
)
from django.core.exceptions import PermissionDenied
from .forms import ConferenceForm


# Liste des conférences
class ConferenceList(ListView):
    model = Conference
    context_object_name = "liste"
    template_name = "conferences/liste.html"


# Détails d'une conférence
class ConferenceDetails(LoginRequiredMixin, DetailView):
    model = Conference
    context_object_name = "conference"
    template_name = "conferences/details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Récupérer les soumissions liées à cette conférence
        context["submissions"] = Submission.objects.filter(
            conference=self.object,
            user=self.request.user
        ).order_by("-submission_date")
        
        return context



# Création d'une nouvelle conférence
class ConferenceCreate(CreateView):
    model = Conference
    form_class = ConferenceForm
    template_name = "conferences/form.html"
    success_url = reverse_lazy("liste_conferences")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titre"] = "Créer une nouvelle conférence"
        context["btn"] = "Enregistrer"
        return context



# Modification d'une conférence existante
class ConferenceUpdate(UpdateView):
    model = Conference
    form_class = ConferenceForm
    template_name = "conferences/form.html"
    success_url = reverse_lazy("liste_conferences")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titre"] = "Modifier la conférence"
        context["btn"] = "Mettre à jour"
        return context


# Suppression d'une conférence
class ConferenceDelete(DeleteView):
    model = Conference
    template_name = "conferences/delete_confirm.html"
    success_url = reverse_lazy("liste_conferences")


# Liste des soumissions d'un utilisateur pour une conférence donnée
class SubmissionList(LoginRequiredMixin, ListView):
    model = Submission
    context_object_name = "submissions"
    template_name = "submissions/liste.html"

    def get_queryset(self):
        conference_id = self.kwargs.get("conference_id")
        return (
            Submission.objects.select_related("conference", "user")
            .filter(conference_id=conference_id, user=self.request.user)
            .order_by("-submission_date")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        conference_id = self.kwargs.get("conference_id")
        context["conference"] = get_object_or_404(Conference, pk=conference_id)
        return context


# Détails d'une soumission (réservé à l'auteur)
class SubmissionDetails(LoginRequiredMixin, DetailView):
    model = Submission
    context_object_name = "submission"
    template_name = "submissions/details.html"

    def get_queryset(self):
        return Submission.objects.select_related("conference", "user").filter(user=self.request.user)


# Création d'une soumission
class SubmissionCreate(LoginRequiredMixin, CreateView):
    model = Submission
    form_class = SubmissionForm
    template_name = "submissions/form.html"

    def dispatch(self, request, *args, **kwargs):
        # Ensure conference exists
        self.conference = get_object_or_404(Conference, pk=kwargs.get("conference_id"))
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        # Include status and payed on create form
        self.form_class = SubmissionAdminForm
        form = super().get_form(self.form_class)
        # Bind required relations before model.clean runs during validation
        form.instance.user = self.request.user
        form.instance.conference = self.conference
        return form

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.conference = self.conference
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("conference_submissions", kwargs={"conference_id": self.conference.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["conference"] = self.conference
        context["titre"] = "Ajouter une soumission"
        context["btn"] = "Enregistrer"
        return context


# Mise à jour d'une soumission
class SubmissionUpdate(LoginRequiredMixin, UpdateView):
    model = Submission
    form_class = SubmissionForm
    template_name = "submissions/form.html"

    def get_queryset(self):
        return Submission.objects.filter(user=self.request.user)

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.status in ("accepted", "rejected"):
            raise PermissionDenied("Soumission non modifiable après décision.")
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy("conference_submissions", kwargs={"conference_id": self.object.conference.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["conference"] = self.object.conference
        context["titre"] = "Modifier la soumission"
        context["btn"] = "Mettre à jour"
        return context

    def get_form(self, form_class=None):
        # Staff/committee can set status/payed on update (when allowed)
        if self.request.user.is_staff or getattr(self.request.user, "role", None) == "commitee":
            self.form_class = SubmissionAdminForm
        return super().get_form(self.form_class)


class SubmissionPay(LoginRequiredMixin, View):
    def post(self, request, pk):
        submission = get_object_or_404(Submission, pk=pk, user=request.user)
        if not submission.payed:
            submission.payed = True
            submission.save(update_fields=["payed"]) 
        next_url = request.POST.get("next")
        if next_url:
            from django.shortcuts import redirect
            return redirect(next_url)
        return redirect(
            reverse_lazy("conference_submissions", kwargs={"conference_id": submission.conference.pk})
        )


class SubmissionUpdateStatus(LoginRequiredMixin, View):
    def post(self, request, pk):
        submission = get_object_or_404(Submission.objects.select_related("conference"), pk=pk)
        # Only staff or committee members can change status
        is_committee = getattr(request.user, "role", None) == "commitee"
        if not (request.user.is_staff or is_committee):
            raise PermissionDenied("Non autorisé à modifier le statut.")
        new_status = request.POST.get("status")
        valid_statuses = {choice[0] for choice in Submission.STATUS}
        if new_status in valid_statuses:
            submission.status = new_status
            submission.save(update_fields=["status"]) 
        next_url = request.POST.get("next")
        if next_url:
            from django.shortcuts import redirect
            return redirect(next_url)
        return redirect(
            reverse_lazy("conference_submissions", kwargs={"conference_id": submission.conference.pk})
        )


# Liste de toutes les soumissions de l'utilisateur (toutes conférences)
class MySubmissions(LoginRequiredMixin, ListView):
    model = Submission
    context_object_name = "submissions"
    template_name = "submissions/liste_all.html"

    def get_queryset(self):
        return (
            Submission.objects.select_related("conference", "user")
            .filter(user=self.request.user)
            .order_by("-submission_date")
        )


# Création d'une soumission (sélection de la conférence dans le formulaire)
class SubmissionCreateGlobal(LoginRequiredMixin, CreateView):
    model = Submission
    form_class = SubmissionFormWithConference
    template_name = "submissions/form.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("my_submissions")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titre"] = "Ajouter une soumission"
        context["btn"] = "Enregistrer"
        return context

    def get_form(self, form_class=None):
        # Include status and payed on create form (with conference selector)
        self.form_class = SubmissionAdminFormWithConference
        form = super().get_form(self.form_class)
        form.instance.user = self.request.user
        return form
