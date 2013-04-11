from flask import Flask
from flask import render_template
from flask import request
import search

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def index():
	app.logger.debug("hit")
	if request.method == 'POST':
		app.logger.debug(request.form['search'])
		a_variable = request.form['search']
		return render_template('index.html', a_variable=a_variable)
	if request.method == 'GET':
		try:
			results=search.get_results(request.args.get('search'))
			a_variable = results[0]["hits"]
		except: a_variable=""
		return render_template('index.html', a_variable=a_variable)

   
@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

if __name__ == "__main__":
    app.run(debug=True)