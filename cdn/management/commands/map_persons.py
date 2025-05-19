import os, re, string, configparser
from typing import Union

from django.core.management.base import BaseCommand
from django.conf import settings
from django.db.models import Q

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

		# Subdir msg
		if options["dir"] != "":
			self.stdout.write(f'Sub directory {options["dir"]} selected for scanning')
		root_dir = settings.MEDIA_ROOT + f"/{options['dir']}"

		# Look for the .ini file
		ini_file = ""
		for file in os.listdir(root_dir):
			if os.path.isfile(f"{root_dir}/{file}") and file.endswith(".ini"):
				ini_file = file
				break
		if ini_file == "":
			self.stdout.write(self.style.ERROR('No ini file found'))
			return

		# Read .ini file
		config = configparser.ConfigParser()
		config.read(f"{root_dir}/{ini_file}")

		# Look for person ID section
		person_section = ""
		for section in config.sections():
			if "Contacts" in section:
				person_section = section
		if person_section == "":
			self.stdout.write(self.style.ERROR('No section with person ID data found'))
			return

		# Process section
		person_ids : dict[str, Person] = {}
		for flag in config[person_section]:
			name = config[person_section][flag].strip().translate(str.maketrans('', '', string.punctuation))
			# Check the records
			temp_person = get_or_none(Person, name=name)
			if temp_person is None:
				temp_person = Person(
					name=name,
				)
				temp_person.save()
			person_ids[flag] = temp_person

		# Start Processing
		for section in config.sections():
			# Bypass if no faces flag
			if "faces" not in config[section]:
				continue

			# Bypass if file not exist
			file_name_chunk = section.split(".")

			# Make Folder Filter
			dir_q = Q()
			if options["dir"] != "":
				# Process the path
				folders = options["dir"].split("/")
				dir_q = Q(folder__name=folders[-1])
				layer_count = 1
				for folder in reversed(folders[:-1]):
					dir_q &= Q(**{
						f"folder{'__parent'*layer_count}__name": folder
					})
			
			# Query
			picture = get_or_none(File, dir_q, file_name=".".join(file_name_chunk[:-1]), file_ext=file_name_chunk[-1])
			if picture is None:
				self.stdout.write(self.style.ERROR('Could not find the file ' + section))
				continue

			# Process Each Entry
			for info in config[section]["faces"].split(";"):
				picture.tags.add(person_ids[info.split(",")[1]])

		self.stdout.write(self.style.SUCCESS('Successfully scanned the MEDIA_ROOT'))
		
	def add_arguments(self, parser):
		parser.add_argument("--dir", help="directory to scan within MEDIA_ROOT", default="")