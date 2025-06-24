from django import forms
from .models import Member, Book, CD, DVD, BoardGame, Loan, Media


class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['address', 'phone', 'can_borrow']


class MemberCreateForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=150)
    email = forms.EmailField()
    address = forms.CharField(widget=forms.Textarea)
    phone = forms.CharField(max_length=20)


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'


class CDForm(forms.ModelForm):
    class Meta:
        model = CD
        fields = '__all__'


class DVDForm(forms.ModelForm):
    class Meta:
        model = DVD
        fields = '__all__'


class BoardGameForm(forms.ModelForm):
    class Meta:
        model = BoardGame
        fields = '__all__'


class LoanForm(forms.ModelForm):
    class Meta:
        model = Loan
        fields = ['media', 'member']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['media'].queryset = Media.objects.filter(available=True).exclude(media_type='BOARDGAME')
        self.fields['member'].queryset = Member.objects.filter(can_borrow=True)