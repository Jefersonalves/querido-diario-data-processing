import json
import re
import unicodedata
from datetime import date, datetime
import hashlib
from io import BytesIO


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


class GazetteSegment:
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

    def __init__(self, municipio: str, texto: str):
        self.territory_name = municipio
        self.source_text = texto.rstrip()
        self.date = self._get_publication_date(texto)
        self.edition_number = self._get_edition_number(texto)
        self.is_extra_edition = False
        self.power = "executive_legislative"
        self.file_checksum = self.md5sum(BytesIO(self.source_text.encode(encoding='UTF-8')))
        self.scraped_at = datetime.utcnow()
        self.created_at = self.scraped_at
        self.processed = True

    def _get_edition_number(self, texto: str) -> str:
        match = re.search(r"Nº (\d+)", texto)
        if match:
            return match.group(1)
        return None

    def _get_publication_date(self, texto: str):
        match = re.findall(
            r".*(\d{2}) de (\w*) de (\d{4})", texto, re.MULTILINE)[0]
        mes = GazetteSegment._mapa_meses[match[1]]
        return date(year=int(match[2]), month=mes, day=int(match[0]))

    def md5sum(self, file):
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
