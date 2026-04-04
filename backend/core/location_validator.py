from global_land_mask import globe


class LocationValidator:
    @staticmethod
    def validate(latitude: float, longitude: float) -> None:
        if not globe.is_land(latitude, longitude):
            raise ValueError(
                "Selected coordinates are located over water."
            )