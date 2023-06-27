# open-ab

### What is open-ab?
open-ab is a server side tool that helps developers randomly split traffic on Flask Routes in support of AB Testing. 

### How does it work?
open-ab was built using GPT-4 via prototypr.ai and is really easy to use. 

On a particular flask route, you simply add the templates you want to randomize with their respective weights of distribution. The randomize weights should add up to 1. 

You pass the templates object or dictionary to the choose_random_template function and return the result.

Here's an example of this code working on a route called /open-ab:

```python

  @app.route('/open-ab')
  def test_ab_view():
  
      # Set the templates you want to render here, with how often you want each to appear using randomize values
      templates = {
          "pages": ["variationA.html", "variationB.html", "variationC.html"],
          "randomize": [0.33, 0.34, 0.33]
      }
      
      # Choose random template based on above config
      template = openab_helper.choose_random_template(templates)
      
      # Render template on route
      return template    

```

The function choose_random_template works as follows:

```python

def choose_random_template(templates):

    """
    Background: 
    This function returns a random template. If the user has already seen a template, they will get the
    same one due to a cookie that is set on the user which assigns the random page to be viewed for
    subsequent visits

    :param 
	templates (obj): Contains a list of pages and a list of respective weights to be randomized
    :return 
	response (str): Template randomly chosen
    """

    # Check if the user has a cookie for the assigned page
    assigned_page = request.cookies.get('assigned_ab_page')

    # If the user is not assigned a page, randomly serve a page and set a cookie for future sessions
    if not assigned_page:

        # Set pages and weights for template to be chosen
        pages = templates["pages"]
        weights = templates["randomize"]

        # Choose a random template based on the list of ab templates and provided weights
        template_to_serve = random.choices(pages, weights, k=1)[0]

        # make_response and return the template
        response = make_response(render_template(template_to_serve))

        # Set a cookie to always show this page - for future sessions
        response.set_cookie('assigned_page', template_to_serve,
                            max_age=60 * 60 * 24 * 30)  # Set cookie to expire after 30 days
        return response

    # If the user has a cookie, serve the assigned page
    return render_template(assigned_page)

```

### How can I test this?

I have supplied 3 landing pages that you can use to test out thie randomization functionality. These pages were geneated generated via prototypr.ai.



# What are the requirements?
In order to run this flask app, you will need to have the following python modules installed:



# Are there any accompanying reports?



