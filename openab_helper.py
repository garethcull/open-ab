from flask import Flask,render_template,jsonify,request,json,make_response,session,redirect,url_for
import random

def choose_random_template(templates):

    """

    Background:
        This function returns a random template. If the user has already seen a template, they will get the
        same one due to a cookie that is set on the user which assigns the random page to be viewed for
        subsequent visits

    :param
        templates (obj): Contains a list of pages and a list of respective weights to be randomized
    :return:
        response: Render the random template that was chosen or already assigned
    """

    # Check if the user has a cookie for the assigned page
    assigned_page = request.cookies.get('assigned_ab_page')

    # If the user doesn't have a an assigned ab page, randomly serve a page and set the cookie for future sessions
    if not assigned_page:

        # Set pages and weights for template to be chosen
        pages = templates["pages"]
        weights = templates["randomize"]

        # Choose a random template based on the list of ab templates and provided weights
        template_to_serve = random.choices(pages, weights, k=1)[0]

        # make_response and return the template
        response = make_response(render_template(template_to_serve))

        # **** Uncomment to enable ***** > Set a cookie to always show this page for future sessions
        # response.set_cookie('assigned_page', template_to_serve,
        #                    max_age=60 * 60 * 24 * 30)  # Set cookie to expire after 30 days
        return response

    # If the user has a cookie, serve the assigned page
    return render_template(assigned_page)