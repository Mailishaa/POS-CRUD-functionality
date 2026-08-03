from pydantic import BaseModel, ConfigDict

class CategoryBase(BaseModel):
    category_name: str
    description: str = None  
    parent_category_id: int = None  
    is_active: bool = True

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    category_name: str = None
    description: str = None  
    parent_category_id: int = None  
    is_active: bool = None

class CategoryRead(CategoryBase):
    model_config = ConfigDict(from_attributes=True)

    category_id: int
