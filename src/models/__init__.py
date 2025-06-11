from pydantic import BaseModel


class EnrollmentRequest(BaseModel):
    numberOfEnrollments: int