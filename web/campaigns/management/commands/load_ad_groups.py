"""Management utility to load ad groups from a CSV file."""

from bidnamic.load_data import LoadDataCommand
from campaigns.models import AdGroup


class Command(LoadDataCommand):

    help = "Loads ad groups from a CSV file."
    model = AdGroup
