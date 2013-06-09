# Statika

Primitive and fast builder of static blocks (js and css) into the bundles for projects written in Python.
Tested with Django and Werkzeug.

## Basic usage

media/css/project.css:

    @import "reset.css";
    @import "blocks/b-form/b-form.css";

media/js/project.js:

    require('jquery.js');
    require('blocks/b-form/b-form.js');

And following code creates media/css/_project.css and media/css/_project.js bundles:

    from statika import build

    build(('media/css/project.css', 'media/css/project.js'))

You can also use includes in included files. E.g., in media/js/blocks/b-form.js:

    require('blocks/i-loader/i-loader.js');

## Writing custom handlers

TODO:

## Using watcher

TODO:

## Django command "build_static"

TODO:
