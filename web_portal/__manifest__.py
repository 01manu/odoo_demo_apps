{
    'name': 'website portal',
    'summary': """This module allows to create a web portal """,
    'version': '1.3',
    'author': 'Manoj',
    'company': 'prime minds consulting pvt ltd',
    'website': 'http://www.primeminds.com',
    'category': 'website',
    'depends': ['base', 'website', 'web', 'hr','mail', ],
    'data': [

        'views/portal.xml',
        # 'views/web_portal.xml',
        'views/exam_portal.xml',
        # 'security/ir.model.access.csv',
        # 'security/ir.model.access.csv',

    ],
    'images':['static/src/Description/img/bg.jpeg'],
    'installable': True,
    'application': True,

}
