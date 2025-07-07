from django.core.management.base import BaseCommand
from wixbuddy.models import Question

class Command(BaseCommand):
    help = 'Populate the database with survey questions'

    def handle(self, *args, **options):
        questions_data = [
            {
                'title': 'Which of these describes you?',
                'options': ['Business Owner', 'Manager', 'Engineer', 'Other'],
                'order': 1
            },
            {
                'title': 'What is your friend of work in road transport?',
                'options': ['Manufacturing', 'Modification', 'Safety and Compliance'],
                'order': 2
            },
            {
                'title': 'What kind of vehicles do you specialize in?',
                'options': ['Light', 'Heavy', 'Freight', 'Road Tanker'],
                'order': 3
            },
            {
                'title': 'Why do you want to join Regpus?',
                'options': ['Time consuming research for compliance standards', 'Lack of centralized', 'Others'],
                'order': 4
            }
        ]

        for data in questions_data:
            question, created = Question.objects.get_or_create(
                title=data['title'],
                defaults={
                    'options': data['options'],
                    'order': data['order'],
                    'question_type': 'multiple_choice'
                }
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created question: {question.title}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Question already exists: {question.title}')
                ) 