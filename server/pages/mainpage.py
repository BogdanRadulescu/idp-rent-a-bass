from typing import List
from sanic import response, request
from yawrap import Yawrap, LinkCss

def build_page(objects: List):
    jawrap = Yawrap('mainpage.html')
    with jawrap.tag('div', klass='content'):
        with jawrap.tag('span'):
            jawrap.text('CSS in yawrap.')
    jawrap.add(LinkCss.from_file('mainpage.css'))
    return jawrap.render()
    return response.html(jawrap.render())

print(build_page(None))