
routers = dict(
    # Base router
    BASE = dict(
        default_application = 'SIGPIE',
    ),
    # app specific router
    SIGPIE = dict(
        default_controller = 'home',
        default_function = 'index'
    )
)

routes_onerror = [
    (r'SIGPIE/404', r'/SIGPIE/static/404.html'),
    (r'SIGPIE/*', r'/SIGPIE/static/500.html'),
    (r'*/404', r'/SIGPIE/static/403.html'),
    (r'*/*', r'/SIGPIE/error/index'),
]


error_message = ('<html><body>'
                 '<strong>ERROR DETECTED</strong>'
                 '<h1 style="display:none">%s</h1>'
                 '</body></html>')

error_message_ticket = ('<html><body><h1>Internal error</h1>Ticket issued:'
                        '<a href="/admin/default/ticket/%(ticket)s">'
                        'target = "_blank">%(ticket)s</a>'
                        '<h1>ERROR DETECTED</h1>'
                        '</body></html>')
