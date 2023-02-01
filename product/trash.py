"""
class Location(db.Model):
    __tablename__ = "location"
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(200), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    type = db.Column(db.String(20), nullable=False)

    def __init__(self, address, latitude, longitude, type):
        self.address = address
        self.latitude = latitude
        self.longitude = longitude
        self.type = type
        
class LocationManager:
    @staticmethod
    def create(address, latitude, longitude, type):
        location = Location(address=address, latitude=latitude, longitude=longitude, type=type)
        db.session.add(location)
        db.session.commit()
        return location

    @staticmethod
    def get(location_id):
        return Location.query.get(location_id)



from ..models import Driver
from datetime import datetime, timedelta
from haversine import haversine
def estimate_time_to_destination(driver_id: str, restaurant_id: str, customer_id: str) -> str:
    driver = Driver.query.get(driver_id)
    if not driver:
        raise ValueError("Driver not found")
    #uncomment this when you import Restaurant table
    #restaurant = Restaurant.query.get(restaurant_id)
    #if not restaurant:
        #raise ValueError("Restaurant not found")
    #uncomment this when you import customer table
    customer = Customer.query.get(customer_id)
    if not customer:
        raise ValueError("Customer not found")

    # Get the driving distance and duration between the restaurant and customer location
    #uncomment this when you import resturant
    restaurant_location = (restaurant.latitude, restaurant.longitude)
    customer_location = (customer.latitude, customer.longitude)
    distance = haversine(restaurant_location, customer_location)
    speed = 40  # assume average speed of 40km/h
    duration = distance / speed * 60 * 60  # in seconds
    # Calculate the estimated time of arrival
    current_time = datetime.utcnow()
    estimated_time_of_arrival = current_time + timedelta(seconds=duration)
    return estimated_time_of_arrival.strftime("%Y-%m-%d %H:%M:%S")
"""