from dataclasses import dataclass
from datetime import datetime
from typing import Text

DATE_FORMAT: Text = "%d-%b-%Y %H:%M:%S"


@dataclass
class Ticket:
    ticket_number: int
    spot_number: int
    entry_datetime: datetime

    def __str__(self) -> Text:
        return (
            f"Parking Ticket:\n\tTicket Number: {'{0:03}'.format(self.ticket_number)}\n"
            f"\tSpot Number: {self.spot_number}\n"
            f"\tEntry Date-time: {self.entry_datetime.strftime(DATE_FORMAT)}"
        )


@dataclass
class Receipt:
    receipt_number: int
    entry_datetime: datetime
    exit_datetime: datetime
    fees_paid: float

    def __str__(self) -> Text:
        return (
            f"Parking Receipt:\n\tReceipt Number: R-{'{0:03}'.format(self.receipt_number)}\n"
            f"\tEntry Date-time: {self.entry_datetime.strftime(DATE_FORMAT)}\n"
            f"\tExit Date-time: {self.exit_datetime.strftime(DATE_FORMAT)}\n"
            f"\tFees: {self.fees_paid}"
        )
