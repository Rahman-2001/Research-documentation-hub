from typing import Any
from django.core.management.base import BaseCommand
from django.db import connection
from blog.models import Category


class Command(BaseCommand):  # Must be "Command" with capital C
    help = "This command inserts Category data and resets ID counter"

    def handle(self, *args: Any, **options: Any):

        # Delete all existing data
        Category.objects.all().delete()

        # Reset AUTO_INCREMENT ID counter
        # with connection.cursor() as cursor:
        #     cursor.execute("ALTER TABLE blog_post AUTO_INCREMENT = 1;")

        categories = ['Sports', 'Technology', 'Science', 'Art', 'Food']

        for category_name in categories:
            Category.objects.create(name = category_name)


        self.stdout.write(self.style.SUCCESS("✅ Completed inserting category data!"))
