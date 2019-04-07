# Modified from https://github.com/dmo60/lLyrics/blob/master/lLyrics/DarklyricsParser.py
# Parser for darklyrics.com

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import urllib.request, urllib.error, urllib.parse
import string
import re
import logging

from . import util

class Parser(object):
    def __init__(self, artist, title):
        self.artist = artist
        self.title = title
        self.lyrics = ""
        self.log = logging.getLogger(__name__)

    def parse(self):
        # remove unwanted characters from artist and title strings
        clean_artist = self.artist.lower()
        clean_artist = util.remove_punctuation(clean_artist)
        clean_artist = clean_artist.replace(" ", "")

        # create artist Url
        url = "http://www.darklyrics.com/" + clean_artist[:1] + "/" + clean_artist + ".html"
        self.log.debug("darklyrics artist Url " + url)
        try:
            resp = urllib.request.urlopen(url, None, 3).read()
        except:
            self.log.debug("could not connect to darklyrics.com")
            return ""

        resp = util.bytes_to_string(resp)

        # find title with lyrics url
        match = re.search("<a href=\"\.\.(.*?)\">" + self.title + "</a><br />", resp, re.I)
        if match is None:
            self.log.debug("could not find title: " + self.title)
            return ""
        url = "http://www.darklyrics.com" + match.group(1)
        self.log.debug("darklyrics Url " + url)
        try:
            resp = urllib.request.urlopen(url, None, 3).read()
        except:
            self.log.debug("could not connect to darklyrics.com")
            return ""

        resp = util.bytes_to_string(resp)

        self.track_no = url.split("#")[1]

        self.lyrics = self.get_lyrics(resp)
        self.lyrics = string.capwords(self.lyrics, "\n").strip()

        return self.lyrics

    def get_lyrics(self, resp):
        # search for the relevant lyrics
        match = re.search("<h3><a name=\"" + self.track_no + "\">" + self.track_no + "\. " + self.title + "</a></h3>",
                          resp, re.I)
        if match is None:
            self.log.debug("lyrics start not found")
            return ""
        start = match.end()
        resp = resp[start:]

        end = resp.find("<h3><a name")
        if end == -1:
            # case lyrics are the last ones on the page
            end = resp.find("<div ")
        if end == -1:
            self.log.debug("lyrics end not found")
            return ""

        resp = resp[:end]

        # replace unwanted parts
        resp = resp.replace("<br />", "")
        resp = resp.replace("<i>", "")
        resp = resp.replace("</i>", "")

        return resp
