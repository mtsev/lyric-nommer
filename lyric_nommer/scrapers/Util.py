# Modified from https://github.com/dmo60/lLyrics/blob/master/lLyrics/Util.py

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

import re
import string

def remove_punctuation(data):
    for c in string.punctuation:
        data = data.replace(c, "")
    data = ' '.join(data.split())
    return data


def bytes_to_string(data):
    encoding = 'utf-8'
    decoded_string = ""
    try:
        partial_string = data.decode(encoding, 'replace')
        try:
            bytes_to_string.charSetRegex = re.compile("charset=\"?([a-zA-Z0-9\\-]*)\"?")
            results = bytes_to_string.charSetRegex.search(partial_string)
            if results is not None:
                encoding = results.group(1)
                decoded_string = data.decode(encoding)
                print("encoding: " + encoding)
            else:
                decoded_string = partial_string
        except:
            print("Fail trying to get declared bytes encoding (charset) using regular expression")
            try:
                encoding = chardet.detect(data)['encoding']
                decoded_string = data.decode(encoding, 'replace')
            except:
                print("could not detect bytes encoding, assume utf-8")
                decoded_string = partial_string
    except:
        print("failed to decode bytes to string")

    return decoded_string