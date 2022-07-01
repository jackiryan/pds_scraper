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
import urllib.parse
import re
import requests


# Copy of the Django URL validation regex, cited from:
# https://github.com/django/django/blob/stable/1.3.x/django/core/validators.py#L45
_URLREGEX = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

# A copy of the above regex specifically for identifying domain names only.
_DOMAINREGEX = re.compile(
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', re.IGNORECASE) # ...or ip

class ResourceNotFoundError(Exception):
    pass

def check_url(value: str, check_exists=True) -> str:
    """
    :param value: str containing an unvalidated URL input.
    :return: The validated URL string. It may have an origin string
             appended to the hostname.
    """
    out_url = value.encode("utf-8")

    # Use the super complicated regex from Django to validate the URL.
    isValidURL = re.match(_URLREGEX, value) is not None
    isValidDomain = re.match(_DOMAINREGEX, value) is not None
    if not isValidURL and isValidDomain:
        # The address is valid, but missing an origin string.
        # Append https by default. If this fails to connect, an exception will be thrown.
        out_url = urllib.parse.urlunparse(("https", str(value), "", "", "", ""))
    elif not isValidURL and not isValidDomain:
        raise ResourceNotFoundError(f"The given node name: {value} does not describe a URL or hostname.")
    
    if check_exists:
        response = requests.head(out_url, allow_redirects=True)
        if response.status_code == 200:
            return out_url
        else:
            raise ResourceNotFoundError(f"The given node name: {out_url} could not be found. Please check the connection and try again.")

    return out_url