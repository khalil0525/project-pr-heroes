from flask import render_template, url_for
from app import app
from app import TimelinePost
import os
from .models.experience import Experience
from .models.education import Education
from .models.hobbies import Hobbies
from .models.about import About
from .static.sample_data.data import data
from flask import request
from playhouse.shortcuts import model_to_dict
@app.route('/')
def index():
    return render_template('layout.html',
                           title="MLH Fellow",
                           photoUrl=data['John Doe']['photourl'],
                           url=os.getenv("URL")
                           )

@app.route('/about/<name>')
def about(name):
    aboutme = []
    for about in data[name]['about']:
        aboutme.append(About(about['email'],
                                about['twitter'],
                                about['linkedin'],
                                about['description']
                                )
                            )
    return render_template('main.html', 
                           title="MLH Fellow",
                           name=name,
                           photoUrl=data[name]['photourl'],
                           url=os.getenv("URL"),
                           type='About', 
                           elements=aboutme)

@app.route('/experience/<name>')
def experience(name):
    experiences = []
    for experience in data[name]['experience']:
        experiences.append(Experience(experience['company'], 
                                    experience['position'], 
                                    experience['duration'], 
                                    experience['description']
                                    )
                            )
    return render_template('main.html', 
                           title="MLH Fellow",
                           name=name,
                           photoUrl=data[name]['photourl'],
                           url=os.getenv("URL"),
                           type='Experience', 
                           elements=experiences)

@app.route('/education/<name>')
def education(name):
    educations = []
    for education in data[name]['education']:
        educations.append(Education(education['institution'], 
                                    education['degree'], 
                                    education['tenure'], 
                                    education['description']
                                    )
                            )
    return render_template('main.html', 
                           title="MLH Fellow",
                           name=name,
                           photoUrl=data[name]['photourl'],
                           url=os.getenv("URL"),
                           type='Education', 
                           elements=educations)

@app.route('/hobbies/<name>')
def hobbie(name):
    hobbies = []
    for hobbie in data[name]['hobbies']:
        hobbies.append(Hobbies(hobbie['name'],
                            hobbie['description'],
                            hobbie['url'],
                            hobbie['alt'],
                            hobbie['textcolor']
                                )
                    )
    return render_template('main.html', 
                           title="MLH Fellow",
                           name=name,
                           photoUrl=data[name]['photourl'],
                           url=os.getenv("URL"),
                           type='Hobbies', 
                           elements=hobbies)
@app.route('/timeline/')
def timeline():
    return render_template('timeline.html', title="Timeline")

@app.route('/api/timeline_post', methods=['POST'])
def post_time_line_post():
    name = request.form['name']
    email = request.form['email']
    content = request.form['content']
    timeline_post = TimelinePost.create(name=name, email=email, content=content)
    
    return model_to_dict(timeline_post)

@app.route('/api/timeline_post', methods=['GET'])
def get_time_line_post():
    return {
        'timeline_posts':[
        model_to_dict(p)
        for p in
        TimelinePost.select().order_by(TimelinePost.created_at.desc())
        ]
    }
@app.route('/api/timeline_post', methods=['DELETE'])
def delete_time_line_posts():
    delete_posts = TimelinePost.delete()
    delete_posts.execute()
    return {        'timeline_posts':[
        model_to_dict(p)
        for p in
        TimelinePost.select().order_by(TimelinePost.created_at.desc())
        ]

    }


