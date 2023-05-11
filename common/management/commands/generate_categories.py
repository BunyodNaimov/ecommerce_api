from django.core.management.base import BaseCommand, CommandError


from factories import ParentCategoryFactory, CategoryFactory


class Command(BaseCommand):
    help = 'Generate categories'

    def handle(self, *args, **options):
        ParentCategoryFactory.create_batch(size=5)
        CategoryFactory.create_batch(size=10)
        self.stdout.write(self.style.SUCCESS('Successfully generate categories.'))
