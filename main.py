
from fastapi import FastAPI
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi.responses import HTMLResponse

app = FastAPI()

# MongoDB setup
client = AsyncIOMotorClient('mongodb://49.207.240.252:27017/neuro')
db = client['neuro']
collection = db['labs']


class User(BaseModel):
    name: str
    age: int

@app.on_event("startup")
async def startup_db():
  
    pass

@app.post("/add_user/")
async def add_user(user: User):
 
    await collection.insert_one(user.dict())
    return {"message": "User added successfully"}

@app.get("/app", response_class=HTMLResponse)
async def read_html():
   
    html_content = """
    <html>
        <head>
           
            <script>
                async function fetchData() {
                    const response = await fetch('/get_users/');
                    const data = await response.json();
                    let table = '<table><tr><th>Name</th><th>Age</th></tr>';
                    data.forEach(user => {
                        table += `<tr><td>${user.name}</td><td>${user.age}</td></tr>`;
                    });
                    table += '</table>';
                    document.getElementById('user-data').innerHTML = table;
                }
            </script>
        </head>
        <body>
            <h1>Users from MongoDB</h1>
            <div id="user-data"></div>
            <button onclick="fetchData()">Load Users</button>
        </body>
    </html>
    """
    return html_content

@app.get("/get_users/")
async def get_users():
    
    users = []
    async for user in collection.find():
        users.append({"name": user["name"], "age": user["age"]})
    return users


