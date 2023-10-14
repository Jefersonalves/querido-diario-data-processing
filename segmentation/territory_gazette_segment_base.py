import json
import unicodedata
from datetime import date, datetime
import hashlib
from io import BytesIO
from dataclasses import dataclass


class Municipio:
    def __init__(self, municipio):
        self.id = self._computa_id(municipio)
        self.nome = municipio

    def _computa_id(self, nome_municipio):
        ret = nome_municipio.strip().lower().replace(" ", "-")
        ret = unicodedata.normalize('NFKD', ret)
        ret = ret.encode('ASCII', 'ignore').decode("utf-8")
        return ret

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id

    def __str__(self):
        return json.dumps(self.__dict__, indent=2, default=str, ensure_ascii=False)


@dataclass
class TerritoryGazetteSegment:
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


class GazetteSegmentExtractor:
    """
    Given a gazette text from a territory, returns a TerritoryGazetteSegment object
    """
    def __init__(self, territory, source_text):
        self.territory = territory
        self.source_text = source_text
    
    def get_territory_segment(self) -> TerritoryGazetteSegment:
        raise NotImplementedError
    
    def get_checksum(self):
        """Calculate the md5 checksum of text
        by creating a file-like object without reading its
        whole content in memory.
        
        Example
        -------
        >>> extractor = GazetteSegmentExtractor("cidade", "A simple text")
        >>> extractor.get_checksum()
            'ef313f200597d0a1749533ba6aeb002e'
        """
        file = BytesIO(self.source_text.encode(encoding='UTF-8'))

        m = hashlib.md5()
        while True:
            d = file.read(8096)
            if not d:
                break
            m.update(d)
        return m.hexdigest()
