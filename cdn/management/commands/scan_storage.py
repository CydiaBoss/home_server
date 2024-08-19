from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
	help = 'Scans the MEDIA_ROOT folder and populates the database as needed'

	def handle(self, *args, **options):
		self.stdout.write('Started scanning the MEDIA_ROOT')

		self.stdout.write(self.style.SUCCESS('Successfully scanned the MEDIA_ROOT'))