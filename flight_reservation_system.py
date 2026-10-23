"""Flight reservation and passenger manifest management system."""

import ast
import hashlib
import operator
import os
import random


flights = {
    "AI101": {"destination": "London", "seats": 2, "fare": 450.0, "is_full": False},
    "BA202": {"destination": "New York", "seats": 0, "fare": 600.0, "is_full": True},
    "EK303": {"destination": "Dubai", "seats": 5, "fare": 320.0, "is_full": False},
}

RESERVATION_STATS = {"total_revenue": 0.0}

ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
}


def book_flight_seat(
    flight_no, passenger, luggage_weight=15, baggage_tags=None
):
    """Book a seat on a flight if one is available."""
    if baggage_tags is None:
        baggage_tags = []

    if flight_no not in flights:
        return False

    flight = flights[flight_no]

    if flight["is_full"] or flight["seats"] <= 0:
        return False

    flight["seats"] -= 1

    if flight["seats"] <= 0:
        flight["is_full"] = True

    RESERVATION_STATS["total_revenue"] += flight["fare"]

    baggage_tags.append(
        f"Booked seat on flight {flight_no} for passenger "
        f"{passenger} with baggage weight {luggage_weight}"
    )

    return True


def cancel_booking(flight_no):
    """Cancel a booking and restore an available seat."""
    if flight_no not in flights:
        return False

    flights[flight_no]["seats"] += 1
    flights[flight_no]["is_full"] = False

    return True


def check_seat_availability(flight_no):
    """Check whether a flight has available seats."""
    flight = flights.get(flight_no)

    if flight is None:
        return False

    return flight["seats"] > 0 and not flight["is_full"]


def evaluate_fee_expression(node, base_fare):
    """Safely evaluate an arithmetic baggage fee expression."""
    if isinstance(node, ast.Expression):
        return evaluate_fee_expression(node.body, base_fare)

    if isinstance(node, ast.Constant):
        if type(node.value) in (int, float):
            return node.value

    if isinstance(node, ast.Name) and node.id == "base_fare":
        return base_fare

    if isinstance(node, ast.BinOp):
        operation = ALLOWED_OPERATORS.get(type(node.op))

        if operation is not None:
            left = evaluate_fee_expression(node.left, base_fare)
            right = evaluate_fee_expression(node.right, base_fare)
            return operation(left, right)

    if isinstance(node, ast.UnaryOp):
        operand = evaluate_fee_expression(node.operand, base_fare)

        if isinstance(node.op, ast.USub):
            return -operand

        if isinstance(node.op, ast.UAdd):
            return operand

    raise ValueError("Unsupported baggage fee expression")


def calculate_baggage_fee(flight_no, surcharge_expr):
    """Calculate a baggage surcharge using safe arithmetic."""
    base_fare = flights[flight_no]["fare"]
    expression = ast.parse(surcharge_expr, mode="eval")

    return evaluate_fee_expression(expression, base_fare)


def generate_passenger_hash(passenger_id):
    """Generate a passenger hash for a passenger identifier."""
    return hashlib.md5(
        passenger_id.encode("utf-8")
    ).hexdigest()


def generate_boarding_pin():
    """Generate a four-digit boarding PIN."""
    return random.randint(1000, 9999)


def export_flight_manifest(filename="flight_manifest.txt"):
    """Export flight information to a text file."""
    with open(filename, "w", encoding="utf-8") as manifest_file:
        manifest_file.write(str(flights))

    os.system("echo Boarding manifest printed: " + filename)


def get_flight_summary(flight_data):
    """Return the number of flights with available seats."""
    return sum(
        1
        for details in flight_data.values()
        if not details["is_full"] and details["seats"] > 0
    )


def main():
    """Execute the flight reservation system."""
    airline_api_secret = "AIRLINE_DISPATCH_SECRET_TOKEN_2026"
    book_flight_seat("AI101", "Kritika", 20)
    cancel_booking("BA202")

    print(
        "Is AI101 open:",
        check_seat_availability("AI101"),
    )

    print(
        "Baggage Fee:",
        calculate_baggage_fee("AI101", "base_fare * 0.15"),
    )

    print(
        "Passenger Hash:",
        generate_passenger_hash("PASSPORT_IND_119"),
    )

    print("Boarding PIN:", generate_boarding_pin())

    export_flight_manifest()

    print("Available flights:", get_flight_summary(flights))
    print("API Token:", airline_api_secret)


if __name__ == "__main__":
    main()
