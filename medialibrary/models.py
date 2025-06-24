from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import datetime, timedelta


class Media(models.Model):
    TYPE_CHOICES = [
        ('BOOK', 'Livre'),
        ('CD', 'CD'),
        ('DVD', 'DVD'),
        ('BOARDGAME', 'Jeu de plateau'),
    ]

    title = models.CharField(max_length=200, verbose_name="Titre")
    author = models.CharField(max_length=100, verbose_name="Auteur")
    publication_date = models.DateField(verbose_name="Date de publication")
    media_type = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name="Type de média")
    available = models.BooleanField(default=True, verbose_name="Disponible")

    def __str__(self):
        return f"{self.title} ({self.get_media_type_display()})"

    class Meta:
        ordering = ['title']


class Book(Media):
    isbn = models.CharField(max_length=20, verbose_name="ISBN", unique=True)
    page_count = models.IntegerField(verbose_name="Nombre de pages")

    class Meta:
        verbose_name = "Livre"
        verbose_name_plural = "Livres"


class CD(Media):
    duration = models.IntegerField(verbose_name="Durée (minutes)")
    track_count = models.IntegerField(verbose_name="Nombre de pistes")

    class Meta:
        verbose_name = "CD"
        verbose_name_plural = "CDs"


class DVD(Media):
    duration = models.IntegerField(verbose_name="Durée (minutes)")
    video_format = models.CharField(max_length=10, verbose_name="Format vidéo")

    class Meta:
        verbose_name = "DVD"
        verbose_name_plural = "DVDs"


class BoardGame(Media):
    min_players = models.IntegerField(verbose_name="Joueurs minimum")
    max_players = models.IntegerField(verbose_name="Joueurs maximum")
    duration = models.IntegerField(verbose_name="Durée moyenne (minutes)")

    class Meta:
        verbose_name = "Jeu de plateau"
        verbose_name_plural = "Jeux de plateau"


class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Utilisateur")
    address = models.TextField(verbose_name="Adresse")
    phone = models.CharField(max_length=20, verbose_name="Téléphone")
    membership_date = models.DateField(auto_now_add=True, verbose_name="Date d'adhésion")
    can_borrow = models.BooleanField(default=True, verbose_name="Peut emprunter")

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username}"

    def update_borrow_status(self):
        overdue_loans = self.loan_set.filter(
            return_date__isnull=True,
            due_date__lt=datetime.now().date()
        ).exists()
        active_loans = self.loan_set.filter(return_date__isnull=True).count()
        self.can_borrow = not overdue_loans and active_loans < 3
        self.save()

    class Meta:
        verbose_name = "Membre"
        verbose_name_plural = "Membres"
        ordering = ['user__last_name']


class Loan(models.Model):
    media = models.ForeignKey(Media, on_delete=models.CASCADE, verbose_name="Média")
    member = models.ForeignKey(Member, on_delete=models.CASCADE, verbose_name="Membre")
    loan_date = models.DateField(auto_now_add=True, verbose_name="Date d'emprunt")
    due_date = models.DateField(verbose_name="Date de retour prévue")
    return_date = models.DateField(null=True, blank=True, verbose_name="Date de retour effectif")

    def __str__(self):
        return f"{self.media} emprunté par {self.member}"

    def clean(self):
        # Validation des règles métier
        if not self.pk:  # Nouvel emprunt seulement
            if not self.media.available:
                raise ValidationError("Ce média n'est pas disponible pour l'emprunt.")

            if self.media.media_type == 'BOARDGAME':
                raise ValidationError("Les jeux de plateau ne peuvent pas être empruntés.")

            active_loans = self.member.loan_set.filter(return_date__isnull=True).count()
            if active_loans >= 3:
                raise ValidationError("Ce membre a déjà 3 emprunts en cours.")

            if not self.member.can_borrow:
                raise ValidationError("Ce membre ne peut pas emprunter (emprunts en retard ou trop d'emprunts).")

    def save(self, *args, **kwargs):
        if not self.pk:  # Nouvel emprunt
            self.due_date = datetime.now().date() + timedelta(days=7)
            self.media.available = False
            self.media.save()
        elif self.return_date and not self.media.available:  # Retour
            self.media.available = True
            self.media.save()
            self.member.update_borrow_status()

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Emprunt"
        verbose_name_plural = "Emprunts"
        ordering = ['-loan_date']