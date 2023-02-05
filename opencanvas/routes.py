from flask import request 

from opencanvas import app, db
from opencanvas.models import Pixel, User


@app.route("/")
def hello():
    return "welcome to open-canvas. ✨"



@app.route("/pixel/set", methods=['POST'])
def set_pixel():
    """
    set new color of given pixel

    params:
    x:      x'th co-ordinate of the canvas.
    y:      y'th co-ordinate of the canvas.
    color:  new color of the pixel.
    """

    body = request.get_json()

    pixel = Pixel (
        x = body['x'],
        y = body['y'],
        color = body['color'],
        user = body['user']
    )
    db.session.add(pixel)
    db.session.commit()
    
    return { "msg": f"pixel {body['x'], body['y']} set to color: {body['color']}" }



@app.route("/signup", methods=['POST'])
def signup():
    """
    add new user to db

    params:
    username:
    password:
    """

    body = request.get_json()
    
    user = User (
        username = body['username'],
        password = body['password'],
    )

    try:
        # check if username exists 
        # TODO: there might be a simpler way to query username, instead of creating a where stmt.
        username_exist_check = db.session.execute(db.select(User.username).where(User.username == user.username)).first()
        
        if not username_exist_check:
            db.session.add(user)
            db.session.commit()
            return { "msg": f"added user {body['username']}" }
        return { "msg": "username already exists" }

    except:
        return { "msg": "error adding user" }