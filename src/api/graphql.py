import os
from fastapi import FastAPI, Depends, HTTPException
from fastapi.graphql import GraphQLApp
from graphene import ObjectType, String, Int, Float, List, Field, Schema, Mutation
from passlib.context import CryptContext

# Sample data models
class User(ObjectType):
    id = Int()
    username = String()
    email = String()
    full_name = String()

class Transaction(ObjectType):
    id = Int()
    user_id = Int()
    amount = Float()
    description = String()

# Sample in-memory data storage (replace with a database in production)
users_db = {}
transactions_db = {}

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Utility functions
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

# GraphQL Queries
class Query(ObjectType):
    users = List(User)
    transactions = List(Transaction)

    def resolve_users(self, info):
        return list(users_db.values())

    def resolve_transactions(self, info):
        return list(transactions_db.values())

# GraphQL Mutations
class CreateUser (Mutation):
    class Arguments:
        id = Int(required=True)
        username = String(required=True)
        email = String(required=True)
        full_name = String(required=False)
        password = String(required=True)

    user = Field(User)

    def mutate(self, info, id, username, email, full_name, password):
        if id in users_db:
            raise HTTPException(status_code=400, detail="User  already exists")
        hashed_password = get_password_hash(password)
        user = User(id=id, username=username, email=email, full_name=full_name)
        users_db[id] = user
        return CreateUser (user=user)

class CreateTransaction(Mutation):
    class Arguments:
        id = Int(required=True)
        user_id = Int(required=True)
        amount = Float(required=True)
        description = String(required=True)

    transaction = Field(Transaction)

    def mutate(self, info, id, user_id, amount, description):
        transaction = Transaction(id=id, user_id=user_id, amount=amount, description=description)
        transactions_db[id] = transaction
        return CreateTransaction(transaction=transaction)

# GraphQL Schema
class Mutation(ObjectType):
    create_user = CreateUser .Field()
    create_transaction = CreateTransaction.Field()

schema = Schema(query=Query, mutation=Mutation)

# Initialize FastAPI app
app = FastAPI(title="GFMS-Core GraphQL API", version="1.0.0")

# Add GraphQL endpoint
app.add_route("/graphql", GraphQLApp(schema=schema))

# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=os.getenv("HOST", "0.0.0.0"), port=int(os.getenv("PORT", 8000)))
