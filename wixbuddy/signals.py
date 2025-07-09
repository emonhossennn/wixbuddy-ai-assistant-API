from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Question

@receiver(post_save, sender=Question)
def renumber_questions(sender, instance, **kwargs):
    questions = Question.objects.all().order_by('order', 'pk')
    for idx, q in enumerate(questions, start=1):
        new_title = f"{idx}. {q.title.lstrip('0123456789. ')}"
        if q.order != idx or q.title != new_title:
            q.order = idx
            q.title = new_title
            q.save(update_fields=['order', 'title']) 