"""Management utility to load campaigns from a CSV file."""

from bidnamic.load_data import LoadDataCommand
from campaigns.models import Campaign


class Command(LoadDataCommand):

    help = "Loads campaigns from a CSV file."
    model = Campaign
