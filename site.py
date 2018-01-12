from collections import namedtuple
import os
import time
import argparse
from datetime import datetime
from base64 import b64encode
from hashlib import sha256
import urllib.parse
import zipfile

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

def index(scripts):

    name = 'Index'
    r = common_replacements(name)
    r['scripts'] = scripts

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

def hash_file(name):
    with open(name) as f:
        content = f.read().encode('utf-8')
        sha = sha256()
        sha.update(content)

        hash = sha.digest()
        return b64encode(hash).decode('utf-8')

def format_css(hash, file):
    return f'<link rel="stylesheet" integrity="sha256-{hash}" href="{file}" />'

def format_script(hash, file):
    return f'<script async type="text/javascript" integrity="sha256-{hash}" src="{file}"></script>'


def gen_script(name):

    formatters = {"css": format_css, "js": format_script}

    files[name] = get_file_time(name)
    hash = hash_file(name)
    type = name.split('.')[-1]
    name = name + "?v=" + urllib.parse.quote_plus(hash)

    return formatters[type](hash, name)

def pre():

    other_files = ['files/resume.pdf',
                    'files/profile_image.jpg']
    
    for f in other_files:
        files[f] = get_file_time(f)

    fs = ['script.js', 'style.css']
    
    scripts = "\n".join([gen_script(f) for f in fs])

    return scripts
    

def post():
    
    with zipfile.ZipFile('site.zip', 'w') as z:
        for name in files.keys():
            z.write(name)


def run():
    scripts = pre()
    a = index(scripts)
    index_file = a.id + '.html'
    with open(index_file, 'w') as f:
        f.write(a.content)
        print(f'wrote {index_file}')
    files[index_file] = get_file_time(index_file)
    post()

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
