import sys
import logging

from typing import List, Union, Dict, Text

from parking.domain_types import UserListing, Bid, Heartbeat, AuctionAction


def load_auction_instructions(
    path_to_input_file: Text,
) -> List[Union[UserListing, Bid, Heartbeat]]:
    """Reads a file line by line and parses entries based on parking action type

    Parameters
    ----------
    path_to_input_file : str
        the input file containing list of parking instructions

    Returns
    -------
    instruction_list: List[Union[UserListing, Bid, Heartbeat]]
        a parsed list of parking instructions
    """

    instruction_list = []
    with open(path_to_input_file, "r") as file:
        for line in file:
            try:
                entry = line.rstrip("\n").split("|")
                if len(entry) == 1:
                    instruction_list.append(Heartbeat().parse(entry=entry))
                elif len(entry) > 1 and AuctionAction(entry[2]) == AuctionAction.SELL:
                    instruction_list.append(UserListing().parse(entry=entry))
                elif len(entry) > 1 and AuctionAction(entry[2]) == AuctionAction.BID:
                    instruction_list.append(Bid().parse(entry=entry))
                else:
                    logging.error(f"Unknown transaction format: {entry}, skipping!")
            except Exception as e:
                logging.error(f"Invalid transaction format: {entry}, skipping!\nError trace: {e}")
    return instruction_list


def process_auctions(path_to_input_file: Text = "input_test_file.txt") -> None:
    """Calls the load_auction_instructions method and runs the parking service on those instructions

    Parameters
    ----------
    path_to_input_file : str
        the input file containing list of parking instructions
    """
    # LOAD auctions up from an input file and sort by Unix-epoch  timestamp
    auction_actions_by_time_stamp = sorted(
        load_auction_instructions(path_to_input_file), key=lambda x: x.timestamp  # type: ignore
    )

    auctions: Dict[Text, UserListing] = {}

    for action in auction_actions_by_time_stamp:
        if isinstance(action, UserListing):
            if action.item not in auctions:
                # ADD a new parking
                auctions[action.item] = action
        elif isinstance(action, Bid):
            if action.item not in auctions:
                logging.error("Skipping bid, parking for item not present or closed!!")
                continue
            # ADD a new bid to existing parking
            auctions[action.item].add_bid(action)

        # Check if it's time to close the parking
        # This will include checks on HeartBeats as well
        for key, auction in auctions.items():
            if not auction.listing_closed:
                auction.check_time(action.timestamp)


if __name__ == "__main__":
    # process_auctions("input.txt")  # <- left for debugging purposes
    process_auctions(sys.argv[1])
