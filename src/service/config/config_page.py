import os
from config.config import get_cfg_details_categories, get_cfg_details_country, get_cfg_details_language, get_cfg_details_sources
from service.news_parameters import categories, countries, languages
from service.news_getinfo import get_sources_all


def build_page():
    #
    html_categories = build_categories()
    html_countries = build_countries()
    html_languages = build_languages()
    html_sources = build_sources()
    #
    with open(os.path.join(os.path.dirname(__file__), 'main_page.html'), 'r') as f:
        return f.read().format(html_categories=html_categories,
                               html_countries=html_countries,
                               html_languages=html_languages,
                               html_sources=html_sources)


def build_categories():
    #
    cfg_categories = get_cfg_details_categories()
    #
    html = '<form>'
    #
    for category in categories:
        #
        if category in cfg_categories:
            checked = 'checked'
        else:
            checked = ''
        #
        html += '<div class="col-xs-6 col-sm-4 col-md-3 col-lg-2 col-xl-1">'
        html += '<input class="form-check-input" type="checkbox" name="category" id="{id}" {checked}>'.format(id=category, checked=checked)
        html += '<label class="form-check-label" style="padding-left: 1em; font-weight: 400;">{label}</label>'.format(id=category, label=category.title())
        html += '</div>'
    #
    html += '</form>'
    #
    return html


def build_countries():
    #
    cfg_country = get_cfg_details_country()
    #
    html = ''
    #
    for id, country in sorted(countries.items()):
        #
        if cfg_country == id:
            checked = 'checked'
        else:
            checked = ''
        #
        html += '<div class="col-xs-6 col-sm-4 col-md-3 col-lg-2 col-xl-1">'
        html += '<input class="form-check-input" type="radio" name="country" value="{id}" id="{id}" {checked}>'.format(id=id, checked=checked)
        html += '<label class="form-check-label" style="padding-left: 1em; font-weight: 400;">{label}</label>'.format(id=id, label=country)
        html += '</div>'
    #
    return html


def build_languages():
    #
    cfg_language = get_cfg_details_language()
    #
    html = ''
    #
    for id, language in sorted(languages.items()):
        #
        if cfg_language == id:
            checked = 'checked'
        else:
            checked = ''
        #
        html += '<div class="col-xs-6 col-sm-4 col-md-3 col-lg-2 col-xl-1">'
        html += '<input class="form-check-input" type="radio" name="language" value="{id}" id="{id}" {checked}>'.format(id=id, checked=checked)
        html += '<label class="form-check-label" style="padding-left: 1em; font-weight: 400;">{label}</label>'.format(id=id, label=language)
        html += '</div>'
    #
    return html


def build_sources():
    #
    cfg_sources = get_cfg_details_sources()
    sources = get_sources_all()
    #
    html = '<div class="container-fluid">'
    #
    for id, source in sorted(sources.items()):
        #
        name = source['name']
        description = source['description']
        url = source['url']
        category = source['category']
        language = source['language']
        country = source['country']
        #
        if id in cfg_sources:
            checked = 'checked'
        else:
            checked = ''
        #
        html += '<div class="row">'
        #
        html += '<div class="col-xs-12 col-sm-12 col-md-3 col-lg-2 col-xl-1">'
        html += '<input class="form-check-input" type="checkbox" name="source" value="{id}" id="{id}" {checked}>'.format(id=id, checked=checked)
        html += '<label class="form-check-label" style="padding-left: 1em; font-weight: 400;">{label}</label>'.format(id=id, label=name)
        html += '</div>'
        #
        html += '<div class="col-xs-11 col-xs-offset-1 col-sm-11 col-sm-offset-1 col-md-8 col-lg-9 col-xl-10" style="margin-bottom: 0.5em;">'
        html += '<p style="margin: 0;">{desc}</p>'.format(desc=description)
        html += '<a href="{url}" >{url}</a>'.format(url=url)
        html += '</div>'
        #
        html += '</div>'
    #
    html += '</div>'
    #
    return html
