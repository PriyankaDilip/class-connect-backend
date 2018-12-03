import json
from db_course import db, Course
from db_hours import db, Hours
from db_votes import db, Cand
from db_security import db, User
from flask import Flask, request
import users_dao

db_filename = "oh_list.db"
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///%s' % db_filename
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

db.init_app(app)
with app.app_context():
    db.create_all()

#get all hours for particular course
@app.route('/course/get_hours/', methods=['GET'])
def get_hours():
    subj = request.args['subj']
    nbr = request.args['nbr']
    course = users_dao.get_course_by_subject_nbr(subj, nbr)
    if course is not None:
        hours = [hour.serialize() for hour in course.hours]
        return json.dumps({'success': True, 'data': hours}), 200
    return json.dumps({'success': False, 'error': 'Hours not found!'}), 404 

@app.route('/courses/get_course/')
def get_course():
    subj = request.args['subj']
    nbr = request.args['nbr']
    course = users_dao.get_course_by_subject_nbr(subj, nbr)
    if course is not None:
        return json.dumps({'success': True, 'data': course.serialize()}), 200
    return json.dumps({'success': False, 'error': 'Course not found!'}), 404

"""
# update course info
@app.route('/courses/foo/', methods=['POST'])
def foo():
    subj = request.args['subj']
    nbr = request.args['nbr']
    course = users_dao.get_course_by_subject_nbr(subj, nbr)
    if course is not None:
        post_body = json.loads(request.data)
        task.description = post_body.get('description', task.description)
        task.done = bool(post_body.get('done', task.done))
        db.session.commit()
        return json.dumps({'success': True, 'data': task.serialize()}), 200
    return json.dumps({'success': False, 'error': 'Task not found!'}), 404
"""

# create new course
@app.route('/courses/', methods=['POST'])
def create_course():
    course_body = json.loads(request.data)

    course = Course(
        subject=course_body.get('subject'),
        catalogNbr=course_body.get('catalogNbr'),
        title=course_body.get('title')
    )
    db.session.add(course)
    db.session.commit()
    return json.dumps({'success': True, 'data': course.serialize()}), 201

# delete course by course info
@app.route('/courses/get_course/delete_course_foo/', methods=['DELETE'])
def delete_course_foo():
    subj = request.args['subj']
    nbr = request.args['nbr']
    course = users_dao.get_course_by_subject_nbr(subj, nbr) 
    if course is not None:
        db.session.delete(course)
        db.session.commit()
        return json.dumps({'success': True, 'data': course.serialize()}), 200
    return json.dumps({'success': False, 'error': 'Course not found!'}), 404 

# create hours for an existing class
@app.route('/courses/hours/create_hour_foo/', methods=['POST'])
def create_hour_foo():
    subj = request.args['subj']
    nbr = request.args['nbr']
    course = users_dao.get_course_by_subject_nbr(subj, nbr)
    if course is not None:
        post_body = json.loads(request.data)
        hour = Hours(
            expert_name=post_body.get('expert_name'),
            expert_type=post_body.get('expert_type'),
            start_time=post_body.get('start_time'),
            end_time=post_body.get('end_time'),
            location=post_body.get('location'),
            course_id=course.course_id
        )
        course.hours.append(hour)
        db.session.add(hour)
        db.session.commit()
        return json.dumps({'success': True, 'data': hour.serialize()})
    return json.dumps({'success': False, 'error': 'Course not found!'}), 404 

def extract_token(request):
    auth_header = request.headers.get('Authorization')
    if auth_header is None:
        return False, json.dumps({'error': 'Missing authorization header.'})

    # Header looks like "Authorization: Bearer <session token>"
    bearer_token = auth_header.replace('Bearer ', '').strip()
    if bearer_token is None or not bearer_token:
        return False, json.dumps({'error': 'Invalid authorization header.'})

    return True, bearer_token
    
@app.route('/')
def hello_world():
    return json.dumps({'message': 'Hello, World!'})

@app.route('/register/', methods=['POST'])
def register_account():
    post_body = json.loads(request.data)
    email = post_body.get('email')
    password = post_body.get('password')

    if email is None or password is None:
        return json.dumps({'error': 'Invalid email or password'})

    created, user = users_dao.create_user(email, password)

    if not created:
        return json.dumps({'error': 'User already exists.'})

    return json.dumps({
        'session_token': user.session_token,
        'session_expiration': str(user.session_expiration),
        'update_token': user.update_token
    })

@app.route('/login/', methods=['POST'])
def login():
    post_body = json.loads(request.data)
    email = post_body.get('email')
    password = post_body.get('password')

    if email is None or password is None:
        return json.dumps({'error': 'Invalid email or password'})

    success, user = users_dao.verify_credentials(email, password)

    if not success:
        return json.dumps({'error': 'Incorrect email or password.'})

    return json.dumps({
        'session_token': user.session_token,
        'session_expiration': str(user.session_expiration),
        'update_token': user.update_token
    })

@app.route('/session/', methods=['POST'])
def update_session():
    success, update_token = extract_token(request)

    if not success:
        return update_token

    try:
        user = users_dao.renew_session(update_token)
    except: 
        return json.dumps({'error': 'Invalid update token.'})

    return json.dumps({
        'session_token': user.session_token,
        'session_expiration': str(user.session_expiration),
        'update_token': user.update_token
    })

@app.route('/secret/', methods=['GET'])
def secret_message():
    success, session_token = extract_token(request)

    if not success:
        return session_token 

    user = users_dao.get_user_by_session_token(session_token)
    if not user or not user.verify_session_token(session_token):
        return json.dumps({'error': 'Invalid session token.'})

    return json.dumps({'message': 'You have successfully implemented sessions.'})
#--------------Edit all references to password above--------------------------
# # ADD MORE ROUTES :)
# """
"""
@app.route('/api/user/', methods=['POST'])
def create_user():
    this_user = json.loads(request.data)
    user = User(
        email = this_user.get('email'),
        family_name = this_user.get('family_name'),
        given_name = this_user.get('given_name')
    )
    db.session.add(user)
    db.session.commit()
    return json.dumps({'success': True, 'data': user.serialize()}), 201
"""

@app.route('/api/votes/', methods=['POST'])
def create_cand():
  """ Create new candidate: 'POST'.
    KW Entry: dict containing
        "cand_id": <USER INPUT>,
        "ta_name": <USER INPUT>,
        "days": <USER INPUT>, 
        "time": <USER INPUT>, 
        "proof": <USER_INPUT>
    Return: JSON with success status and contents of new candidate created
  """
  this_cand = json.loads(request.data)
  cand = Candidates(
      cand_id = this_cand.get('cand_id', ''),
      ta_Name = this_cand.get('ta_name', ''),
      days = this_cand.get('days', ''),
      time = this_cand.get('time', '')
  )
  db.session.add(cand)
  db.session.commit()
  return json.dumps({'success': True, 'data': cand.serialize()}), 201

@app.route('/api/votes/', methods=['GET'])
def get_cands():
  """ Get all candidates: 'GET'.
    KW Entry: dict containing
      "success": True/False,
      "data": <CANDIDATE WITH ID {id}>
    Return: JSON with success status and list of posts. 
  """
  candidates = Candidates.query.all()
  res = {'success': True, 'data': [cand.serialize() for cand in candidates]}
  return json.dumps(res), 200

@app.route('/api/cand/<int:cand_id>/', methods=['GET'])
def get_cand(cand_id):
  """ Get a specific candidate: 'GET'.
      KW Entry: none
      Return: JSON with sucess status and contents of specific post
  """ 
  currPost = Cand.query.filter_by(id=cand_id).first()
  if currPost is not None:
    return json.dumps({'success': True, 'data': currPost.serialize()}), 200
  return json.dumps({'success': False, 'error': 'Cand not found!'}), 404

@app.route('/api/cand/<int:cand_id>/', methods=['POST'])
def edit_cand(cand_id):
  """ Edit a specific candidate: 'POST'
      KW Entry: dict containing "text": <USER INPUT>
      Return: JSON with success status and newly-edited text of specific post
  """
  edited_cand = Cand.query.filter_by(id=cand_id).first()
  if edited_post is not None:
      update = json.loads(request.data)
      edited_post.text = update.get('text', edited_post.text)
      db.session.commit()
      return json.dumps({'success': True, 'data': edited_post.serialize()}), 200
  return json.dumps({'success': False, 'error': 'Post not found!'}), 404

@app.route('/api/cand/<int:cand_id>/', methods=['DELETE'])
def delete_post(cand_id):
  """ Delete specific post: 'DELETE'.
      KW Entry: dict containing
          "success": True,
          "data": <DELETED POST>
      Return: JSON with success status and contents of deleted post
  """
  to_delete = Cand.query.filter_by(id=cand_id).first()
  if to_delete is not None:
    db.session.delete(to_delete)
    db.session.commit()
    # cascade relationship automatically deletes all associated comments
    return json.dumps({'success' : True, 'data': to_delete.serialize()}), 200
  return json.dumps({'success' : False, 'data': "Post not found!"}), 404
  
"""


""" 
@app.route('/api/post/<int:cand_id>/vote/', methods=['POST'])
def vote_post(cand_id):
    """ Upvote/Downvote a specific post: 'POST'
    KW Entry: cand_id
    Return: JSON with success status and newly-edited post
    """
    to_vote_post = Post.query.filter_by(id=cand_id).first()
    if to_vote_post is not None:
        update = json.loads(request.data)
        which_vote = update.get('vote', True)
        if which_vote is True:
            to_vote_post.score = to_vote_post.score+1
        else:
            to_vote_post.score = to_vote_post.score-1
        db.session.commit()
        return json.dumps({'success': True, 'data': to_vote_post.serialize()}), 200
    return json.dumps({'success': False, 'error': 'Post not found!'}), 404


    # @app.route('/api/post/<int:cand_id>/', methods=['POST'])
    # def like_post(cand_id):
    #   """ Like a specific post: 'POST'
    #       Arguments: none
    #       Return: JSON with success status and contents of post with newly-incremented like count.
    #   """
    #   if cand_id in posts:
    #     post_like = posts[cand_id]
    #     post_like["score"] = post_like["score"] + 1
    #     return json.dumps({'success': True, 'data': post_like}), 200
    #   return json.dumps({'success': False, 'error': 'Post not found!'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
