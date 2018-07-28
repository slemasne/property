from flask import Flask, render_template, request
from functions import Property, datetime_now

app = Flask(__name__)

@app.route('/index')
def index():
   return render_template('index.html')

@app.route('/test',methods = ["POST","GET"])
def test():
	pass

@app.route('/result', methods = ["POST","GET"])
def result():
	try:
		request.method == "POST"
		postcode = request.form['city']
		beds = request.form['beds']
		checked = request.form.getlist('checked') 
		prop_data = Property(postcode, beds=beds)
		listing_count = prop_data.listing_count()
		if not checked:
			df = prop_data.basic_table()
		else:
			df = prop_data.table_with_rent()
		return render_template('postcode.html', datetime=datetime_now(), table = df.to_html(classes="table-striped"), 
								postcode = postcode, listing_count = listing_count, beds = beds)
	except KeyError:
		print ("Page has failed - please go back")

if __name__ == '__main__':
	app.debug = True
	app.run()
	app.run(debug = True)
