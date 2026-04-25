# cs3980HW4, My Fridge w/ MongoDB

## So sorry for the late submission, I had a lot of trouble getting this assingment working

```bash
python3 -m venv venv
source ../.venv/bin/activate  or  . venv/bin/activate
pip3 install fastapi
pip3 install uvicorn
pip3 install pydantic
pip3 install motor
pip3 install bcrypt
uvicorn main:app --reload
```

Add, display, update, and remove the contents of my kitchen so I can visually track which ingredients I have. Now connected to MongoDB.

Built from the CRUD midterm todo app base with FastAPI.

It's not the most intuitive UI, but it is functional with handling authentication, password encryption, routing, CRUD functions, and connecting to MongoDB.

```bash
pip3 freeze > requirements.txt
```
```bash
uvicorn main:app --reload
```
---
## Screenshots
**Main Page**

![Screenshot1](screenshots/begin_app.png)

**Add info for user account**

![Screenshot2](screenshots/signupentry.png)

**Sign up success**

![Screenshot2](screenshots/signupsuccess.png)

**Adding items**

![Screenshot2](screenshots/additems.png)

**Adding items**

![Screenshot2](screenshots/edit_items.png)

**Changes after updating items**

![Screenshot2](screenshots/afterediteditems.png)

**Changes after deleting items**

![Screenshot2](screenshots/afterdelete.png)

**Items cleared after user logs out**

![Screenshot2](screenshots/logout.png)