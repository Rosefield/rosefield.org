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
    return name.lower().replace(' ','_').replace(',','')


def template(name, replacements):
    tmpl = load_template(name)

    return tmpl.format(**replacements)

def format_article_link(article):
    return f'<a class="project-link" id="{article.id}Link" href="#{article.id}">{article.name}</a>'

def format_css(hash, file):
    return f'<link rel="stylesheet" integrity="sha256-{hash}" href="{file}" />'

def format_script(hash, file):
    return f'<script async type="text/javascript" integrity="sha256-{hash}" src="{file}"></script>'

def hash_file(name):
    with open(name) as f:
        content = f.read().encode('utf-8')
        sha = sha256()
        sha.update(content)

        hash = sha.digest()
        return b64encode(hash).decode('utf-8')


def gen_script(name):

    formatters = {"css": format_css, "js": format_script}

    files[name] = get_file_time(name)
    hash = hash_file(name)
    type = name.split('.')[-1]
    name = name + "?v=" + urllib.parse.quote_plus(hash)

    return formatters[type](hash, name)

'''
Functions to generate the index page
'''
def index(scripts):

    name = 'Index'
    r = common_replacements(name)
    r['scripts'] = scripts

    articles = [about(), 
                research(),
                work(),
                #interests(), 
                projects(),  
                resume()]

    r['articles'] = '\n'.join([a.content for a in articles])
    
    r['links'] = '\n'.join([format_article_link(a) for a in articles])
    
    id = r['id']
    content = template('index', r)  

    return Article(id, name, content)

def about():
    name = 'About'
    r = common_replacements(name)
    content = template('about', r)

    return Article(r['id'], r['name'], content)

def research():
    name = 'Research'
    r = common_replacements(name)
    content = template('research', r)

    return Article(r['id'], r['name'], content)

def work():
    name = 'Work'
    r = common_replacements(name)
    content = template('work', r)

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

'''
Functions to generate candidacy page
'''
def candidacy(scripts):
    name = 'Candidacy'
    r = common_replacements(name)
    r['scripts'] = scripts
    r['title'] = 'Schuyler Rosefield Candidacy Form'

    articles = [candidacy_link(),
                candidacy_statement()] 
                
    r['articles'] = '\n'.join([a.content for a in articles])
    
    #r['links'] = '\n'.join([format_article_link(a) for a in articles])
    
    id = r['id']
    content = template('candidacy', r)  

    return Article(id, name, content)

def candidacy_statement():
    name = 'Statement by Advisor, abhi shelat'
    r = common_replacements(name)
    r['id'] = 'candidacy_statement'
    content = template('candidacy_statement', r)

    return Article(r['id'], r['name'], content)

def candidacy_link():
    name = 'Paper Link'
    r = common_replacements(name)
    content = template('candidacy_link', r)

    return Article(r['id'], r['name'], content)


'''
Functions to run assemble the files
'''
def pre():

    other_files = ['files/resume.pdf',
                    'files/DRSA.pdf',
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

    
    a = candidacy(scripts)
    candidacy_file = a.id + '.html'
    with open(candidacy_file, 'w') as f:
        f.write(a.content)
        print(f'wrote {candidacy_file}')
    files[candidacy_file] = get_file_time(candidacy_file)

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
