from typing import List, Optional
from datetime import datetime
from app.models.user import User, UserCreate, UserUpdate, UserInDB

class UserService:
    def __init__(self):
        # 임시 메모리 저장소 (나중에 데이터베이스로 교체)
        self.users_db: List[UserInDB] = []
        self.next_id = 1
    
    def create_user(self, user: UserCreate) -> User:
        user_in_db = UserInDB(
            id=self.next_id,
            name=user.name,
            email=user.email,
            created_at=datetime.now(),
            is_active=True
        )
        self.users_db.append(user_in_db)
        self.next_id += 1
        return User(**user_in_db.dict())
    
    def get_user(self, user_id: int) -> Optional[User]:
        for user in self.users_db:
            if user.id == user_id:
                return User(**user.dict())
        return None
    
    def get_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        users = self.users_db[skip: skip + limit]
        return [User(**user.dict()) for user in users]
    
    def update_user(self, user_id: int, user_update: UserUpdate) -> Optional[User]:
        for i, user in enumerate(self.users_db):
            if user.id == user_id:
                update_data = user_update.dict(exclude_unset=True)
                updated_user = user.copy(update=update_data)
                self.users_db[i] = updated_user
                return User(**updated_user.dict())
        return None
    
    def delete_user(self, user_id: int) -> bool:
        for i, user in enumerate(self.users_db):
            if user.id == user_id:
                del self.users_db[i]
                return True
        return False