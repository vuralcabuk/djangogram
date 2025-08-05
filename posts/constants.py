from enum import Enum

class SocialShareStatus(str,Enum):
    PENDING = "pending"
    SHARED = "shared"
    FAILED = "failed"
    
