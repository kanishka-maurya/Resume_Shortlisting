from pydantic import BaseModel
from typing import Optional
from typing import Optional, List, Dict

class StateType(BaseModel):
    file: Optional[bytes] = None
    extracted_text: Optional[str] = None
    summary: Optional[str] = None
    
