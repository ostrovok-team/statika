# Statika

Primitive and fast builder of static blocks (js and css) into the bundles.
Works with Django.

## Basic usage

media/css/project.css:

    @import "reset.css";
    @import "blocks/b-form/b-form.css";

media/js/project.js:

    require('jquery.js');
    require('blocks/b-form/b-form.js');

Usage:

    from statika import build

    build(('media/css/project.css', 'media/css/project.js'))

You can also write includes in included files. E.g., in media/js/blocks/b-form.js:

    require('blocks/i-loader/i-loader.js');

## Advanced usage

TODO

## Using watcher

TODO

## To do:

  * Using watcher in django
