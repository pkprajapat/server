# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################
def test():
    noti = db(db.users.hostel==db.hostel_names.id).select(orderby=~db.hostel_names.id)
    return dict(show=noti)

""" userid = request.vars.userid
    password = request.vars.password
    user = auth.login_bare(userid,password)
    return dict(success=False if not user else True, user=user)
"""
def comment_new():
    if auth.is_logged_in() and ("description" in request.vars) and ("id_comp" in request.vars):
        description = str(request.vars["description"]).strip()
        id_comp = str(request.vars["id_comp"])
        if description!='':
            cid = db.comments_.insert(created_by=auth.user.id, id_complaint=id_comp, description=description)
        notii = db(db.notification.id_complaint == id_comp).select()
        for noti in notii:
            row = db(db.notifications.id==noti.id).select().first()
            row.update_record(is_seen_new = "False")
        return dict(success="True")
    return dict(success="False")

def new_complaint():
    if auth.is_logged_in() and ("title" in request.vars) and ("description" in request.vars) and ("id_type" in request.vars):
        description = str(request.vars["description"]).strip()
        title = str(request.vars["title"])
        id_user = auth.user.id
        id_type = str(request.vars["id_type"])
        addressed_to = str(request.vars["addressed_to"])
        if description!='' and title!='' and id_type!='' and addressed_to!='':
            cid = db.complaints.insert(user_=auth.user.id, id_type=id_type,title=title, description=description,addressed_to=addressed_to,resolving_person="me")
        if id_type ==2:
            users = db(db.users.id >0).select().first()
            for us in users:
                nid = db.notification.insert(id_user=us.id,id_complaint=cid,id_type=id_type)
        if id_type == 1:
            cur = db(db.users.id == auth.user.id).select().first()
            users = db(db.user.hostel == cur.hostel).select()
            for us in users:
                nid = db.notification.insert(id_user=us.id,id_complaint=cid,id_type=id_type)
        return dict(success="True",complaint=cid)
    return dict(success="False")


def complaint_new():
    def POST(title,description,id_type,addressed_to):
        user_ = auth.user.id
        return  db.complaints.validate_and_insert(title=title,description=description,user_=user_,id_type=id_type,addressed_to=addressed_to,resolving_person ="me")

@auth.requires_login()
def notification():
    notii = db(db.notification.id_user == auth.user.id ).select(orderby=~db.notification.id)
    users = []
    complaints = []
    comp_type = []
    users.append(db(db.users.id == auth.user.id).select().first())
    for noti in notii:
        complaints.append(db(db.complaints.id == noti.id_complaint).select().first())
        comp_type.append(db(db.complaint_type.id == noti.id_type).select().first())
    for comp in complaints:
        users.append(db(db.users.id == comp.user_).select().first())
    return dict(notifi=notii,users=users,complaints=complaints,comp_type=comp_type)

@auth.requires_login()
def complaint():
	try:
		cid = int(request.args[0])
	except Exception, e:
		raise e
	try:
		tab = str(request.args[1])
	except Exception, e:
		tab = "problem"
	try:
		vote = int(request.args[2])
	except Exception, e:
		vote = 0
	success = "False"
	row = db(db.complaints.id==cid).select().first()
	if 1==1:
		complaint = db(db.complaints.id==cid).select().first()
        comments = get_comments(cid)
        if(len(request.args)==1):success = "True" 
        users = []
        users.append(db(db.users.id == complaint.user_).select().first())
        for comm in comments:
			users.append(db(db.users.id == comm.created_by).select().first())
	if (len(request.args)==2) & (tab == "resolve") :
		row.update_record(is_resolved = 1) if row.is_resolved==0 else row.update_record(is_resolved = 0)
		success = "True"
	if (len(request.args)==3) & (tab == "vote"):     ##check if already upvoted
		row.update_record(upvotes = vote+row.upvotes)
		success = "True"
	db(db.notification.id_user==auth.user.id)(db.notification.id_complaint == cid).update(is_seen=1)
	db(db.notification.id_user==auth.user.id)(db.notification.id_complaint == cid).update(is_seen_new=1)
	if success == "True":
		return dict(success = success, complaint=complaint,comments=comments,users=users)
	else :
		raise HTTP(404)



def get_comments(cid):
    comments =  db(db.comments_.id_complaint == cid).select()
    return comments



def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    response.flash = T("Welcome on Moodle+")
    return dict(noti_count=4)

def grades():
    grades = db(db.grades.user_id==auth.user.id).select()
    courses = []
    for grade in grades:
        courses.append(db(db.courses.id==grade.registered_course_id.course_id).select().first())
    return dict(grades=grades, courses=courses)

def notifications():
    noti = db(db.notifications.user_id==auth.user.id).select(orderby=~db.notifications.created_at)
    db(db.notifications.user_id==auth.user.id).update(is_seen=1)
    return dict(notifications=noti)


def logged_in():
    return dict(success=auth.is_logged_in(), user=auth.user)

def logout():
    return dict(success=True, loggedout=auth.logout())

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@request.restful()
def api():
    response.view = 'generic.'+request.extension
    def GET(*args,**vars):
        patterns = 'auto'
        parser = db.parse_as_rest(patterns,args,vars)
        if parser.status == 200:
            return dict(content=parser.response)
        else:
            raise HTTP(parser.status,parser.error)
    def POST(table_name,**vars):
        return db[table_name].validate_and_insert(**vars)
    def PUT(table_name,record_id,**vars):
        return db(db[table_name]._id==record_id).update(**vars)
    def DELETE(table_name,record_id):
        return db(db[table_name]._id==record_id).delete()
    return dict(GET=GET, POST=POST, PUT=PUT, DELETE=DELETE)

def login():
    userid = request.vars.userid
    password = request.vars.password
    user = auth.login_bare(userid,password)
    return dict(success=False if not user else True, user=user)

def populate_db():
	## Populate DB Script

	## clear database
	for table in db.tables():
		try:
			db(db[table].id>0).delete()
			print "Cleared",table
		except Exception, e:
			print "Couldn't clear",table

    ##create hostel names
	db.hostel_names.insert(
		hostel_name = "Nilgiri"
	)
	db.hostel_names.insert(
		hostel_name = "Kara"
	)
	db.hostel_names.insert(
		hostel_name = "Kailash"
	)

    ##create complaint types
	db.complaint_type.insert(
		type_name = "Individual"
	)
	db.complaint_type.insert(
		type_name = "Hostel Level"
	)
	db.complaint_type.insert(
		type_name = "Institute Level"
	)

    ##create professions
	db.profession.insert(
		profession = "Student"
	)
	db.profession.insert(
		profession = "Professor"
	)
	db.profession.insert(
		profession = "Warden"
	)

	## create 4 students
	db.users.insert(
		first_name="John",
		last_name="Doe",
        hostel = 1,
		email="cs1110200@cse.iitd.ac.in",
		username="cs1110200",
		entry_no="2011CS10200",
		type_=0,
		password="john",
	)

	db.users.insert(
		first_name="Jasmeet",
		last_name="Singh",
        hostel = 2,
		email="cs5110281@cse.iitd.ac.in",
		username="cs5110281",
		entry_no="2011CS50281",
		type_=0,
		password="jasmeet",
	)

	db.users.insert(
		first_name="Abhishek",
		last_name="Bansal",
        hostel = 2,
		email="cs5110271@cse.iitd.ac.in",
		username="cs5110271",
		entry_no="2011CS50271",
		type_=0,
		password="abhishek",
	)


	db.users.insert(
		first_name="Shubham",
		last_name="Jindal",
        hostel = 1,
		email="cs5110300@cse.iitd.ac.in",
		username="cs5110300",
		entry_no="2011CS50300",
		type_=0,
		password="shubham",
	)


	## create 3 professors
	db.users.insert(
		first_name="Vinay",
		last_name="Ribeiro",
        hostel = 3,
		email="vinay@cse.iitd.ac.in",
		username="vinay",
		entry_no="vinay",
		type_=1,
		password="vinay",
	)

	db.users.insert(
		first_name="Suresh",
		last_name="Gupta",
        hostel = 2,
		email="scgupta@cse.moodle.in",
		username="scgupta",
		entry_no="scgupta",
		type_=1,
		password="scgupta",
	)

	db.users.insert(
		first_name="Subodh",
		last_name="Kumar",
        hostel = 1,
		email="subodh@cse.iitd.ac.in",
		username="subodh",
		entry_no="subodh",
		type_=1,
		password="subodh",
	)
    ##linking hostels and users
	db.hostels.insert(
		hostel_name = 1,
        user_ = 1
	)
	db.hostels.insert(
		hostel_name = 2,
        user_ = 2
	)
	db.hostels.insert(
		hostel_name = 2,
        user_ = 3
	)
	db.hostels.insert(
		hostel_name = 1,
        user_ = 4
	)
	db.hostels.insert(
		hostel_name = 3,
        user_ = 5
	)
	db.hostels.insert(
		hostel_name = 2,
        user_ = 6
	)
	db.hostels.insert(
		hostel_name = 1,
        user_ = 7
	)

    ##create a sample complaint
	db.complaints.insert(
		title = "too much work in cop290",
        description ="At any time, there is a cop290 assignment to submit.Either make the work load less or conduct actual help sessions",
        user_ = 1,
        id_type = 2,
        addressed_to = 2,
        resolving_person = "I"
	)

	db.comments_.insert(
        description ="sounds right",
        created_by = 4,
        id_complaint = 1
	)
	db.comments_.insert(
        description ="please, consider it at the time of grading",
        created_by = 7,
        id_complaint = 1
	)

	db.notification.insert(
		id_user = 1,
        id_complaint = 1,
        id_type = 2,
        is_seen = 1
	)
	db.notification.insert(
		id_user = 4,
        id_complaint = 1,
        id_type = 2
	)
	db.notification.insert(
		id_user = 7,
        id_complaint = 1,
        id_type = 2
	)



	## create 7 courses
	db.courses.insert(
		name="Design Practices in Computer Science",
		code="cop290",
		description="Design Practices in Computer Science.",
		credits=3,
		l_t_p="0-0-6"
	)

	db.courses.insert(
		name="Wireless Networks",
		code="csl838",
		description="PHY and MAC layer concepts in wireless networking",
		credits=3,
		l_t_p="2-0-2"
	)

	db.courses.insert(
		name="Software Engineering",
		code="col740",
		description="Introduction to the concepts of Software Design and Engineering.",
		credits=4,
		l_t_p="3-0-2"
	)

	db.courses.insert(
		name="Cloud Computing and Virtualisation",
		code="csl732",
		description="Introduction to Cloud Computing and Virtualisation.",
		credits=4,
		l_t_p="3-0-2"
	)

	db.courses.insert(
		name="Parallel Programming",
		code="col380",
		description="Introduction to concurrent systems and programming style.",
		credits=4,
		l_t_p="3-0-2"
	)

	db.courses.insert(
		name="Computer Graphics",
		code="csl781",
		description="Computer Graphics.",
		credits=4,
		l_t_p="3-0-2"
	)

	db.courses.insert(
		name="Advanced Computer Graphics",
		code="csl859",
		description="Graduate course on Advanced Computer Graphics",
		credits=4,
		l_t_p="3-0-2"
	)




	## create 7 registered courses
	db.registered_courses.insert(	
		course_id=1,
		professor=5,
		year_=2016,
		semester=2,
		starting_date=datetime(2016,1,1),
		ending_date=datetime(2016,5,10),
	)

	db.registered_courses.insert(
		course_id=2,
		professor=5,
		year_=2016,
		semester=2,
		starting_date=datetime(2016,1,1),
		ending_date=datetime(2016,5,10),
	)

	db.registered_courses.insert(
		course_id=3,
		professor=6,
		year_=2016,
		semester=2,
		starting_date=datetime(2016,1,1),
		ending_date=datetime(2016,5,10),
	)

	db.registered_courses.insert(
		course_id=4,
		professor=6,
		year_=2016,
		semester=2,
		starting_date=datetime(2016,1,1),
		ending_date=datetime(2016,5,10),
	)

	db.registered_courses.insert(
		course_id=5,
		professor=7,
		year_=2016,
		semester=2,
		starting_date=datetime(2016,1,1),
		ending_date=datetime(2016,5,10),
	)

	db.registered_courses.insert(
		course_id=6,
		professor=7,
		year_=2016,
		semester=2,
		starting_date=datetime(2016,1,1),
		ending_date=datetime(2016,5,10),
	)

	db.registered_courses.insert(
		course_id=7,
		professor=7,
		year_=2016,
		semester=1,
		starting_date=datetime(2014,7,1),
		ending_date=datetime(2014,12,10),
	)

	## register 3 students for 5 courses each out of 7 registered courses
	db.student_registrations.insert(student_id=1,registered_course_id=3)
	db.student_registrations.insert(student_id=1,registered_course_id=2)
	db.student_registrations.insert(student_id=1,registered_course_id=1)
	db.student_registrations.insert(student_id=1,registered_course_id=4)
	db.student_registrations.insert(student_id=1,registered_course_id=5)
	db.student_registrations.insert(student_id=2,registered_course_id=3)
	db.student_registrations.insert(student_id=2,registered_course_id=4)
	db.student_registrations.insert(student_id=2,registered_course_id=6)
	db.student_registrations.insert(student_id=2,registered_course_id=7)
	db.student_registrations.insert(student_id=2,registered_course_id=1)
	db.student_registrations.insert(student_id=3,registered_course_id=3)
	db.student_registrations.insert(student_id=3,registered_course_id=1)
	db.student_registrations.insert(student_id=3,registered_course_id=5)
	db.student_registrations.insert(student_id=3,registered_course_id=6)
	db.student_registrations.insert(student_id=3,registered_course_id=2)
	db.student_registrations.insert(student_id=4,registered_course_id=3)
	db.student_registrations.insert(student_id=4,registered_course_id=4)
	db.student_registrations.insert(student_id=4,registered_course_id=5)
	db.student_registrations.insert(student_id=4,registered_course_id=7)
	db.student_registrations.insert(student_id=4,registered_course_id=1)

	## create 3 assignments in Design Practices course
	db.events.insert(
		registered_course_id=1,
		type_=0,
		name="Project Submission 1: Draft Requirement Document",
		description="<p><br></p><p>Organise 2 hr meeting of the team to</p><p>-Choose one of the Projects discussed in the class</p><p>-Discuss the specification of the selected project. Identify the aspects to be explored by team members&nbsp;</p><p>-Document the discussion and the initial specs of the project</p><p><br></p><p>Organise 2nd 2 hr meeting &nbsp;to</p><p>-Share the homework done by each team member</p><p>-Discuss and finalise the specs of the projects</p><p>-Prepare 1 or 2 page document on the draft project specification&nbsp;</p><p><br></p><p>Submit the draft Project Requirement Document by Wednesday mid night.</p><p>Add title of the project in the group excel sheet</p>",
		created_at=datetime.now(),
		deadline=datetime.now()-timedelta(days=-7),
		late_days_allowed=0
	)

	db.events.insert(
		registered_course_id=1,
		type_=0,
		name="Project Submission 2: Requirement Document in IEEE template format",
		description="<p>Submission Deadline 20 Feb Midnight.</p><p id='yui_3_17_2_3_1431040674495_308'>Recommended Process</p><p>-Meeting1 &nbsp;</p><p>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; Compete listing &nbsp;of User requirements</p><p>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; Create System Architecture</p><p id='yui_3_17_2_3_1431040674495_309'>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; Identify Use cases, Users, draw Use Case Diagram<br></p><p>-Meeting2</p><p>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp;Translate user requirement into system requirements</p><p>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp;Discuss and document Use cases including relevant Models</p><p>-Meeting3&nbsp;</p><p>&nbsp; &nbsp; &nbsp; &nbsp; Discuss each section of the IEEE template&nbsp;</p><p>&nbsp; &nbsp; &nbsp; &nbsp; Create Document as per IEEE template</p><p><br></p><p>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp;</p><p>&nbsp;</p><p><br></p>",
		created_at=datetime.now(),
		deadline=datetime.now()-timedelta(days=-7),
		late_days_allowed=2
	)

	db.events.insert(
		registered_course_id=1,
		type_=0,
		name="Project Submission 3 : Detailed Design Document",
		description="<p>Based on the Requirement Document, a detailed design document</p><p>will be created by each group.</p><p>It should have the following components</p><p>-Project Overview</p><p>-Architectural design with well identified Modules</p><p>-Modules specification &amp; its APIs</p><p>-Database Design</p><p>-User Interface Design</p><p>-Module internal data structures and processing if needed.</p><p>-Aprorpriate Diagrams as necessary</p><p>-Any other information as necessary</p><p>Design document should be complete from all aspects ( i.e Requirement &amp; design document should be adequate for any other programming team to develop the system without may further input)</p><p>You may use any apropriate format for this design document</p><p>Submission date 29th March.</p><p><br></p><p><br></p>",
		created_at=datetime.now(),
		deadline=datetime.now()-timedelta(days=-7),
		late_days_allowed=3
	)

	## Grades
	db.grades.insert(user_id=1, registered_course_id=1, name="Assignment 1", score=15, out_of=15, weightage=10)
	db.grades.insert(user_id=1, registered_course_id=1, name="Assignment 2", score=10, out_of=20, weightage=15)
	db.grades.insert(user_id=1, registered_course_id=1, name="Minor 1", score=25, out_of=30, weightage=25)

	db.grades.insert(user_id=2, registered_course_id=1, name="Assignment 1", score=15, out_of=15, weightage=10)
	db.grades.insert(user_id=2, registered_course_id=1, name="Assignment 2", score=18, out_of=20, weightage=15)
	db.grades.insert(user_id=2, registered_course_id=1, name="Minor 1", score=20, out_of=30, weightage=25)

	db.grades.insert(user_id=3, registered_course_id=1, name="Assignment 1", score=15, out_of=15, weightage=10)
	db.grades.insert(user_id=3, registered_course_id=1, name="Assignment 2", score=14, out_of=20, weightage=15)
	db.grades.insert(user_id=3, registered_course_id=1, name="Minor 1", score=23, out_of=30, weightage=25)

	db.grades.insert(user_id=4, registered_course_id=1, name="Assignment 1", score=15, out_of=15, weightage=10)
	db.grades.insert(user_id=4, registered_course_id=1, name="Assignment 2", score=20, out_of=20, weightage=15)
	db.grades.insert(user_id=4, registered_course_id=1, name="Minor 1", score=15, out_of=30, weightage=25)

	## create 4 threads in Different courses


	## Create Static Variables
	db.static_vars.insert(
		name="current_year",
		int_value=2016,
		string_value="2016"
	)

	db.static_vars.insert(
		name="current_sem",
		int_value=2,
		string_value="2"
	)
def api():
    return """
Moodle Plus API (ver 1.0)
-------------------------

Url: /default/login.json
Input params:
    userid: (string)
    password: (string)
Output params:
    success: (boolean) True if login success and False otherwise
    user: (json) User details if login is successful otherwise False


Url: /default/logout.json
Input params:
Output params:
    success: (boolean) True if logout successful and False otherwise


Url: /courses/list.json
Input params:
Output params:
    current_year: (int)
    current_sem: (int) 0 for summer, 1 break, 2 winter
    courses: (List) list of courses
    user: (dictionary) user details

Url: /threads/new.json
Input params:
    title: (string) can't be empty
    description: (string) can't be empty
    course_code: (string) must be a registered courses
Output params:
    success: (bool) True or False depending on whether thread was posted
    thread_id: (bool) id of new thread created

    """
