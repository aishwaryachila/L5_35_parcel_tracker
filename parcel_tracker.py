
"""Manage parcel bookings, delivery status, tracking, and shipping costs."""

import os
import secrets
import subprocess
import tempfile
from datetime import date

STATUS_FLOW = [
    "Booked",
    "Picked Up",
    "In Transit",
    "Out for Delivery",
    "Delivered",
]

parcels = {}


def book_parcel(sender, receiver, weight_kg, history=None):
    """Book a parcel and return its tracking ID."""
    if history is None:
        history = []

    tracking_id = "TRK" + str(10001 + len(parcels))
    parcels[tracking_id] = {
        "sender": sender,
        "receiver": receiver,
        "weight": weight_kg,
        "status": 0,
        "booked": str(date.today()),
    }
    history.append(tracking_id)
    return tracking_id


def advance_status(tracking_id):
    """Advance a parcel to its next delivery status."""
    parcel = parcels[tracking_id]
    if parcel["status"] < len(STATUS_FLOW) - 1:
        parcel["status"] += 1
    return STATUS_FLOW[parcel["status"]]


def shipping_cost(weight_kg):
    """Calculate shipping cost based on parcel weight."""
    cost = 50
    if weight_kg > 1:
        cost += (weight_kg - 1) * 30
    return round(cost, 2)


def track_parcel(tracking_id):
    """Return the route and delivery status of a parcel."""
    try:
        parcel = parcels[tracking_id]
    except KeyError:
        return "Unknown tracking id " + tracking_id

    route = parcel["sender"] + " -> " + parcel["receiver"]
    return route + ": " + STATUS_FLOW[parcel["status"]]


def is_with_courier(tracking_id):
    """Check whether a parcel is picked up or in transit."""
    status = STATUS_FLOW[parcels[tracking_id]["status"]]
    return status in ("Picked Up", "In Transit")


def label_path():
    """Create a secure temporary file and return its path."""
    with tempfile.NamedTemporaryFile(
        suffix=".txt", delete=False
    ) as temporary_file:
        return temporary_file.name


def ping_hub(hub_address):
    """Ping a hub once and return the command output."""
    ping_option = "-n" if os.name == "nt" else "-c"
    return subprocess.check_output(
        ["ping", ping_option, "1", hub_address],
        text=True,
    )


def main():
    """Run a demonstration of the parcel-tracking system."""
    first = book_parcel("Bengaluru Books", "Ravi Kumar", 2.5)
    second = book_parcel("Gadget Hub", "Sneha Rao", 0.8)
    third = book_parcel("Spice Store", "Imran Khan", 4)

    advance_status(first)
    advance_status(first)
    advance_status(second)

    for _ in range(6):
        advance_status(third)

    for tracking_id in (first, second, third):
        print(track_parcel(tracking_id))
        print("  with courier:", is_with_courier(tracking_id))
        print("  cost:", shipping_cost(parcels[tracking_id]["weight"]))

    print(track_parcel("TRK00000"))  # Unknown ID
    delivery_otp = secrets.randbelow(9000) + 1000
    print("Delivery OTP for", third, "is", delivery_otp)
    print("Parcels booked today:", len(parcels))


if __name__ == "__main__":
    main()
