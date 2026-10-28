
"""Courier and parcel tracking system with safer coding practices."""

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

    tracking_id = f"TRK{10001 + len(parcels)}"
    parcels[tracking_id] = {
        "sender": sender,
        "receiver": receiver,
        "weight": weight_kg,
        "status": 0,
        "booked": str(date.today()),
    }
    history.append(tracking_id)
    return tracking_id


def update_status(tracking_id, status_index):
    """Update a parcel's delivery status."""
    if tracking_id not in parcels:
        return False

    if not 0 <= status_index < len(STATUS_FLOW):
        return False

    parcels[tracking_id]["status"] = status_index
    return True


def track_parcel(tracking_id):
    """Return the tracking details of a parcel."""
    parcel = parcels.get(tracking_id)
    if parcel is None:
        return None

    status = STATUS_FLOW[parcel["status"]]
    return f"{parcel['sender']} -> {parcel['receiver']}: {status}"


def with_courier(tracking_id):
    """Check whether a parcel is still with the courier."""
    parcel = parcels.get(tracking_id)
    return parcel is not None and parcel["status"] < 4


def shipping_cost(weight_kg):
    """Calculate shipping cost based on parcel weight."""
    if weight_kg < 0:
        raise ValueError("Parcel weight cannot be negative.")

    return weight_kg * 10 + 40


def label_path():
    """Create a secure temporary file path for a parcel label."""
    with tempfile.NamedTemporaryFile(
        suffix=".txt",
        delete=False,
    ) as label_file:
        return label_file.name


def ping_hub(hub_address):
    """Ping a courier hub without invoking a shell."""
    return subprocess.check_output(
        ["ping", "-c", "1", hub_address],
        text=True,
        timeout=5,
    )


def generate_otp():
    """Generate a cryptographically secure four-digit OTP."""
    return secrets.randbelow(9000) + 1000


def main():
    """Run the parcel tracking demonstration."""
    history = []

    first = book_parcel(
        "Bengaluru Books", "Ravi Kumar", 5.5, history
    )
    second = book_parcel(
        "Gadget Hub", "Sneha Rao", 1, history
    )
    third = book_parcel(
        "Spice Store", "Imran Khan", 10, history
    )

    update_status(first, 2)
    update_status(second, 1)
    update_status(third, 4)

    for tracking_id in history:
        print(track_parcel(tracking_id))
        print("  with courier:", with_courier(tracking_id))
        weight = parcels[tracking_id]["weight"]
        print("  cost:", shipping_cost(weight))

    unknown_id = "TRK00000"
    print(
        "Unknown tracking id",
        track_parcel(unknown_id) or unknown_id,
    )
    print(
        "Delivery OTP for",
        third,
        "is",
        generate_otp(),
    )
    print("Parcels booked today:", len(parcels))


if __name__ == "__main__":
    main()
