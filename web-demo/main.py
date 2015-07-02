import web
from web import form
import os
import sys
sys.path.append('../amr-el')
import amrel
sys.path.append('../amr-el/src')
import linkipedia

urls = (
    '/', 'index',
    '/linking', 'linking',
    '/graphs/(.*)', 'graphs',
)
app = web.application(urls, globals())
render = web.template.render('templates/')

class index:
    def GET(self):
        form = text()
        return render.template(form)

    def POST(self):
        webinput = web.input()
        output_format = webinput['output']
        coherence_level = webinput['coherence']
        amr_input = str(webinput['input'])
        amrel.main(amr_input, 'output', './')
        return '<html>\n%s\n<html>\n' % open('./output.html').read()

class linking:
    def GET(self):
        webinput = web.input()
        query = webinput['query']
        return linkipedia.find_json(query)

class graphs:
    def GET(self, name):
        ext = name.split(".")[-1]

        cType = {
            "png":"graphs/png",
            "jpg":"graphs/jpeg",
            "gif":"graphs/gif",
            "ico":"graphs/x-icon" }

        if name in os.listdir('graphs'):
            web.header("Content-Type", cType[ext])
            return open('graphs/%s'%name,"rb").read()
        else:
            raise web.notfound()

text = form.Form(
    form.Textarea('input', rows=30, cols=80, value=open('default').read()),
    # form.Dropdown('coherence', [('doc', 'Document-level'),
    #                             ('dis', 'Discourse-level')]),
    # form.Dropdown('output', [('amr', 'AMR'), ('json', 'JSON')]),
    form.Dropdown('coherence', [('doc', 'Document-level')]),
    form.Dropdown('output', [('amr', 'AMR')]),
)

if __name__ == "__main__":
    app.run()
