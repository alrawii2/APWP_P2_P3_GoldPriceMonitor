Gold Price Monitor – P2 & P3 Project

Advanced Programming with Python
Istinye University – Software Engineering

Project Description

This project monitors the live gold price (XAU/USD) and categorizes it into:

LOW

NORMAL

HIGH

The threshold values are set by the user at runtime.
If the API fails, the program uses a built-in demo price generator, so it always works.

The system saves each result (price, status, demo flag, timestamp) into a MongoDB Atlas database, earning full bonus marks for external DB integration.

Features

✔ Live API request for gold price
✔ Automatic fallback demo price
✔ Status detection (LOW, NORMAL, HIGH)
✔ Saves all results to MongoDB Atlas
✔ Organized object-oriented Python code
✔ Fully documented, easy to read
✔ Works on VS Code, macOS, Windows, and Linux

Technologies Used

Python 3

pymongo (MongoDB driver)

urllib (API request)

random (demo price fallback)

MongoDB Atlas Cloud Database

How to Run the Project

Install requirements:

pip install pymongo dnspython


Open VS Code

Open the folder containing the project

Run the program:

python3 P2&P3 CODE.py


Enter:

Low alert

High alert

Number of checks

Check MongoDB Atlas → your database updates every run.

MongoDB Connection

The project uses your URI:

mongodb+srv://2309015858_db_user:zaq1zaq1@apwp2and3.mj9eph0.mongodb.net/?retryWrites=true&w=majority&tlsAllowInvalidCertificates=true


Database name:

gold_monitor


Collection name:

history

Expected Output

Example console output:

Gold Price Monitor Project (P2–P3)
[2025-12-07 01:41:01] XAU/USD 2876.32 -> HIGH


And MongoDB document:

{
  "price": 2876.32,
  "status": "HIGH",
  "demo_used": true,
  "timestamp": "2025-12-07T01:41:01"
}
