import os
import logging

from google.appengine.ext import webapp 
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import users
from google.appengine.ext import db

from models import Link


class BasePage(webapp.RequestHandler):

    def __init__(self):
        (self.user, self.login_url, self.logout_url) = self.auth_data()
        self.user_is_admin = users.is_current_user_admin()
        self.template_values = {
            "user":self.user, 
            "user_is_admin":self.user_is_admin,
            "login_url":self.login_url, 
            "logout_url":self.logout_url,
            "debug":config.SITE["debug"],
        } 

    def auth_data(self):
        """Returns: (user, login_url, logout_url)"""
        user = users.get_current_user()
        login_url = users.create_login_url("/auth")
        logout_url = users.create_logout_url("/")
        return (user, login_url, logout_url)

    def template_path(self, tmpl):
        return os.path.join(os.path.dirname(__file__), "templates/%s" % tmpl)

    def render(self, tmpl, tmpl_vals):
        template_path = self.template_path(tmpl) 
        self.response.out.write(template.render(template_path, tmpl_vals))


class Index(BasePage):
    """
    Homepage where User submits URL to be shortened.
    """

    def get(self):
        self.template_values.update({})
        self.render("index.html", self.template_values) 

    def post(self):
        url = self.request.get("url")
        custom_path = self.request.get("custom_path")
        if custom_path:
            exists = Link.filter("path =", custom_path).get()
            if exists:
                return "path already exists, choose another"
        
class Stats(BasePage):
    """
    Show stats for most recent and most followed links.
    """

    def get(self):
        links = Link.filter("user =", self.user).order_by_count_desc().fetch(config.SITE["max_stats"])
        self.template_values.update({"links":links})
        self.render("stats.html", self.template_values) 

class Expand(BasePage):
    """
    Get the target URL given the shortened path.
    """

    def get(self, path):
        linkobj = Link.get_link_by_path(path)
        #account for 404, log it.
        linkobj.count += 1
        linkobj.put()
        self.redirect(linkobj.url)


application = webapp.WSGIApplication([
    ("/", Index),
    ("/stats", Stats),
    ("/(.+)", Expand),
    ], debug=True)

if __name__ == "__main__":
    run_wsgi_app(application)
