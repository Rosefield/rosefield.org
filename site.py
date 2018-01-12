from collections import namedtuple
import os
import time
import argparse
from datetime import datetime

Article = namedtuple('Article', ['id', 'name', 'content'])

files = {}

def watch_files():
    
    if(len(files) == 0):
        return True

    while True:
        for name, ftime in files.items():
            if ftime < get_file_time(name):
                return True

        time.sleep(1)

def get_file_time(name):
    return os.stat(name).st_mtime

def load_template(name):
    name = name + '.tmpl'

    files[name] = get_file_time(name)

    with open(name) as f:
        return f.read()

def common_replacements(name):
    r = {'site_title': 'Schuyler Rosefield'}

    r['date_created'] = datetime.now().strftime('%Y-%m-%d')

    if name:
        r['name'] = name
        r['id'] = name_to_id(name)
    return r 

def name_to_id(name):
    return name.lower().replace(' ','_')


def template(name, replacements):

    tmpl = load_template(name)

    return tmpl.format(**replacements)

def create_link(article):

    return f'<a class="project-link" id="{article.id}Link" href="#{article.id}">{article.name}</a>'

def index():

    name = 'Index'
    r = common_replacements(name)

    articles = [about(), 
                #interests(), 
                projects(),  
                resume()]

    r['articles'] = '\n'.join([a.content for a in articles])
    
    r['links'] = '\n'.join([create_link(a) for a in articles])
    
    id = r['id']
    content = template('index', r)  

    return Article(id, name, content)

def about():
    name = 'About'
    r = common_replacements(name)
    content = template('about', r)

    return Article(r['id'], r['name'], content)

def projects():
    name = 'Projects'
    r = common_replacements(name)
    content = template('projects', r)

    return Article(r['id'], r['name'], content)

def interests():
    name = 'Interests'
    r = common_replacements(name)
    content = template('interests', r)

    return Article(r['id'], r['name'], content)

def resume():
    name = 'Resume'
    r = common_replacements(name)
    content = template('resume', r)

    return Article(r['id'], r['name'], content)

def run():
    a = index()
    with open(a.id + '.html', 'w') as f:
        f.write(a.content)
        print(f'wrote {a.id}.html')

def main():
    arg = argparse.ArgumentParser()
    arg.add_argument('--watch-files', dest='watch_files', action='store_const', 
                        const=True, default=False)

    args = arg.parse_args()

    if(args.watch_files):
        while True:
            watch_files()
            run()
    else:
        run() 

    
    return

if __name__ == "__main__":
    main()
