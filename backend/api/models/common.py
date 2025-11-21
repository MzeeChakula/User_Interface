from enum import Enum
from pydantic import BaseModel, Field, ConfigDict

class Region(str, Enum):
    """Uganda regions"""
    CENTRAL = "Central Uganda (Buganda)"
    WESTERN = "Western Uganda (Ankole, Tooro, Kigezi, Bunyoro)"
    EASTERN = "Eastern Uganda (Busoga, Bugisu, Teso)"
    NORTHERN = "Northern Uganda (Acholi, Lango, Karamoja, West Nile)"

class Condition(str, Enum):
    """Health conditions"""
    HYPERTENSION = "Hypertension"
    UNDERNUTRITION = "Undernutrition"
    ANEMIA = "Anemia"
    FRAILTY = "Frailty"
    DIGESTIVE = "Digestive issues"
    ARTHRITIS = "Arthritis"
    OSTEOPOROSIS = "Osteoporosis"
    DIABETES = "Diabetes"

class AgeGroup(str, Enum):
    """Age groups"""
    SIXTY_TO_SEVENTY = "60-70"
    SEVENTY_TO_EIGHTY = "70-80"
    EIGHTY_PLUS = "80+"

class Season(str, Enum):
    """Seasons"""
    DRY = "Dry"
    WET = "Wet"
