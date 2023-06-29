# open-ab

### Contents

1. What is open_ab?
2. How does open_ab work?
3. Measuring AB Traffic Variations
4. Implementing Data Collection for AB Tests
5. Reporting on AB Test Results
6. Requirements & How to Run this App
7. References


### What is open-ab?
open_ab is server side software that helps developers randomly split traffic on Flask Routes in support of AB Testing. 

### How does open_ab work?

The purpose of open_ab is to make it easy to distribute random page templates on flask routes in support of AB Testing. For any particular flask route, you simply create a list of html page templates that you want to randomize and set their respective weights of distribution. The list of randomize weights should sum up to 1, which represents 100% of traffic across all variations.

Here's an example of the open_ab code working on a route called /open-ab:

```python

  @app.route('/open-ab')
  def test_ab_view():
  
      # Set the templates you want to randomize with how often you want each to appear
      templates = {
          "pages": ["variationA.html", "variationB.html", "variationC.html"],
          "randomize": [0.34, 0.33, 0.33]
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
    same one due to a cookie that is set on the user which assigns that page to be viewed for
    subsequent visits

    :param 
	templates (obj): Contains a list of pages and a list of respective weights to be randomized
    :return 
	response: Render the random template that was chosen or already assigned.

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

### Measuring AB Traffic Variations

In order to measure what pages are being rendered on a route, we’ll need to use a dataLayer as part of a Google Analytics 4 (GA4) and Google Tag Manager (GTM) implementation. 

A dataLayer helps store meta data about pages or events you want to measure. In this case, let’s use the dataLayer to store information about our experiments using standardized experiment event parameters:

1. experiment_name
2. experiment_variation

The Control page template (variationA.html) has a dataLayer in the head of its page and contains the following information about an experiment.

```javascript
<!-- Google Tag Manager Data Layer -->
<script>
  dataLayer = [{
    "experiment_name": "Server Side Test 01",
    "experiment_variation": "Control"
  }];
</script>
<!-- End Google Tag Manager Data Layer -->
```

When the page loads, we’ll trigger a GA4 page_view event in Google Tag Manager and pass this data along with that event. When a user interacts with an element on this page, we can also pass this data from the dataLayer along with the event (eg. button_click).

Below are some instructions for how to implement data collection in support of AB tests.

# Implementing Data Collection for AB Tests

### Setting up event parameters in Google Analytics 4

In order to measure the variations being viewed and interacted with, we will need to set up some event parameters in GA4. 

Event parameters allow us to attach meta data to various events in GA4, such as page_views and button clicks. 

So, when the page_view event is triggered, we can pass these parameters from the dataLayer along with it and denote what experiment_name and experiment_variation is being viewed.

In Google Analytics 4, open Admin > Custom dimensions

Then click create a new Custom dimension for both experiment_name and experiment_variation like this:
<img width="561" alt="Adding a custom dimension in GA4" src="https://github.com/garethcull/open-ab/assets/3453253/beccc166-e94d-495c-94ff-cf8c84b5da4d">


That’s it! Now let’s add an event_parameter to the pageview event in GTM.

### Passing an event_parameter along with GA4 event in Google Tag Manager

The first thing we need to do in GTM, is to register experiment_name and experiment_variations as dataLayer Variables. We’ll then attach these variables to a page_view event. 

### Creating a DataLayer Variable in GTM

In Google Tag Manager, go to your workspace > Variables > New User-Defined Variable.

Under Variable Configuration, choose ‘Data Layer Variable’, then enter the event parameter name you want to create. 

Here’s what that should look like for experiment_name. 

<img width="1146" alt="Setting up a DataLayer Variable in GTM" src="https://github.com/garethcull/open-ab/assets/3453253/84952e30-4228-4539-9bd8-fa30d2f31c33">

Then repeat the same process for experiment_variable.

### Create a GA4 page_view Event in GTM and Pass Experiment Parameters

Now that we have created the event parameters, let’s quickly create a GA4 page_view event.

Click New Tag > Tag Configuration > Google Analytics 4: Event

Then configure the event like this:
<img width="1144" alt="GA4 Page View event tag in GA4" src="https://github.com/garethcull/open-ab/assets/3453253/5f871fe2-e531-4e49-a23f-f52f8d798ee8">

Notice that in the Event Parameters section, I added in our two experiment parameters with values (which is the name of the dataLayer variable in curly brackets).

Next, you’ll need to create an event for any conversions you want to measure as part of your test and pass these same experiment parameters along with that event. 

Keep repeating this process for any other events you want to measure as part of the experiment.

Then publish the GTM container and sing like no one is listening!

<img width="952" alt="Publishing a container in GTM" src="https://github.com/garethcull/open-ab/assets/3453253/ce731f11-514c-4808-9c18-84da8c4b56e7">


If you need any help implementing Google Analytics 4, I do provide consulting in this area and would be happy to collaborate with you and get your testing program set up! So, please reach out to me on LinkedIn you need any assistance.


# Reporting on AB Test Results

Now that everything is set up, let's talk about our reporting options. 

I created an AB Testing report on <a href="https://www.prototypr.ai" rel="dofollow">prorotypr.ai</a> that automatically pulls this data and creates a report for you using the GA4 API. (Disclosure: I am the creator of <a href="https://www.prototypr.ai" rel="dofollow">prorotypr.ai</a>). 

This report does all of the heavy lifting for you and even calculates experiment statistics using SciPy and has GPT-3.5 do some light analysis on the results! It's an experimental report, but it works really well.

Here’s a screenshot of a report I created and am currently using to measure AB Tests on prototypr.ai:
![ab_test_results_open_ab](https://github.com/garethcull/open-ab/assets/3453253/66666148-1068-4783-aff1-5d4a74a1c0f1)




If you want to sign-up for access, please visit <a href="https://www.prototypr.ai" rel="dofollow">prorotypr.ai</a> or message me for a demo about how it works.

If you want to use other reporting options, I’d recommend:

1. Looker Studio
2. GA4 API
3. SciPy for experiment stats

# Requirements & How to Run this App

This app requires the following python modules, which you will need to install in your developer environment
* Flask
* Random
* eventlet (used when deploying to Heroku)
* gunicorn (used when deploying to Heroku)
  
### How to run this locally.

1. Clone this repo and make sure you install all of the above dependencies using requirements.txt
2. Open Repo folder in dev environment in terminal
3. In terminal ($): flask run --debugger --reload
4. Open http://localhost:5000/open-ab
5. Refresh Page to see the different variations!

### Page Templates Included in this App

I have supplied 3 landing pages in the /templates folder that you can use to test out the randomization functionality. These pages were generated via <a href="https://www.prototypr.ai" rel="dofollow">prototypr.ai</a>.

Here's what the variations look like:
<br>
<img width="100%" alt="Landing page generated with prototypr.ai" src="https://github.com/garethcull/open-ab/assets/3453253/f6abdecc-ad96-4af3-a9d5-4eeeeaf1af0c">

### Setting Cookies on Page Experiences

In order to enable the user to see the same experience, you'll need to set a cookie. This has been commented out inititally so you can see the randomization at work.

```python
# Set a cookie to always show this page - for future sessions
response.set_cookie('assigned_page', template_to_serve,max_age=60 * 60 * 24 * 30)  
```

### Hosting on Heroku?
I’ve included a Procfile and some eventlet dependencies outlined in requirements.txt if you want to test it out on Heroku.

# References

1. <a href="https://www.prototypr.ai" rel="dofollow">prorotypr.ai</a> - Used GPT-4 chat in prototypr.ai to generate first draft of this code, which was later edited. I also generated and edited landing page template from prototypr.ai's landing page generator tool. 

2. <a href="https://support.google.com/analytics/">Google Analytics 4 Support Page</a>

3. <a href="https://support.google.com/tagmanager/">Google Tag Manager Support Page</a>
