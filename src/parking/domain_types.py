from enum import Enum
from typing import List, Text, Optional, Union


class AuctionAction(Enum):
    SELL = "SELL"
    BID = "BID"


class AuctionStatus(Enum):
    SOLD = "SOLD"
    UNSOLD = "UNSOLD"


class Bid:
    """Class for keeping track parking bids"""

    timestamp: int
    """is an integer representing a Unix-epoch time and is the time of the bid;"""

    user_id: int

    item: Text
    """is a unique string code for that item"""

    bid_amount: float
    """is a decimal representing a bid in the parking site's local currency."""

    def __lt__(self, other: "Bid") -> bool:
        """add an implementation for the comparison operator so the list would allow sorting"""
        return self.bid_amount < other.bid_amount

    def parse(self, entry: List[Union[Text, int, float]]) -> "Bid":
        """parses an entry of possible values to a Bid instance

        Parameters
        ----------
        entry: List[Union[Text, int, float]]
            an entry read from an input file that signifies a new bid added on a given parking

        Returns
        -------
        an instance of Bid initialised to the values from the entry parameter
        """
        err_msg = "Correct format e.g. : '12', '8', 'BID', 'toaster_1', '7.50'\n"

        try:
            if AuctionAction(entry[2]) != AuctionAction.BID:
                raise TypeError("Auction action should be a BID")

            self.timestamp = int(entry[0])
            self.user_id = int(entry[1])
            self.item = str(entry[3])
            self.bid_amount = float(entry[4])
            if len(entry) > 5:
                raise IndexError("Too many attributes added to entry")
            return self
        except TypeError as e:
            raise TypeError(f"Wrong types! {err_msg} error trace: {str(e)}")
        except IndexError as e:
            raise IndexError(f"Passed entry length is invalid! {err_msg} error trace: {str(e)}")
        except ValueError as e:
            raise ValueError(f"Unknown parking type! error trace: {str(e)}")
        except Exception as e:
            raise IndexError(f"Unknown Error: error trace: {str(e)}")


class UserListing:
    """Class for keeping track parking user listings"""

    """is an integer representing a Unix-epoch time and is the parking start time;"""
    timestamp: int

    user_id: int

    """is a unique string code for that item"""
    item: Text

    """is a decimal representing the item reserve price in the site's local currency;"""
    reserve_price: float

    """is an integer representing a Unix-epoch time."""
    close_time: int

    status: AuctionStatus = AuctionStatus.UNSOLD

    price_paid: float = 0

    total_bid_count: int = 0

    lowest_bid: float = 0

    highest_bid_user: Optional[int] = None

    placed_bids: Optional[List[Bid]] = None

    second_best_price: float = 0

    max_bid_amount: float = 0

    reserve_price_met: bool = False

    listing_closed: bool = False

    def check_time(self, time_stamp: int) -> None:
        """checks up on possible closing time of the UserListing/parking in hand.
            If yes, closes the parking and sets the winner with the highest bid if there is any.

        Parameters
        ----------
        time_stamp: int
            a unix-epoch instant in a given parking's lifetime
        """
        if time_stamp >= self.close_time:

            if self.reserve_price_met:
                self.price_paid = self.second_best_price
                self.status = AuctionStatus.SOLD

            self.listing_closed = True
            self.print_auction_state()

    def add_bid(self, bid: Bid) -> None:
        """adds a bid instance to the list of placed bids of this user listing,
            based on specified conditions

        Parameters
        ----------
        bid: Bid
            the bid instance to be added if conditions are met
        """
        if not self.placed_bids:
            self.placed_bids = []

        if self.timestamp <= bid.timestamp <= self.close_time:
            self.total_bid_count += 1
            if bid.bid_amount > self.max_bid_amount:
                self.reserve_price_met = bid.bid_amount >= self.reserve_price

                self.second_best_price = (
                    self.max_bid_amount
                    if self.max_bid_amount > self.reserve_price
                    else self.reserve_price
                )

                self.max_bid_amount = bid.bid_amount
                self.highest_bid_user = bid.user_id
            self.placed_bids.append(bid)

    def parse(self, entry: List[Union[Text, int, float]]) -> "UserListing":
        """parses an entry of possible values to a UserListing instance

        Parameters
        ----------
        entry: List[Union[Text, int, float]]
            an entry read from an input file that signifies the opening on an parking sell

        Returns
        -------
        an instance of UserListing initialised to the values from the entry parameter
        """
        err_msg = "Correct format e.g. : '10', '1', 'SELL', 'toaster_1', '10.00', '20'\n"

        try:
            if AuctionAction(entry[2]) != AuctionAction.SELL:
                raise TypeError("Auction action should be a SELL")

            self.timestamp = int(entry[0])
            self.user_id = int(entry[1])
            self.item = str(entry[3])
            self.reserve_price = float(entry[4])
            self.close_time = int(entry[5])
            if len(entry) > 6:
                raise IndexError("Too many attributes added to entry")
            return self
        except TypeError as e:
            raise TypeError(f"Wrong types! {err_msg} error trace: {str(e)}")
        except IndexError as e:
            raise IndexError(f"Passed entry length is invalid! {err_msg} error trace: {str(e)}")
        except ValueError as e:
            raise ValueError(f"Unknown parking type! error trace: {str(e)}")
        except Exception as e:
            raise IndexError(f"Unknown Error: error trace: {str(e)}")

    def print_auction_state(self) -> None:
        """
        Prints to stdout
        ----------------
            a given state of an parking once its closed, in the form of:
                close_time|item|user_id|status|price_paid|total_bid_count|highest_bid|lowest_bid
        """

        lowest_bid = (
            "{:.2f}".format(min(self.placed_bids).bid_amount) if self.placed_bids else "0.00"
        )

        price_paid = "{:.2f}".format(self.price_paid)

        print(
            f"{self.close_time}|{self.item}|{self.highest_bid_user or ''}|{self.status}"
            f"|{price_paid}|{self.total_bid_count}|{self.max_bid_amount}|{lowest_bid}"
        )


class Heartbeat:
    """Class for keeping track parking heartbeats"""

    timestamp: int
    """is an integer representing a Unix epoch time."""

    def parse(self, entry: List[Text]) -> "Heartbeat":
        """parses an entry of possible values to a Heartbeat instance

        Parameters
        ----------
        entry: List[Union[Text, int, float]]
            an entry read from an input file that signifies a heartbeat in an parking sell

        Returns
        -------
        an instance of Heartbeat initialised to the value from the entry parameter
        """
        err_msg = "Correct format e.g. : '12'\n"
        try:
            self.timestamp = int(entry[0])
            return self
        except TypeError as e:
            raise TypeError(f"Wrong type! {err_msg} error trace: {str(e)}")
        except IndexError as e:
            raise IndexError(f"Passed entry is empty {err_msg} error trace: {str(e)}")
