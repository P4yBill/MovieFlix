from flask_assets import Bundle


def create_assets(assets):
    # js = Bundle(
    #     'vendor/jquery/dist/jquery.min.js',
    #     output='js/libs.js'
    # )
    # assets.register('JS_FRAMEWORS', js)

    css = Bundle(
        'css/app.css',
        output='build/css/app.min.css',
        filters='cssmin'
    )
    assets.register('app-css', css)
