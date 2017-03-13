
from flask import Flask 
from flask import request
from flask import jsonify



from flask_redis import FlaskRedis 

app = Flask(__name__)
redis_store = FlaskRedis(app)

@app.route('/')
def index():
	return 'Home to the remote logger'


@app.route('/logerror',methods=['POST','GET'])
def logerror():
	if request.method == 'POST':
		log = request.get_json(force=True)
		#print(log)
		redis_store.rpush("errors",str(log))
		
		return "Log saved",201
	else:
		all_logs = redis_store.lrange("errors",0,-1)
		all_logs_str = [item.decode('utf-8') for item in  all_logs]
		
		return jsonify(all_logs_str)


@app.route('/clearerror')
def clearerror():
	redis_store.delete("errors")
	return 'Deleted',200





if __name__ == '__main__':
	app.run()

