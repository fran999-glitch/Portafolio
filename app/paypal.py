import sys

from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment


class PayPalClient:
    def __init__(self):
        self.client_id = "AQnl113UoM83PantvBkn9DstDPiZLh7EtvqS3-MXiKREXzEPOpsoEqcC4qYcW0HoQp26bu_shOxBoZy6"
        self.client_secret = "EHHNULt4FBosoheRdAU5c1XipDpeGffj1ltJdFg6y76y76zrH980gIDs9Et8n6eRQaTk-GFoyNZCOq5P"
        self.environment = SandboxEnvironment(client_id=self.client_id, client_secret=self.client_secret)
        self.client = PayPalHttpClient(self.environment)