 
def load_template(name):
    with open(name + '.tmpl') as f:
        return f.read()

def common_replacements():
    r = {'site_title': 'Schuyler Rosefield'}
    return r 

def template(name, replacements):

    tmpl = load_template(name)

    return tmpl.format(**replacements)

def create_link(id, name):

    return f'<a class="project-link" id="{id}Link" href="#{id}">{name}</a>'

def index():

    r = common_replacements()

    sections = [about(), projects(), interests()]

    r['articles'] = '\n'.join([section[2] for section in sections])
    
    r['links'] = '\n'.join([create_link(section[0], section[1]) for section in sections])
    
    content = template('index', r)  

    return ('index', 'Index', content)

def about():

    return ('about', 'About', 'Hi I am Schuyler')

def projects():

    return ('projects', 'Selected Projects', 'There will be projects here')

def interests():

    return ('interests', 'Interests', 'All crypto all day every day')

def main():
    s = index()
    with open(s[0] + '.html', 'w') as f:
        f.write(s[2])
    
    return

if __name__ == "__main__":
    main()
