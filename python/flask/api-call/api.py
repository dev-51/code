import flask

from flask import request, jsonify, render_template

app = flask.Flask(__name__)
app.config["DEBUG"] = True

# Create test data 
books = [
    {
		'id': 0,
		'title': 'A Fire Upon the Deep',
		'author': 'Vernor Vinge',
		'first_sentence': 'The coldsleep itself was dreamless.',
		'year_published': '1992'
	},
    {
		'id': 1,
		'title': 'The Ones Who Walk Away From Omelas',
		'author': 'Ursula K. Le Guin',
		'first_sentence': 'With a clamor of bells that set the swallows soaring, the Festival of Summer came to the city Omelas, bright-towered by the sea.',
		'published': '1973'
	},
    {
		'id': 2,
		'title': 'Dhalgren',
		'author': 'Samuel R. Delany',
		'first_sentence': 'to wound the autumnal city.',
		'published': '1975'
	}
]


@app.route('/', methods=['GET'])
#http://127.0.0.1:5000
def home():
    return '''<h1>Distant Reading Archive</h1>
<p>A prototype API for distant reading of science fiction novels.</p>'''


# A route to return all of the available entries in our catalog.
@app.route('/api/v1/resources/books/all', methods=['GET'])
#http://127.0.0.1:5000/api/v1/resources/books/all
def api_all():
    return jsonify(books)

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

@app.route('/api/v1/resources/books', methods=['GET'])
#http://127.0.0.1:5000/api/v1/resources/books?author=Connie+Willis&published=1993&id=3
def api_filter():
    query_parameters = request.args

    id = query_parameters.get('id')
    published = query_parameters.get('published')
    author = query_parameters.get('author')

    results = {
        'id': id
    ,   'published': published
    ,   'author': author
    }
    
    return jsonify(results)

@app.route('/index')
def index():
    user = {'username': 'Miguel'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland.'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool.'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)

@app.route('/api/v1/users/<id>', methods=['GET'])
#http://127.0.0.1:5000/api/v1/users/54
def get_user(id):
    return id

app.run()
