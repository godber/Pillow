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
import re
from collections import OrderedDict

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

        print "".join(pds_label['_raw'])

        self.mode = "F"
        self.size = 1, 1

        self.tile = [("raw", (0, 0, xsize, ysize), self.fp.tell(),
                     (rawmode, 0, 1))]

    def _parse_pds_label(self):
        """Parses PDS Label into a dict"""
        label_dict = OrderedDict({'_raw': []})

        # TODO: This RE is a little tight, I should allow for whitespace
        label_end = re.compile(r"^END\r$")
        # Open the file again in non-binary mode to parse the PDS Label
        # self.fp.readline() didn't return lines, presumably because it was in
        # binary mode
        # TODO: don't read through the full file, stop at the end of the label
        with open(self.fp.name, 'r') as f:
            for line in f:
                if label_end.match(line):
                    break
                label_dict['_raw'].append(line)
                #print line.strip()

        return label_dict


# Register Plugin
Image.register_open("PDS", PDSImageFile, _accept)

Image.register_extension("PDS", ".img")
