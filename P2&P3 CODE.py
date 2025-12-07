import urllib.request
import json
import time
from datetime import datetime, UTC
import random
from dataclasses import dataclass
from pymongo import MongoClient
from abc import ABC, abstractmethod


# -----------------------
# Dataclass for logging entries
# -----------------------
@dataclass
class PriceLog:
    price: float
    status: str
    used_demo: bool
    timestamp: datetime


# -----------------------
# Abstract Base Class
# -----------------------
class WebMonitor(ABC):

    def __init__(self, name: str, interval_seconds: int = 5):
        self.name = name
        self.interval_seconds = interval_seconds

    def log(self, message: str):
        """Simple console logger with timestamp."""
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}")

    @abstractmethod
    def check_once(self):
        """To be implemented in child class."""
        pass

    def run_for_n_checks(self, n: int):
        """Run monitor for N cycles instead of forever."""
        self.log(f"{self.name} started")
        for _ in range(n):
            self.check_once()
            time.sleep(self.interval_seconds)


# -----------------------
# Gold Price Monitor Class
# -----------------------
class GoldPriceMonitor(WebMonitor):

    API_URL = "https://api.exchangerate.host/convert?from=XAU&to=USD"

    def __init__(self, low_alert, high_alert, mongo_uri):
        super().__init__("Gold Price Monitor", interval_seconds=5)
        self.low_alert = low_alert
        self.high_alert = high_alert

        # MongoDB connection
        self.client = MongoClient(
            mongo_uri,
            tlsAllowInvalidCertificates=True   # required for macOS certificate issues
        )

        self.db = self.client["gold_monitor_db"]
        self.collection = self.db["gold_price_logs"]

    # API fetch function
    def fetch_price(self):
        try:
            with urllib.request.urlopen(self.API_URL, timeout=10) as r:
                data = json.loads(r.read().decode())
                return float(data["result"])
        except Exception as e:
            self.log(f"API error: {e}")
            return None

    # Demo price generator
    def generate_demo_price(self):
        return round(random.uniform(self.low_alert * 0.85, self.high_alert * 1.15), 2)

    # MongoDB save function
    def save_to_db(self, entry: PriceLog):
        try:
            self.collection.insert_one(entry.__dict__)
        except Exception as e:
            self.log(f"DB error: {e}")

    # Main checking logic
    def check_once(self):
        real_price = self.fetch_price()

        if real_price is None:
            price = self.generate_demo_price()
            used_demo = True
            self.log(f"Using demo price {price}")
        else:
            price = real_price
            used_demo = False

        # Determine status
        if price < self.low_alert:
            status = "LOW"
        elif price > self.high_alert:
            status = "HIGH"
        else:
            status = "NORMAL"

        self.log(f"XAU/USD {price} -> {status}")

        # Save entry to MongoDB
        entry = PriceLog(
            price=price,
            status=status,
            used_demo=used_demo,
            timestamp=datetime.now(UTC)
        )
        self.save_to_db(entry)


# -----------------------
# MAIN PROGRAM
# -----------------------
def main():

    print("Gold Price Monitor Project (P2–P3)\n")

    low = int(input("Low alert (default 2200): ") or "2200")
    high = int(input("High alert (default 2600): ") or "2600")
    checks = int(input("How many checks? (default 10): ") or "10")

    # YOUR REAL MONGODB URI
    mongo_uri = "mongodb+srv://2309015858_db_user:zaq1zaq1@apwp2and3.mj9eph0.mongodb.net/gold_monitor_db?retryWrites=true&w=majority&appName=APWP2and3"

    monitor = GoldPriceMonitor(low, high, mongo_uri)
    monitor.run_for_n_checks(checks)


if __name__ == "__main__":
    main()
