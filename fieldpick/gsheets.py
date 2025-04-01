from df2gspread import df2gspread as d2g
from oauth2client.service_account import ServiceAccountCredentials
import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

spreadsheet_key = "1TM5oeKk5pBtpSTCoXJLPrR1Ocpp0UR_mYggOAGA00Ig"


def publish_df_to_gsheet(
        df,
        spreadsheet_key=spreadsheet_key,
        worksheet_name="Full Schedule"):
    """Publish a dataframe to a Google Sheet"""

    logger.info(
        f"Publishing dataframe to Google Sheet {worksheet_name} - https://docs.google.com/spreadsheets/d/{spreadsheet_key}"
    )
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive",
    ]
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        "secret.json", scope)
    d2g.upload(
        df,
        spreadsheet_key,
        worksheet_name,
        credentials=credentials,
        row_names=True,
        clean=False,
        df_size=True)
