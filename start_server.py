from flask import Flask
from flask import render_template
from flask import request
import search

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def index():
# 	app.logger.debug("hit")
	if request.method == 'GET':
		try:
			results=search.get_results(request.args.get('search'))
			a_variable = results
			query="You searched for: "+request.args.get('search')
			app.logger.debug(a_variable)
		except: 
			query=""
			a_variable=''
		return render_template('index.html', a_variable=a_variable, query=query)

   
@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

if __name__ == "__main__":
    app.run(debug=True)