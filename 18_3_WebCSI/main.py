#!/usr/bin/env python
import os
import jinja2
import webapp2


template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if params is None:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        return self.render_template("index.html")

class DNAHandler(BaseHandler):
    def get(self):
        return self.render_template(("dna.html"))

class ResultHandler(BaseHandler):
    def post(self):

        dna = self.request.get("dna")

        analysis = {"Black Hair": 0,
                    "Brown Hair": 0,
                    "Blonde Hair": 0,
                    "Square Face": 0,
                    "Round Face": 0,
                    "Oval Face": 0,
                    "Blue Eyes": 0,
                    "Green Eyes": 0,
                    "Brown Eyes": 0,
                    "Female Gender": 0,
                    "Male Gender": 0,
                    "White Race": 0,
                    "Black Race": 0,
                    "Asian Race": 0}

        analysis["Black Hair"] = dna.count("CCAGCAATCGC")
        analysis["Brown Hair"] = dna.count("GCCAGTGCCG")
        analysis["Blonde Hair"] = dna.count("TTAGCTATCGC")

        analysis["Square Face"] = dna.count("GCCACGG")
        analysis["Round Face"] = dna.count("ACCACAA")
        analysis["Oval Face"] = dna.count("AGGCCTCA")

        analysis["Blue Eyes"] = dna.count("TTGTGGTGGC")
        analysis["Green Eyes"] = dna.count("GGGAGGTGGC")
        analysis["Brown Eyes"] = dna.count("AAGTAGTGAC")

        analysis["Female Gender"] = dna.count("TGAAGGACCTTC")
        analysis["Male Gender"] = dna.count("TGCAGGAACTTC")

        analysis["White Race"] = dna.count("AAAACCTCA")
        analysis["Black Race"] = dna.count("CGACTACAG")
        analysis["Asian Race"] = dna.count("CGCGGGCCG")

        result = []
        for check in analysis:
            if analysis[check] == 1:
                result.append(check)

        return self.render_template("result.html", params={"result": result})

class ContactHandler(BaseHandler):
    def get(self):
        return self.render_template("contact.html")

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/dna', DNAHandler),
    webapp2.Route('/result', ResultHandler),
    webapp2.Route('/contact', ContactHandler),
], debug=True)
