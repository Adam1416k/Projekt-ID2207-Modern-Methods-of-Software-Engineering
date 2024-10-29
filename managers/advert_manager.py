import json
from datetime import datetime
from models import Advert

class AdvertManager: 
    def __init__(self, storage_file="adverts.json"):
        self.storage_file = storage_file
        self.adverts = self.load_adverts()  # Load adverts from file


    """------------ SET AND GET FROM JSON FILE ---------------"""

    def save_advert(self):
        """Save adverts to a JSON file."""
        with open(self.storage_file, "w") as f:
            json.dump([self.serialize_advert(advert) for advert in self.adverts], f)
        print("Ads saved to JSON.")

    def load_adverts(self):
        """Load adverts from a JSON file."""
        try:
            with open(self.storage_file, "r") as f:
                adverts_data = json.load(f)
                print("Adverts loaded from JSON.")
                return [self.deserialize_advert(advert) for advert in adverts_data]
        except (FileNotFoundError, json.JSONDecodeError):
            print("No adverts file found or JSON error.")
            return []



    """ ------------  ADDS NEW Advert  ------------  """ 

    def add_advert(self, advert):
        """Adds a new advert if there is no advert with the same name."""
        self.adverts.append(advert)
        self.save_advert()  # Ensure the new advert is saved immediately
        return True


    """ ------------  SERIALIZE advert FOR STORAGE TO JSON ------------ """

    def serialize_advert(self, advert):
        """Convert an Advert object to a serializable dictionary."""
        return {
            "position": advert.position,
            "start_date": advert.start_date.isoformat(),
            "coverage": advert.coverage,
            "experience": advert.experience,
            "hr_comment": advert.hr_comment,
            "status": advert.status,
        }

    def deserialize_advert(self, data):
        """Convert a dictionary back to an Advert object."""
        return Advert(
            position=data.get("position", ""),
            start_date=data.get("start_date", ""),
            coverage=data.get("coverage", ""),
            experience=data.get("experience", ""),
            hr_comment=data.get("hr_comment", []),
            status=data.get("status", "Created")
        )
