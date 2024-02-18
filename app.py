from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from py_model import UserResponse, UserCreate, ProductResponse, ProductCreate
from alchemy_models import Product, User, get_db
from starlette.responses import JSONResponse

from tasks import fill_users, fill_products
from typing import List

# init fast api app
app = FastAPI()

app.add_middleware(CORSMiddleware,
                   allow_origins=["*"],
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"],
                   )


# crud operation for User model
# @app.get("/users/{user_id}", response_model=UserResponse)
# def read_users(user_id: int, db: Session = Depends(get_db)):
#     user = db.query(User).filter(User.id == user_id).first()
#     if user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return user

@app.get("/users/", response_model=List[UserResponse])
def read_users(db: Session = Depends(get_db)):
    user = db.query(User).all()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.post("/users/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@app.put("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    db.query(User).filter(User.id == user_id).update(user.model_dump(), synchronize_session=False)

    db.commit()
    db.refresh(db_user)
    return db_user


@app.delete("/users/{user_id}", response_model=UserResponse)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(db_user)
    db.commit()
    return db_user


# crud operation for Product model
@app.get("/product/", response_model=List[ProductResponse])
def read_products(db: Session = Depends(get_db)):
    product = db.query(Product).all()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@app.post("/product/", response_model=ProductResponse)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    db_product = Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


@app.put("/product/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, product: ProductCreate, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.id == product_id).first()

    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    db.query(Product).filter(Product.id == product_id).update(product.model_dump(), synchronize_session=False)

    db.commit()
    db.refresh(db_product)
    return db_product


@app.delete("/product/{product_id}", response_model=ProductResponse)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.id == product_id).first()

    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    db.delete(db_product)
    db.commit()
    return db_product


# @app.get("/")
# def test_json():
#     data = {
#         "user_id": 1,
#         "user": "Toha",
#         "email": "mak.anton87@gmail.com"
#     }
#     return JSONResponse(data)


@app.get("/fill_users/")
def fill_users_task(bgt: BackgroundTasks):
    bgt.add_task(fill_users)
    return JSONResponse({"task_1": "Users"})


@app.get("/fill_products/")
def fill_products_task(bgt: BackgroundTasks):
    bgt.add_task(fill_products)
    return JSONResponse({"task_2": "Products"})


if __name__ == "__main__":
    import uvicorn
    from alchemy_models import SessionLocal

    uvicorn.run(app, host="127.0.0.1", port=8000)
