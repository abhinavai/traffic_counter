from flask import Flask
from flask import request,jsonify,Response
from flask import Blueprint
from Services.opencv_traffic_counting.traffic import Traffic_counter
import config
import numpy as np


app = Flask(__name__)

count_vehicles_app = Blueprint("count_vehicles_app",__name__)

@count_vehicles_app.route("/count_vehicles",methods=['POST'])

def all_data_of_instance_table():
        data = request.get_json()
        if "IMAGE_DIR" in data.keys() and data["IMAGE_DIR"] is not "" and not data["IMAGE_DIR"].isspace():
            if "VIDEO_SOURCE" in data.keys() and data["VIDEO_SOURCE"] is not "" and not data["VIDEO_SOURCE"].isspace():
                if "EXIT_PTS" in data.keys() and data["EXIT_PTS"] is not "":
                    if "SHAPE" in data.keys() and data["SHAPE"] is not "":
                        print (np.array(data['EXIT_PTS']))
                        data =  Traffic_counter(image_dir=data['IMAGE_DIR'],video_source=data['VIDEO_SOURCE'],exits_pts=np.array(data['EXIT_PTS']),make_video = data['make_and_save_video'],shape=tuple(data['SHAPE'])).start_here()
                        return data
                    else:
                        data = {"success": False,
                            "Message": "(Shape) not found",
                            "data": None
                            }
                        resp = jsonify(data)
                        resp.status_code = 404
                        return resp
                else:
                    data = {"success": False,
                            "Message": "(EXIT_PTS) not valid",
                            "data": None
                            }
                    resp = jsonify(data)
                    resp.status_code = 406
                    return resp
            else:
                data = {"success": False,
                        "Message": "(VIDEO_SOURCE) not valid",
                        "data": None
                        }
                resp = jsonify(data)
                resp.status_code = 406
                return resp
        else:
            data = {"success": False,
                    "Message": "(IMAGE_DIR) not valid",
                    "data": None
                    }
            resp = jsonify(data)
            resp.status_code = 406
            return resp
