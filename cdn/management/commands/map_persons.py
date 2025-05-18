import os, re, string, configparser
from typing import Union

from django.core.management.base import BaseCommand
from django.conf import settings

from cdn.models import *
from common.utils import get_or_none, get_media_types

class Command(BaseCommand):
	help = 'Reads the .ini file found in the image directory and generate person tags for the photos'

	# Tracks max file reads
	_file_count = 0

	_, _media_ext = get_media_types()

	# Approved file types
	file_types = []

	def handle(self, *args, **options):
		self.stdout.write('Started scanning the MEDIA_ROOT')

		# Look for the .ini file
		ini_file = ""
		for file in os.listdir(settings.MEDIA_ROOT):
			if os.path.isfile(file) and file.endswith(".ini"):
				ini_file = file
				break
		if ini_file == "":
			self.stdout.write(self.style.ERROR('No ini file found'))
			return

		# Read .ini file
		config = configparser.ConfigParser()
		config.read(ini_file)

		# Look for person ID section
		person_section = ""
		for section in config.sections():
			if "Contacts" in section:
				person_section = section
		if ini_file == "":
			self.stdout.write(self.style.ERROR('No section with person ID data found'))
			return

		# Process section
		person_tag_batch = []
		person_ids = {}
		for flag in config[person_section]:
			name = config[person_section][flag].strip().translate(str.maketrans('', '', string.punctuation))
			# Check the records
			temp_person = get_or_none(Person, name=name)
			if temp_person is None:
				temp_person = Person(
					name=name,
				)
				person_tag_batch.append(temp_person)
			person_ids[flag] = temp_person

		# Batch Create if Filled
		if len(person_tag_batch) > 0:
			Person.objects.bulk_create(person_tag_batch)

		# Start Processing
		for section in config.sections():
			# Bypass if no faces flag
			if "faces" not in config[section]:
				continue

			# TODO loop thru pictures and add person tag if not already

		self.stdout.write(self.style.SUCCESS('Successfully scanned the MEDIA_ROOT'))
		
	def add_arguments(self, parser):
		parser.add_argument("--batch_size", type=int, help="batch size to use before bulk creating new entries in DB", default=50)
		parser.add_argument("--max_reads", type=int, help="maximum amount of entries to make", default=-1)
		parser.add_argument("--media_only", help="toggle scan to media files only", action="store_true", default=False)