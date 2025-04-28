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

# @app.route("/api/friends/<int:id>", methods=["GET"])
# def get_friend():
#     friend = Friend.query.get(id)
#     if friend is None:
#         return jsonify({"error":"friend does not exits!"}),404
#     return jsonify(friend.to_json()),200
# @app.route("/api/friends/<int:id>", methods=["GET"], strict_slashes=False)
# def get_friend(id):
#     friend = Friend.query.get(id)
#     if friend is None:
#         return jsonify({"error": "Friend not found"}), 404
#     return jsonify(friend.to_json()), 200

#create a friend 
@app.route("/api/friends", methods=["POST"])
def create_friend():
    try:
        # get data from the request body
        data = request.json

        requried_fields = ["name","gender","role","description"]
        for field in requried_fields:
            if field not in data:
             return jsonify({f"msg":"{field} field is required"}), 201  

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
    
#delete
@app.route("/api/friends/<int:id>", methods = ["DELETE","PATCH"])
def handle_friend(id):
    friend = Friend.query.get(id)
    if friend is None:
        return jsonify({"error":"Friend not found !"}),404
    if request.method == "DELETE":
        try:
            db.session.delete(friend)
            db.session.commit()
            return jsonify({"msg":"Friend deleted successfully"}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"error":str(e)}), 500 
    elif request.method == "PATCH":
        try:
        # get the specific from the request body
            data = request.get_json(force=True)
            # get the name from request body, if no name has been past, use the original name of the friend
            friend.name = data.get("name", friend.name)
            friend.gender = data.get("gender",friend.gender)
            friend.role = data.get("role",friend.role)
            friend.description = data.get("description",friend.description)
            db.session.commit()
            return jsonify({"msg":"Friend Updated successfully"}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"error":str(e)}), 500



# def delete_freind(id):

    
# #update a friend 
# @app.route("/api/friends/<int:id>", methods=["PATCH"])
# def update_friend(id):

    

    


    