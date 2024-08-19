import os, re
from typing import Union

from django.core.management.base import BaseCommand
from django.conf import settings

from cdn.models import *
from common.utils import get_or_none

class Command(BaseCommand):
	help = 'Scans the MEDIA_ROOT folder and populates the database as needed'

	def handle(self, *args, **options):
		self.stdout.write('Started scanning the MEDIA_ROOT')

		self._process_dir_items(settings.MEDIA_ROOT)

		self.stdout.write(self.style.SUCCESS('Successfully scanned the MEDIA_ROOT'))

	def _process_dir_items(self, dir_name : str, parent_folder : Union[Folder, None]=None):
		"""
		Walk through directory and creates a model for them if not already
		"""
		# Loop through items
		self.stdout.write('Walking through directory "%s"' % dir_name)

		# Temp files list for bulk create
		files = []

		# Looping
		for item in os.listdir(dir_name):
			# Item path
			item_path = f'{dir_name}{item}'

			# Recursive for folders
			if os.path.isdir(item_path):
				# Create or get Folder Model
				folder, _ = Folder.objects.get_or_create(
					parent=parent_folder,
					name__iexact=item,
					defaults={
						"name": item
					}
				)
				
				# Process its children
				self._process_dir_items(item_path + "/", folder)

				# Finish
				continue

			# Parse File Name
			parsed_name = re.match(r"^([\w,\s\-\.]+)\.([A-Za-z]+)$", item)

			# Skip file if fail to parse 
			if parsed_name is None:
				self.stderr.write('File "%s" could not be parsed' % item)
				continue

			# Look for file
			file = get_or_none(File, 
				folder=parent_folder, 
				file_name__iexact=parsed_name.group(1),
				file_ext__iexact=parsed_name.group(2)
			)

			# Skip if file already found (for now)
			if file is not None:
				self.stdout.write('File "%s" already exists in database' % item)
				continue

			# Check if file model exist yet
			file = File()
			file.folder = parent_folder

			# Process file name
			file.file_name = parsed_name.group(1)
			file.file_ext = parsed_name.group(2)

			# Add to temp list
			files.append(file)

		# Bulk create
		File.objects.bulk_create(files)