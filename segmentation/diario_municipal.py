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


class Diario:

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

    def __init__(self, municipio: Municipio, cabecalho: str, texto: str):
        self.territory_name = municipio.nome
        self.source_text = texto.rstrip()
        self.date = self._extrai_data_publicacao(cabecalho)
        self.edition_number = cabecalho.split("Nº")[1].strip()
        self.is_extra_edition = False
        self.power = "executive_legislative"
        self.file_checksum = self.md5sum(BytesIO(self.source_text.encode(encoding='UTF-8')))
        self.scraped_at = datetime.utcnow()
        self.created_at = self.scraped_at
        # file_endpoint = gazette_text_extraction.get_file_endpoint()
        self.processed = True

    def _extrai_data_publicacao(self, ama_header: str):
        match = re.findall(
            r".*(\d{2}) de (\w*) de (\d{4})", ama_header, re.MULTILINE)[0]
        mes = Diario._mapa_meses[match[1]]
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
