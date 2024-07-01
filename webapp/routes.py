import json

from flask import render_template, redirect, url_for

from webapp import app


@app.route('/')
@app.route('/index')
def index():
    """Main page of the game.
    
    :return: The rendered template.
    :rtype: str
    """
    body = "Which incident would you like to report?"
    links = [{"url": url_for('panel', storyid='lwaxana', panelid=0),
              'text': 'Lwaxana (sexual harassment)'},
             {"url": url_for('panel', storyid='q', panelid=0),
              'text': 'Q (trolling, latently sexual)'},
             {"url": url_for('panel', storyid='riker', panelid=0),
              'text': 'Riker (cheating at poker)'},
             {"url": url_for('panel', storyid='balenciaga', panelid=0),
              'text': 'BONUS EPISODE: The Balenciaga Saga'},
             ]
    return render_template('main.html', body=body, links=links)


@app.route('/<string:storyid>')
def story(storyid):
    """Display the first panel of a story.
    
    :param str storyid: The story ID.
    :return: The rendered template.
    :rtype: str
    """
    return redirect(url_for('panel', storyid=storyid, panelid=0))


@app.route('/<string:storyid>/<string:panelid>')
def panel(storyid, panelid):
    """Display a panel.
    
    :param str storyid: The story ID.
    :param str panelid: The panel ID.
    :return: The rendered template.
    :rtype: str
    """
    with open(f"webapp/static/stories/{storyid}.json") as f:
        data = json.load(f)
    panel_data = data[panelid]
    body = panel_data['paragraph_text']
    choices = panel_data['dialogue_options'].items()
    links = [{"url": url_for('panel', storyid=storyid, panelid=i), 'text': t}
             for i,t in choices]
    return render_template('main.html', body=body, links=links)
