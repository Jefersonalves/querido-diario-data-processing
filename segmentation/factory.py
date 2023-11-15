from typing import Any

from segmentation.base import AssociationSegmenter
from segmentation.segmenters import ALAssociacaoMunicipiosSegmenter


def get_segmenter(association_gazzete: dict[str, Any]) -> AssociationSegmenter:
    """
    Factory method to return a AssociationSegmenter

    Example
    -------
    >>> association_gazette = {
        "territory_name": "al_associacao_municipios",
        "created_at": datetime.datetime.now(),
        "date": datetime.datetime.now(),
        "edition_number": 1,
        "file_path": 'raw/pdf.pdf',
        "file_url": 'localhost:8000/raw/pdf.pdf',
        "is_extra_edition": True,
        "power": 'executive',
        "scraped_at": datetime.datetime.now(),
        "state_code": 'AL',
        "source_text": texto,
    }
    >>> from segmentation import get_segmenter
    >>> segmenter = get_segmenter(association_gazette)
    >>> segments = segmenter.get_gazette_segments()

    Notes
    -----
    This method implements a factory method pattern.
    See: https://github.com/faif/python-patterns/blob/master/patterns/creational/factory.py
    """

    association_name = association_gazzete["territory_name"]
    segmenters = {
        "al_associacao_municipios": ALAssociacaoMunicipiosSegmenter,
    }

    return segmenters[association_name](association_gazzete)
