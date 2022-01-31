"""Management utility to load data from a CSV file."""

import os
import pandas as pd
from django.db.models import Model
from django.core.management.base import BaseCommand, CommandError


class LoadDataCommand(BaseCommand):

    model: Model

    def add_arguments(self, parser):
        parser.add_argument(
            "-f",
            "--file",
            type=str,
            help="The path to the CSV file containing the data to load.",
        )

    @staticmethod
    def get_file(parsed_args: dict) -> str:
        """If the user has not provided a file as an argument, then prompt
        them for the file path. Check the files exists before returning the
        filepath. If it does not exist, raise an error.

        Args:
            parsed_args: The arguments parsed from the command line.

        Returns:
            The path to the CSV file.
        """
        _file = parsed_args["file"]

        if _file is None:
            _file = input("Enter the path to the CSV file: ")

        if not os.path.exists(_file):
            raise CommandError("File does not exist.")

        return _file

    @staticmethod
    def read_csv(filepath: str) -> pd.DataFrame:
        """Read the CSV file and return the data as a pandas dataframe.

        Args:
            filepath: The path to the CSV file.

        Returns:
            The data as a pandas dataframe.
        """
        return pd.read_csv(filepath)

    def load_data(self, parsed_args: dict) -> None:
        """Load the data from the CSV file into the database.

        Args:
            parsed_args: The arguments parsed from the command line.

        Returns:
            None
        """
        filepath = self.get_file(parsed_args)
        df = self.read_csv(filepath)
        self.model.load_from_dataframe(df)

    def handle(self, *args, **options):
        """Main handler for running the command from the command line."""
        self.load_data(options)
