from django.test import TestCase
from django.contrib.auth.models import User
from .models import Member, Book, CD, BoardGame, Loan
from datetime import date, timedelta
from django.core.exceptions import ValidationError


class MediaModelTest(TestCase):
    def setUp(self):
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            publication_date=date.today(),
            media_type="BOOK",
            isbn="1234567890",
            page_count=100
        )

        self.cd = CD.objects.create(
            title="Test CD",
            author="Test Artist",
            publication_date=date.today(),
            media_type="CD",
            duration=60,
            track_count=12
        )

        self.boardgame = BoardGame.objects.create(
            title="Test Game",
            author="Test Creator",
            publication_date=date.today(),
            media_type="BOARDGAME",
            min_players=2,
            max_players=4,
            duration=30
        )

    def test_media_creation(self):
        self.assertEqual(str(self.book), "Test Book (Livre)")
        self.assertEqual(str(self.cd), "Test CD (CD)")
        self.assertEqual(str(self.boardgame), "Test Game (Jeu de plateau)")


class MemberModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123",
            first_name="Test",
            last_name="User"
        )
        self.member = Member.objects.create(
            user=self.user,
            address="123 Test St",
            phone="0123456789"
        )

    def test_member_creation(self):
        self.assertEqual(str(self.member), "Test User")
        self.assertTrue(self.member.can_borrow)

    def test_borrow_status(self):
        book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            publication_date=date.today(),
            media_type="BOOK",
            isbn="1234567890",
            page_count=100
        )

        # Emprunt en retard
        Loan.objects.create(
            media=book,
            member=self.member,
            due_date=date.today() - timedelta(days=1))

        self.member.update_borrow_status()
        self.assertFalse(self.member.can_borrow)

        # Retour du livre
        loan = Loan.objects.first()
        loan.return_date = date.today()
        loan.save()

        self.member.refresh_from_db()
        self.assertTrue(self.member.can_borrow)


class LoanModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.member = Member.objects.create(user=self.user, address="123 Test St", phone="1234567890")

        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            publication_date=date.today(),
            media_type="BOOK",
            isbn="1234567890",
            page_count=100
        )

        self.boardgame = BoardGame.objects.create(
            title="Test Game",
            author="Test Creator",
            publication_date=date.today(),
            media_type="BOARDGAME",
            min_players=2,
            max_players=4,
            duration=30
        )

    def test_loan_creation(self):
        loan = Loan.objects.create(
            media=self.book,
            member=self.member
        )
        self.assertEqual(loan.due_date, date.today() + timedelta(days=7))
        self.assertFalse(self.book.available)

    def test_loan_return(self):
        loan = Loan.objects.create(
            media=self.book,
            member=self.member
        )
        loan.return_date = date.today()
        loan.save()

        self.book.refresh_from_db()
        self.assertTrue(self.book.available)

    def test_max_loans(self):
        # Créer 3 emprunts
        for i in range(3):
            book = Book.objects.create(
                title=f"Test Book {i}",
                author="Test Author",
                publication_date=date.today(),
                media_type="BOOK",
                isbn=f"123456789{i}",
                page_count=100
            )
            Loan.objects.create(
                media=book,
                member=self.member
            )

        # Essayer de créer un 4ème emprunt
        book = Book.objects.create(
            title="Test Book 4",
            author="Test Author",
            publication_date=date.today(),
            media_type="BOOK",
            isbn="1234567894",
            page_count=100
        )
        loan = Loan(media=book, member=self.member)

        with self.assertRaises(ValidationError):
            loan.full_clean()

    def test_boardgame_loan(self):
        loan = Loan(media=self.boardgame, member=self.member)
        with self.assertRaises(ValidationError):
            loan.full_clean()


class ViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.member = Member.objects.create(user=self.user, address="123 Test St", phone="1234567890")

        Book.objects.create(
            title="Test Book",
            author="Test Author",
            publication_date=date.today(),
            media_type="BOOK",
            isbn="1234567890",
            page_count=100
        )

    def test_member_media_list_view(self):
        response = self.client.get('/member/media/')
        self.assertEqual(response.status_code, 302)  # Redirection vers login

        self.client.login(username="testuser", password="12345")
        response = self.client.get('/member/media/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Book")

    def test_librarian_views_protection(self):
        # Test sans connexion
        response = self.client.get('/librarian/')
        self.assertEqual(response.status_code, 302)

        # Test avec membre normal
        self.client.login(username="testuser", password="12345")
        response = self.client.get('/librarian/')
        self.assertEqual(response.status_code, 403)

        # Test avec bibliothécaire
        admin = User.objects.create_superuser(username="admin", password="admin")
        self.client.login(username="admin", password="admin")
        response = self.client.get('/librarian/')
        self.assertEqual(response.status_code, 200)