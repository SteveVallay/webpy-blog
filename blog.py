import web
import model 
import log
urls = (
        '/','Index',
        '/view/(/d+)','View',
        '/new','New',
        '/delete/(/d+)','Delete',
        '/edit/(/d+)','Edit',
        '/login','Login',
        '/logout','Logout',
        )

app  = web.application(urls,globals())
log =log.Log()
t_globals = { 
        'datestr': web.datestr,
        'cookie' :web.cookies,
        }

render = web.template.render('templates',base='base',globals=t_globals)

login = web.form.Form(
        web.form.Textbox('username'),
        web.form.Password('password'),
        web.form.Button('login')
        )

class Index:
    def GET(self):
        login_form=login()
        posts = model.get_posts()
        return render.index(posts,login_form)
    def POST(self):
        login_form = login()
        if login_form.validates():
            if login_form.d.username == 'admin' and login_form.d.password == 'admin':
                web.setcookie('username',login_form.d.username)
        raise web.seeother('/')
class View:
    def GET(self,id):
        print 'view...get'
        post = model.get_post(int(id))
        print 'post is', post
        return render.view(post)
class New:
    form = web.form.Form(
            web.form.Textbox('title',
            web.form.notnull,
            size=30,
            description='Post title:'),
            web.form.Textarea('content',
            web.form.notnull,
            row = 30,
            cols=80,
            description = 'Post content:'),
            web.form.Button('Post entry'),
            )
    def GET(self):
        form = self.form()
        log.logd('New','get...')
        print 'New--get'
        return render.new(form)
    def POST(self):
        form = self.form()
        log.logd('New','post...')
        if not form.validates():
            log.logd('New','not validates()...')
            return render.new(form)
        model.new_post(form.d.title,form.d.content)
        raise web.seeother('/')
class Delete:
    def POST(self,id):
        model.delete_post(int(id))
        raise web.seeother('/')
class Edit:
    def GET(self,id):
        post = model.get_post(int(id))
        form = New.form()
        form.fill(post)
        return render.edit(post,form)
    def POST(self,id):
        form = New.form()
        post = model.get_post(int(id))
        if not form.validates():
            return render.edit(post,form)
        model.update_post(int(id),form.d.title,form.d.content)
        raise web.seeother('/')
class Logout:
    def GET(self):
        web.setcookie('username','',expires=-1)
        raise web.seeother('/')

def notfound():
    return web.notfound('Sorry, the page you are looking for   was not found')
app.notfound = notfound

if __name__ == '__main__':
    app.run()
