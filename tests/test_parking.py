import pytest

from parking.__main__ import process_auctions
from parking.domain_types import UserListing, AuctionStatus, Bid


# This is the base case for the Thought Machine test


def create_auction_with_bids_that_sells():
    entry_one = ["10", "1", "SELL", "toaster_1", "10.00", "20"]
    entry_two = ["12", "8", "BID", "toaster_1", "7.50"]
    entry_three = ["13", "5", "BID", "toaster_1", "12.50"]
    user_listing = UserListing().parse(entry_one)
    user_listing.add_bid(Bid().parse(entry_two))
    user_listing.add_bid(Bid().parse(entry_three))
    return user_listing


def test_user_listing_valid_parse():
    entry = ["10", "1", "SELL", "toaster_1", "10.00", "20"]
    user_listing = UserListing().parse(entry)
    assert isinstance(user_listing, UserListing)
    assert user_listing.status == AuctionStatus.UNSOLD


def test_user_listing_parse_on_empty_raises():
    entry = []
    with pytest.raises(IndexError, match="Passed entry length is invalid"):
        UserListing().parse(entry)


def test_user_listing_wrong_auction_action_type_raises():
    entry = ["10", "1", "BID", "toaster_1", "10.00", "20"]
    with pytest.raises(TypeError, match="Auction action should be a SELL"):
        UserListing().parse(entry)


def test_user_listing_invalid_auction_action_type_raises():
    entry = ["10", "1", "XYZ", "toaster_1", "10.00", "20"]
    with pytest.raises(ValueError, match="Unknown parking type"):
        UserListing().parse(entry)


def test_user_listing_add_valid_bid_appends_to_placed_bids_list():
    user_listing = create_auction_with_bids_that_sells()
    assert len(user_listing.placed_bids) > 1


def test_user_listing_check_time_after_close_time_closes_auction():
    user_listing = create_auction_with_bids_that_sells()
    user_listing.check_time(21)

    assert user_listing.listing_closed


def test_user_listing_check_time_after_close_time_sets_expected_pricing():
    user_listing = create_auction_with_bids_that_sells()
    user_listing.check_time(20)

    expected_second_best_price = 10.00
    expected_highest_bid = 12.50

    assert user_listing.second_best_price == expected_second_best_price
    assert user_listing.price_paid == expected_second_best_price
    assert user_listing.reserve_price == expected_second_best_price
    assert user_listing.max_bid_amount == expected_highest_bid


def test_user_listing_check_time_after_close_time_sets_auction_to_sold():
    user_listing = create_auction_with_bids_that_sells()
    user_listing.check_time(40)

    assert user_listing.status == AuctionStatus.SOLD
