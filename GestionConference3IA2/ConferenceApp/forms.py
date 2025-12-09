from django import forms
from .models import Conference, Submission

class ConferenceForm(forms.ModelForm):
    class Meta:
        model = Conference
        fields = ['name', 'theme', 'location', 'start_date', 'end_date', 'description']


        labels = {
            'name': 'titre de la conférence',
            'theme': 'Thématique de la conférence',
            'lieu': 'Lieu',
            'start_date': 'Date de début',
            'end_date': 'Date de fin',
            'description': 'Description',
        }


class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = [
            'title',
            'abstract',
            'keyword',
            'paper',
        ]

        labels = {
            'title': 'Titre',
            'abstract': 'Résumé',
            'keyword': 'Mots-clés (séparés par des virgules, max 10)',
            'paper': 'Fichier PDF',
        }

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'abstract': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'keyword': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ex: AI, ML, Data Mining'}),
            'paper': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


class SubmissionAdminForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = [
            'title',
            'abstract',
            'keyword',
            'paper',
            'status',
            'payed',
        ]

        labels = {
            'title': 'Titre',
            'abstract': 'Résumé',
            'keyword': 'Mots-clés (séparés par des virgules, max 10)',
            'paper': 'Fichier PDF',
            'status': 'Statut',
            'payed': 'Payé',
        }

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'abstract': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'keyword': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ex: AI, ML, Data Mining'}),
            'paper': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'payed': forms.CheckboxInput(attrs={}),
        }


class SubmissionFormWithConference(forms.ModelForm):
    class Meta:
        model = Submission
        fields = [
            'conference',
            'title',
            'abstract',
            'keyword',
            'paper',
        ]

        labels = {
            'conference': 'Conférence',
            'title': 'Titre',
            'abstract': 'Résumé',
            'keyword': 'Mots-clés (séparés par des virgules, max 10)',
            'paper': 'Fichier PDF',
        }

        widgets = {
            'conference': forms.Select(attrs={'class': 'form-select'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'abstract': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'keyword': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ex: AI, ML, Data Mining'}),
            'paper': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Optionally limit to upcoming conferences
        self.fields['conference'].queryset = Conference.objects.all()


class SubmissionAdminFormWithConference(forms.ModelForm):
    class Meta:
        model = Submission
        fields = [
            'conference',
            'title',
            'abstract',
            'keyword',
            'paper',
            'status',
            'payed',
        ]

        labels = {
            'conference': 'Conférence',
            'title': 'Titre',
            'abstract': 'Résumé',
            'keyword': 'Mots-clés (séparés par des virgules, max 10)',
            'paper': 'Fichier PDF',
            'status': 'Statut',
            'payed': 'Payé',
        }

        widgets = {
            'conference': forms.Select(attrs={'class': 'form-select'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'abstract': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'keyword': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ex: AI, ML, Data Mining'}),
            'paper': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'payed': forms.CheckboxInput(attrs={}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['conference'].queryset = Conference.objects.all()

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex : Entrer le titre de la conférence'
            }),
            'theme': forms.Select(attrs={
                'class': 'form-select'
            }),
            'lieu': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex : Paris, France'
            }),
            'start_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'end_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Ajoutez une description détaillée...',
                'rows': 3
            }),
        }
