from segmentation.base import AssociationSegmenter
from segmentation.segmenters import ALAssociacaoMunicipiosSegmenter

def get_segmenter(association_name: str, association_source_text) -> AssociationSegmenter:
    """
    Factory method to return a AssociationSegmenter

    Example
    -------
    >>> from segmentation.segmenter_factory import get_segmenter
    >>> segmenter = get_segmenter("al_associacao_municipios", association_source_text)
    >>> segmenter.get_gazette_segments()

    Notes
    -----
    This method implements a factory method pattern.
    See: https://github.com/faif/python-patterns/blob/master/patterns/creational/factory.py
    """
    
    segmenters = {
        "al_associacao_municipios": ALAssociacaoMunicipiosSegmenter,
    }

    return segmenters[association_name](association_source_text)
