from flask import request, make_response, jsonify
from flask import render_template

import hashlib

from opencanvas import app, db
from opencanvas.models import Pixel, User


# CONSTANTS
class canvas:
    WIDTH = 20
    HEIGHT = 20


@app.route("/")
def hello():
    return render_template('home.html')
    # return "welcome to open-canvas. ✨"

@app.route("/canvas/size")
def get_canvas_size():
    """get canvas size"""

    return make_response(jsonify({ 'width': canvas.WIDTH, 'height': canvas.HEIGHT }), 200)



@app.route("/canvas")
def get_canvas():
    pixels = db.session.execute(db.select(Pixel.color).order_by(Pixel.x, Pixel.y)).scalars()

    canvas_data = []
    temp_canvas_data = [pixel for pixel in pixels]

    for y in range(canvas.HEIGHT):
        canvas_data.append(temp_canvas_data[y*canvas.WIDTH: (y*canvas.WIDTH) + canvas.WIDTH])
    
    return make_response(jsonify({"size": [canvas.HEIGHT, canvas.WIDTH], "data": canvas_data}), 200)




@app.route("/pixel/set", methods=['POST'])
def set_pixel():
    """
    set new color of given pixel

    params:
    x:      x'th co-ordinate of the canvas.
    y:      y'th co-ordinate of the canvas.
    color:  new color of the pixel.
    user:   user that last modified this pixel.
    """

    body = request.get_json()

    if not (body['x'] > canvas.WIDTH or body['y'] > canvas.HEIGHT):
        pixel = Pixel.query.get((body['x'], body['y']))
        pixel.color = body['color']
        pixel.user = body['user']

        db.session.commit()
        
        return make_response(jsonify({ "msg": f"pixel {body['x'], body['y']} set to color: {body['color']}" }), 200) 
    return { "msg": f"pixel range out of bounds." }, 422



# create a plain canvas of some color
@app.route("/pixels/populate", methods=['POST'])
def populate_pixels():
    """
    initialize canvas and pixels in db with one color

    params:
    color:  color of the pixels to be set in the db.
    user:
    """

    body = request.get_json()

    canvas_data = []
    for i in range(canvas.WIDTH):
        for j in range(canvas.HEIGHT):
            temp_pixel = Pixel (
                x = i,
                y = j,
                color = body['color'],
                user = body['user'],
            )

            canvas_data.append(temp_pixel)

    db.session.bulk_save_objects(canvas_data)
    db.session.commit()
    
    return { "msg": f"created canvas of size ({canvas.WIDTH, canvas.HEIGHT})" }




@app.route("/signup", methods=['POST'])
def signup():
    """
    add new user to db

    params:
    username: primary key
    password:
    """

    body = request.get_json()

    # hash password
    encoded_password = body['password'].encode()
    hashed_password = hashlib.sha256(encoded_password).hexdigest()

    user = User (
        username = body['username'],
        password = hashed_password,
    )

    try:
        # check if username exists 
        # TODO: there might be a simpler way to query username (since its a pk), instead of creating a where stmt.
        # username_exist_check = db.session.execute(db.select(User.username).where(User.username == user.username)).first()
        username_exist_check = db.session.get(User, user.username)
        
        if not username_exist_check:
            db.session.add(user)
            db.session.commit()
            return { "msg": f"added user {body['username']}" }
        return { "msg": "username already exists" }

    except:
        return { "msg": "error adding user" }




@app.route("/login", methods=['POST'])
def login():
    """
    authenticate existing user

    username:
    password:
    """

    body = request.get_json()

    # hash password
    encoded_password = body['password'].encode()
    hashed_password = hashlib.sha256(encoded_password).hexdigest()

    # check if user exists
    user = db.session.get(User, body['username'])
    if user:
        if user.password == hashed_password:
            return { "msg": "User logged in succesfully."}
    return {"msg": "username/password is incorrect."}
