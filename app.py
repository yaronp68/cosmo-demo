from flask import Flask, request,render_template, url_for
from flask.ext.restful import Resource, Api, reqparse
from pygtail import Pygtail
from celery import Celery


app = Flask(__name__)
api = Api(app)

file_name = "example.log"

celery = Celery(broker='amqp://10.0.0.5//')


class CosmoTemplateProgress(Resource):
    def get(self):
    	out_string = ""
    	for line in Pygtail(file_name):
    		out_string += line + '\n'
        return out_string

class CosmoTemplateRunner(Resource):
    def get(self):
    	parser = reqparse.RequestParser()
    	parser.add_argument('template')
    	args = parser.parse_args()
    	file_name = 'logs/' + args['template'] + '.log'
    	# call the celery task here to get the parser running
    	celery.send_task("hello")
    	return file_name


#serve the widget html file
@app.route("/widget")
def view_widget():
	#url_for('static', filename='index.html')
	return render_template('index.html')

api.add_resource(CosmoTemplateRunner, '/runner')
api.add_resource(CosmoTemplateProgress, '/progress')

if __name__ == '__main__':
    app.run(debug=True)
