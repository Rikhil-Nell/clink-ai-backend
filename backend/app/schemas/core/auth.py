from pydantic import BaseModel

class AuthData(BaseModel):
    user_id: int
    loyalty_program_id: int