from pydantic import BaseModel, EmailStr, Field, field_validator

class RegisterRequest(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)

class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=128)

class HomeRequest(BaseModel):
    budget: int = Field(gt=0, le=10_000_000)
    rooms: list[str] = Field(min_length=1, max_length=10)
    style: str = Field(default="Modern", max_length=50)
    location: str = Field(default="India", max_length=100)
    priorities: list[str] = Field(default_factory=list)

    @field_validator("rooms", "priorities")
    @classmethod
    def clean_lists(cls, value):
        return [x.strip() for x in value if x and x.strip()]

class PartyRequest(BaseModel):
    budget: int = Field(gt=0, le=10_000_000)
    guests: int = Field(gt=0, le=10_000)
    event_type: str = Field(min_length=2, max_length=80)
    venue: str = Field(default="Flexible", max_length=100)
    location: str = Field(default="India", max_length=100)
    food_preference: str = Field(default="Mixed", max_length=50)

class JewelryRequest(BaseModel):
    budget: int = Field(gt=0, le=10_000_000)
    occasion: str = Field(min_length=2, max_length=100)
    style: str = Field(default="Elegant", max_length=50)
    metal: str = Field(default="Any", max_length=50)
    outfit_description: str = Field(default="", max_length=1000)
