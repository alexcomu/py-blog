from wsgiref.simple_server import make_server
import urlparse

POSTS = [dict(title='Article-1',
              content='Hello world!'),dict(title='Article-2',
              content='Hello Again!')]

def blog(environ, start_response):
    path = environ['PATH_INFO'][1:]
    print path
    create_message = ""
    if path == "create":
        query_string = environ['QUERY_STRING']
        params = urlparse.parse_qs(query_string)
        if not ('title' in params and 'content' in params):
            create_message = '''
                    <p style="color:red;">Title or content not provided!</p>
                '''
        else:
            POSTS.append(dict(title=params['title'][0],
                            content=params['content'][0]))
            create_message = '''
                    <p style="color:green;">Post Created!!</p>
                '''
    articles = ['''
        <h2>
            <a href="/%(title)s">%(title)s</a>
        </h2>
        <p>%(content)s</p>
        ''' % d for d in filter(lambda p: p['title'] == path, POSTS) or POSTS]

    # set container
    html_articles = ''.join(articles)
    # response header
    start_response('200 OK', [('Content-Type', 'text/html')])
    # response
    return '''
        <html>
            <head>
                <title>Welcome to Py-Blog!</title>
            </head>
            <body>
                <h1>This is my Blog!</h1>
                %(create_message)s
                <hr/>
                %(content)s
                <hr/>
                <h3>Create new Article!</h3>
                <form method="GET" action="/create">
                    <input type="text" name="title" placeholder="Title..">
                    <input type="text" name="content" placeholder="Content..">
                    <input type="submit" value="Create!">
                </form>
            </body>
        </html>
        ''' % dict(content=html_articles, create_message=create_message)

server = make_server('', 8080, blog)
print 'Serving on 8080'
server.serve_forever()
