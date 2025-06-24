from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from .models import Book, CD, DVD, BoardGame, Member, Loan, Media
from .forms import (MemberForm, MemberCreateForm, BookForm,
                    CDForm, DVDForm, BoardGameForm, LoanForm)
from datetime import datetime, timedelta
import logging
logger = logging.getLogger('medialibrary')


def is_librarian(user):
    logger.info("Page d’accueil visitée")
    return user.is_staff


# Vu's publishes
def home(request):
    return render(request, 'medialibrary/home.html')

#logout
def logout_view(request):
    logout(request)
    return redirect('home')

#redirection en fonction du rôle utilisateur
def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.is_staff:
                return redirect('librarian_dashboard')
            else:
                return redirect('member_media_list')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

# Vu's members
@login_required
def member_media_list(request):
    media = {
        'books': Book.objects.all(),
        'cds': CD.objects.all(),
        'dvds': DVD.objects.all(),
        'boardgames': BoardGame.objects.all()
    }
    return render(request, 'medialibrary/member/media_list.html', media)


# Vu's billionaires
@login_required
@user_passes_test(is_librarian)
def librarian_dashboard(request):
    stats = {
        'members': Member.objects.count(),
        'media': Media.objects.count(),
        'active_loans': Loan.objects.filter(return_date__isnull=True).count(),
        'overdue_loans': Loan.objects.filter(
            return_date__isnull=True,
            due_date__lt=datetime.now().date()
        ).count()
    }
    return render(request, 'medialibrary/librarian/dashboard.html', {'stats': stats})


@login_required
@user_passes_test(is_librarian)
def member_list(request):
    members = Member.objects.all()
    return render(request, 'medialibrary/librarian/member_list.html', {'members': members})


@login_required
@user_passes_test(is_librarian)
def member_create(request):
    if request.method == 'POST':
        form = MemberCreateForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email=form.cleaned_data['email']
            )
            Member.objects.create(
                user=user,
                address=form.cleaned_data['address'],
                phone=form.cleaned_data['phone']
            )
            return redirect('member_list')
    else:
        form = MemberCreateForm()
    return render(request, 'medialibrary/librarian/member_form.html', {'form': form})


@login_required
@user_passes_test(is_librarian)
def member_update(request, pk):
    member = get_object_or_404(Member, pk=pk)
    if request.method == 'POST':
        form = MemberForm(request.POST, instance=member)
        if form.is_valid():
            form.save()
            return redirect('member_list')
    else:
        form = MemberForm(instance=member)
    return render(request, 'medialibrary/librarian/member_form.html', {'form': form, 'update': True})


@login_required
@user_passes_test(is_librarian)
def media_list(request):
    media = {
        'books': Book.objects.all(),
        'cds': CD.objects.all(),
        'dvds': DVD.objects.all(),
        'boardgames': BoardGame.objects.all()
    }
    return render(request, 'medialibrary/librarian/media_list.html', media)


@login_required
@user_passes_test(is_librarian)
def media_create(request, media_type):
    FormClass = {
        'book': BookForm,
        'cd': CDForm,
        'dvd': DVDForm,
        'boardgame': BoardGameForm
    }.get(media_type)

    if request.method == 'POST':
        form = FormClass(request.POST)
        if form.is_valid():
            form.save()
            return redirect('media_list')
    else:
        form = FormClass()

    return render(request, 'medialibrary/librarian/media_form.html', {
        'form': form,
        'media_type': media_type
    })


@login_required
@user_passes_test(is_librarian)
def loan_list(request):
    loans = {
        'active': Loan.objects.filter(return_date__isnull=True),
        'overdue': Loan.objects.filter(
            return_date__isnull=True,
            due_date__lt=datetime.now().date()
        ),
        'completed': Loan.objects.filter(return_date__isnull=False)
    }
    return render(request, 'medialibrary/librarian/loan_list.html', loans)


@login_required
@user_passes_test(is_librarian)
def loan_create(request):
    if request.method == 'POST':
        form = LoanForm(request.POST)
        if form.is_valid():
            loan = form.save(commit=False)
            loan.due_date = datetime.now().date() + timedelta(days=7)
            loan.save()
            return redirect('loan_list')
    else:
        form = LoanForm()
    return render(request, 'medialibrary/librarian/loan_form.html', {'form': form})


@login_required
@user_passes_test(is_librarian)
def loan_return(request, pk):
    loan = get_object_or_404(Loan, pk=pk)
    if request.method == 'POST':
        loan.return_date = datetime.now().date()
        loan.save()
        return redirect('loan_list')
    return render(request, 'medialibrary/librarian/loan_return.html', {'loan': loan})