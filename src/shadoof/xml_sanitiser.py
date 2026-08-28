"""Some tools for sanitising xml."""

import re


def sanitise_xml(xml_str):
    """Sanitise xml string."""
    output = millisecond_remover(xml_str)
    output = divisor_remover(output)
    return output


def millisecond_remover(xml_str):
    """Remove millisecond timestamps."""
    return re.sub(
        r"<T>(\d{4}-\d\d-\d\d \d\d:\d\d:\d\d).\d+<\/T>", r"<T>\1<\/T>", xml_str
    )


def divisor_remover(xml_str, replacement=1):
    """
    Remove divisor value.

    Divisors are used by whurl to interpret the data sensibly, but we ignore them bceause we want data in the
    nonsensicle format that hilltop desires.

    It overwrites the divisor in the whurl object, so if we do anything with divisors in the future gonna have to do
    a proper fix, but this works for now.
    """
    return re.sub(
        r"<Divisor>.*</Divisor>", rf"<Divisor>{str(replacement)}</Divisor>", xml_str
    )
