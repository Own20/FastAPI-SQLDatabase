#Create initial Pydantic models / schemas
#Create an /ItemBase/ and /UserBase/ Pydantic models (or let's say "schemas") to have common attributes while creating or reading data.
#And create an /ItemCreate/ and /UserCreate/ that inherit from them (so they will have the same attributes), plus any additional data (attributes) needed for creation.
#So, the user will also have a /password/ when creating it.
#But for security, the /password/ won't be in other Pydantic models, for example, it won't be sent from the API when reading a user.
from pydantic import BaseModel


class ItemBase(BaseModel):
    title: str
    description: str | None = None


class ItemCreate(ItemBase):
    pass


#Create Pydantic models / schemas for reading / returning
#Pydantic models (schemas) used when reading data, when returning it from the API.
#For example, before creating an item, we don't know what will be the ID assigned to it, but when reading it (when returning it from the API) we will already know its ID.
#The same way, when reading a user, we can now declare that items will contain the /items/ that belong to this user.
#Not only the IDs of those items, but all the data that we defined in the Pydantic model for reading items: /Item/.
class Item(ItemBase):
    id: int
    owner_id: int

    #Use Pydantic's orm_mode
    #This /Config/ class is used to provide configurations to Pydantic.
    class Config:
        orm_mode = True
    #Pydantic's /orm_mode/ will tell the Pydantic model to read the data even if it is not a /dict/, but an ORM model (or any other arbitrary object with attributes).


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    items: list[Item] = []

    class Config:
        orm_mode = True