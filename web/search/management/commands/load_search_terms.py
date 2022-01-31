"""Management utility to load search terms from a CSV file."""

from bidnamic.load_data import LoadDataCommand
from search.models import SearchTerm


class Command(LoadDataCommand):

    help = "Loads search terms from a CSV file."
    model = SearchTerm
