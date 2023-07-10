from flask import Flask, Blueprint, request, make_response, jsonify
from flask_restful import Api, Resource
from restfull import api
import logging
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required

video_blueprint = Blueprint("video_blueprint", __name__)


def main() -> None:
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(pastime)s% (levelness)s% (message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


all_videos = {
    "video1":
    {
        "title": "1st video",
        "views": 25000,
        "comment": "Very good video",
    },

    "video2":
    {
        "title": "2nd video",
        "views": 100,
        "comment": "Average video",
    },
}


class Video(Resource):
    def get(self, video_id):
        try:
            if video_id not in all_videos:
                return make_response(jsonify({'Message': 'This video doesnt exist'}))
            else:
                return all_videos[video_id]
        except Exception as e:
            return make_response(jsonify({'error': str(e)}))

    @jwt_required()
    def delete(self, video_id):
        try:
            if video_id not in all_videos:
                return make_response(jsonify({'Message': 'This video doesnt exist, cant delete it'}))
            else:
                del all_videos[video_id]
                return all_videos
        except Exception as e:
            return make_response(jsonify({'error': str(e)}))

    def post(self, video_id):
        try:
            if video_id in all_videos:
                return make_response(jsonify({'Message': 'This video already exist'}))
            else:
                title = request.json.get("title", "NA")
                views = request.json.get("views", "NA")
                comment = request.json.get("comment", "NA")
                new_dict = {"title": title, "views": views, "comment": comment}
                if title == "NA" or views == "NA" or comment == "NA":
                    return make_response(jsonify({'missing': 'Title or views or comment is missing'}))
                elif title == "" or comment == "":
                    return make_response(jsonify({'alert': 'title or comment cant be blank'}))
                else:
                    all_videos[video_id] = new_dict
                    access_token = create_access_token(identity=title)
                    refresh_token = create_refresh_token(identity=title)
                    return make_response(jsonify({'access_token': str(access_token), 'refresh_token': str(refresh_token), 'message': 'New video has been added successfully'}))
        except Exception as e:
            return make_response(jsonify({"error": str(e)}))

    @jwt_required()
    def put(self, video_id):
        try:

            if video_id not in all_videos:
                return make_response(jsonify({'Message': 'This video doesnt exist'}))
            else:
                title = request.json.get("title", "NA")
                views = request.json.get("views", 0)
                comment = request.json.get("comment", "NA")
                # new_dict = {"title": title, "views": views, "comment": comment}
                title2 = all_videos[video_id]["title"]
                views2 = all_videos[video_id]["views"]
                comment2 = all_videos[video_id]["comment"]
                print(title2,views2,comment2)

                if title not in ["NA",""] :
                    new_dict = {"title": title, "views": views2, "comment": comment2}
                    all_videos[video_id] = new_dict
                    title2 = all_videos[video_id]["title"]
                    views2 = all_videos[video_id]["views"]
                    comment2 = all_videos[video_id]["comment"]

                if views not in [0,""]:
                    new_dict = {"title": title2, "views": views, "comment": comment2}
                    all_videos[video_id] = new_dict
                    title2 = all_videos[video_id]["title"]
                    views2 = all_videos[video_id]["views"]
                    comment2 = all_videos[video_id]["comment"]

                if comment not in ["NA",""]:
                    new_dict = {"title": title2, "views": views2, "comment": comment}
                    all_videos[video_id] = new_dict
                    title2 = all_videos[video_id]["title"]
                    views2 = all_videos[video_id]["views"]
                    comment2 = all_videos[video_id]["comment"]

                return make_response(jsonify({'message': 'New changes has been saved successfully!'}))
        except Exception as e:
            return make_response(jsonify({"error": str(e)}))


class OnlyGet(Resource):
    def get(self):
        return all_videos


api.add_resource(Video, '/<video_id>')
api.add_resource(OnlyGet, '/')

