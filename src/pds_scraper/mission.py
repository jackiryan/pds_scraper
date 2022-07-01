"""
The MIT License (MIT)

Copyright (c) 2022, Jacqueline Ryan

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
_MARS2020 = "mars2020"
_MSL = "msl"
_MERA = "mera"
_MERB = "merb"

# Known by NAIF integer code -168
_MARS2020_NAMES = ["PERSEVERANCE", "MARS 2020", "MARS2020", "M2020", "M20", "PERCY"]
# Known by NAIF integer code -76
_MSL_NAMES = ["CURIOSITY", "MSL", "MARS SCIENCE LABORATORY"]
# Known by NAIF integer code -253
_MERB_NAMES = ["OPPORTUNITY", "MER-1", "MER 1", "MER-B", "MER - B", "MER B", "MARS EXPLORATION ROVER - B", "OPPY"]
# Known by NAIF integer code -254
_MERA_NAMES = ["SPIRIT", "MER-2", "MER 2", "MER-A", "MER - A", "MER A", "MARS EXPLORATION ROVER - A"]


def check_mission(mission: str) -> str:
    """
    Rough implementation of a check that is done in SPICE to determine
    which mission is being referred to based on name. Simply match the
    unicode string to a list of acceptable inputs.

    :param mission: A string containing the name of the mission of interest.
    :return: A string containing the name of that mission's directory in the PDS imaging node.
    """
    m = mission.encode("utf-8").upper()
    if m in _MARS2020_NAMES:
        return _MARS2020
    elif m in _MSL_NAMES:
        return _MSL
    elif m in _MERA_NAMES:
        return _MERA
    elif m in _MERB_NAMES:
        return _MERB
    else:
        # If a mission hasn't been included in this list, pass it through and hope
        # the user knows what they are talking about.
        return m.lower()