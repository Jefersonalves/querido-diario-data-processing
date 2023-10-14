import json
import re
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
class CityGazetteSegment:
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
    def __init__(self, city_text):
        self.source_text = city_text
    
    def get_city_segment(self, city: str, city_text: str) -> CityGazetteSegment:
        raise NotImplementedError
    
    def get_checksum(self, file):
        """Calculate the md5 checksum of a file-like object without reading its
        whole content in memory.
        from io import BytesIO
        md5sum(BytesIO(b'file content to hash'))
        '784406af91dd5a54fbb9c84c2236595a'
        """
        m = hashlib.md5()
        while True:
            d = file.read(8096)
            if not d:
                break
            m.update(d)
        return m.hexdigest()

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id

    def __str__(self):
        return dict(self.__dict__)


class ALAssociacaoMunicipiosExtractor(GazetteSegmentExtractor):
    _mapa_meses = {
        "Janeiro": 1,
        "Fevereiro": 2,
        "Março": 3,
        "Abril": 4,
        "Maio": 5,
        "Junho": 6,
        "Julho": 7,
        "Agosto": 8,
        "Setembro": 9,
        "Outubro": 10,
        "Novembro": 11,
        "Dezembro": 12,
    }

    def get_city_segment(self, city: str, city_text: str):
        territory_name = city
        source_text = city_text.rstrip()
        date = self._get_publication_date(city_text)
        edition_number = self._get_edition_number(city_text)
        is_extra_edition = False
        power = "executive_legislative"
        file_checksum = self.get_checksum(BytesIO(self.source_text.encode(encoding='UTF-8')))
        utc_now = datetime.utcnow()
        processed = True
        
        return CityGazetteSegment(
            territory_name=territory_name,
            source_text=source_text,
            date=date,
            edition_number=edition_number,
            is_extra_edition=is_extra_edition,
            power=power,
            file_checksum=file_checksum,
            scraped_at=utc_now,
            created_at=utc_now,
            processed=processed,
        )

    def _get_edition_number(self, texto: str) -> str:
        match = re.search(r"Nº (\d+)", texto)
        if match:
            return match.group(1)
        return None

    def _get_publication_date(self, texto: str):
        match = re.findall(
            r".*(\d{2}) de (\w*) de (\d{4})", texto, re.MULTILINE)[0]
        mes = self._mapa_meses[match[1]]
        return date(year=int(match[2]), month=mes, day=int(match[0]))
