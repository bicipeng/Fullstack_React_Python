from app import app, db
from flask import request, jsonify
from models import Friend


#get all friends
@app.route("/api/friends", methods=["GET"])
def get_friends():
    friends = Friend.query.all()
    # for each friend{} in the friends list, convert them to json and store in the list
    result = [friend.to_json() for friend in friends]
    return jsonify(result)

@app.route("/api/friends/id", methods=["GET"])
def get_friend():
    friend = Friend.query.one()

#create a friend 
@app.route("/api/friends", methods=["POST"])
def create_friend():
    try:
        # get data from the request body
        data = request.json
        name = data.get("name")
        gender = data.get("gender")
        role = data.get("role")
        description = data.get("description")
        if gender == "female":
            img_url = f"https://avatar.iran.run/public/girl?username={name}"
        elif gender == "male":
            img_url = f"https://avatar.iran.run/public/boy?username={name}"
        else:
            img_url = None
        
        new_friend = Friend(name = name, role=role,gender=gender, description= description, img_url= img_url)
        db.session.add(new_friend)
        db.session.commit()
        return jsonify({"msg":"Friend created successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error":str(e)}), 500
    

    


    