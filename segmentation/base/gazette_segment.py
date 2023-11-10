from datetime import date, datetime
from dataclasses import dataclass


@dataclass
class GazetteSegment:
    """
    Dataclass to represent a gazette segment of a association
    related to a city
    """
    territory_name: str
    source_text: str
    date: date
    edition_number: str
    is_extra_edition: bool
    power: str
    file_checksum: str
    scraped_at: datetime
    created_at: datetime
    processed: bool
