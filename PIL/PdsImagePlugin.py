#
# The Python Imaging Library
# $Id$
#
# PDS Image Adapter
#
# Copyright (c) 2013 - Austin Godber
#
# See the README file for information on usage and redistribution.
#

__version__ = "0.1"

from PIL import Image, ImageFile


def _accept(prefix):
    """Tests for PDS Image"""
    return prefix[:3] == b"PDS"


class PDSImageFile(ImageFile.ImageFile):
    """PDS Image Support"""
    format = "PDS"
    format_description = "Planetary Data Systems Image Format"

    def _open(self):
        """Open"""
        offset = self.fp.tell()
        if not _accept(self.fp.read(3)):
            raise SyntaxError("Not a PDS file")

        self.fp.seek(offset)

         # Parse Label
        pds_label = self._parse_pds_label()

        self.mode = "F"
        self.size = 1, 1

        self.tile = [("raw", (0, 0, xsize, ysize), self.fp.tell(),
                     (rawmode, 0, 1))]

    def _parse_pds_label(self):
        """Parses PDS Label into a dict"""
        label_dict = {}
        return label_dict


# Register Plugin
Image.register_open("PDS", PDSImageFile, _accept)

Image.register_extension("PDS", ".img")
