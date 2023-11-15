import hashlib
from io import BytesIO
from typing import Union

from segmentation.base import GazetteSegment


class AssociationSegmenter:
    def __init__(self, association_gazette: str):
        self.association_gazette = association_gazette

    def get_gazette_segments(self, *args, **kwargs) -> list[GazetteSegment]:
        """
        Returns a list of GazetteSegment
        """
        raise NotImplementedError

    def split_text_by_territory(self) -> Union[dict[str, str], list[str]]:
        """
        Segment a association text by territory
        and returns a list of text segments
        """
        raise NotImplementedError

    def build_segment(self, *args, **kwargs) -> GazetteSegment:
        """
        Returns a GazetteSegment
        """
        raise NotImplementedError

    def get_checksum(self, source_text: str) -> str:
        """Calculate the md5 checksum of text
        by creating a file-like object without reading its
        whole content in memory.

        Example
        -------
        >>> extractor.get_checksum("A simple text")
            'ef313f200597d0a1749533ba6aeb002e'
        """
        file = BytesIO(source_text.encode(encoding="UTF-8"))

        m = hashlib.md5()
        while True:
            d = file.read(8096)
            if not d:
                break
            m.update(d)
        return m.hexdigest()
