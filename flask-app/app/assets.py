from flask_assets import Bundle

movies_assets = [
    'movies_views/js/movies_table.js',
    'movies_views/js/delete_movie_handler.js',
    'movies_views/js/delete_comment_handler.js',
    'movies_views/js/edit_movie_handler.js'
]

admin_panel_assets = [
    'admin_panel/js/users-table.js',
    'admin_panel/js/button-handlers.js'
]

user_profile_js_assets = [
    'user_profile/js/button-handlers.js'
]

def create_assets(assets):
    js = Bundle(
        *user_profile_js_assets,
        output='build/js/movies.js',
        filters='jsmin'
    )
    assets.register('user_profile_js', js)

    js = Bundle(
        *admin_panel_assets,
        output='build/js/movies.js',
        filters='jsmin'
    )
    assets.register('admin_js', js)

    js = Bundle(
        *movies_assets,
        output='build/js/movies.js',
        filters='jsmin'
    )
    assets.register('movies_js', js)

    css = Bundle(
        'css/app.scss',
        output='build/css/app.min.css',
        filters='pyscss,cssmin'
    )

    movies_css = Bundle(
        'movies_views/css/movies.scss',
        output='build/css/movies.min.css',
        filters='pyscss,cssmin'
    )

    js_common = Bundle(
        'js/common.js',
        output='build/js/common.js',
        filters='jsmin'
    )

    jquery = Bundle(
        'js/jquery.js',
        output='build/js/jquery.js',
        filters='jsmin'
    )

    assets.register('common_js', js_common)
    assets.register('jquery', jquery)
    assets.register('app-css', css)
    assets.register('movies-css', movies_css)
