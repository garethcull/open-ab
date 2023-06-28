from flask import Flask,render_template,jsonify,request,json,make_response,session,redirect,url_for
import openab_helper

# Flask App Setup
app = Flask(__name__)
app.config['SECRET_KEY'] = 'abtesting4life'

'''
*********************************************************
*                                                       *
*          Main Routes for open-ab                      *
*                                                       *
*********************************************************
'''

@app.route('/open-ab')
def test_ab_view():

    # Set the templates you want to render here, with how often (%) you want each to appear using randomize values
    templates = {
        "pages": ["variationA.html", "variationB.html", "variationC.html"],
        "randomize": [0.34, 0.33, 0.33]
    }

    # Choose random template based on above config
    template = openab_helper.choose_random_template(templates)

    # Render template on route
    return template


if __name__ == '__main__':
    app.run()