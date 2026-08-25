"""Adds an audit trail for a dsn copy consistent with copying the individual xml/hts files."""

import datetime
import getpass
import re
from pathlib import Path

import pyodbc
import whurl


def get_audit_dict(whurl_measurement):
    """Get audit details in desired dict format."""
    return {
            "site": whurl_measurement.site_name,
            "data_source": whurl_measurement.data_source.name,
            "ts_type": whurl_measurement.data_source.ts_type,
            "start_date": whurl_measurement.data.timeseries.index[0],
            "end_date": whurl_measurement.data.timeseries.index[-1],
        }


def get_whurl_audit(whurl_root):
    """Get the details from a whurl object, returns details for audit."""
    details = []
    for meas in whurl_root.measurement:
        details.append(get_audit_dict(meas))
    return details


def get_audit_destination(hts_destination):
    """Gets the audit destination from an hts file."""
    audit_destination = str(Path(hts_destination).with_suffix(".accdb"))
    if not Path(audit_destination).exists():
        raise FileNotFoundError(f"The audit file {audit_destination} does not exist.")
    return audit_destination


def write_to_access_for_single_copy(source, destination):
    """Adds an audit trail for copying an individual xml/hts file."""
    root = whurl.schemas.responses.GetDataResponse.from_xml(source)
    for transaction in get_whurl_audit(root):
        write_access_row(
            get_audit_destination(destination),
            transaction["site"],
            transaction["data_source"],
            transaction["ts_type"],
            transaction["start_date"],
            transaction["end_date"],
            source,
        )


def write_access_row(
    access_file, site, data_source, ts_type, start_date, end_date, source
):
    """Write a single access audit entry."""
    connection_string = (
        "DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=" + access_file + ";"
    )
    cnxn = pyodbc.connect(connection_string)

    insert_query = """
        INSERT INTO Audit ("Date","UserName","Process","Site","DataSource","TsType","StartDate","EndDate","Comment")
        VALUES (?,?,?,?,?,?,?,?,?);
    """
    values = (
        datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        getpass.getuser(),
        "Copy from Site",
        site,
        data_source,
        ts_type,
        start_date,
        end_date,
        source,
    )

    cursor = cnxn.cursor()
    print(values)  # Actually good to have some feedback - not just a debug print
    cursor.execute(insert_query, values)
    cursor.commit()

    cursor.close()
    cnxn.close()


def write_to_access_for_dsn(source_dsn, destination):
    """Parse dsn or other file to turn it into auditing instructions."""
    with open(source_dsn) as file:
        dsn_text = file.read()
    regex = re.compile(r'File\d*="(.*)"')
    source_file = regex.findall(dsn_text)
    for path in source_file:
        if Path(path).suffix == ".dsn":
            write_to_access_for_dsn(path, destination)
        else:
            write_to_access_for_single_copy(path, destination)
