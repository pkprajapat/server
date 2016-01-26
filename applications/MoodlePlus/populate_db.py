## Populate DB Script

## clear database
for table in db.tables():
	try:
		db(db[table].id>0).delete()
		print "Cleared",table
	except Exception, e:
		print "Couldn't clear",table

## create 5 students
db.users.insert(
	first_name="Abhishek",
	last_name="Kumar",
	email="abhishek.iitd16@gmail.com",
	username="cs5110272",
	entry_no="2011CS50272",
	type_=0,
	password="1",
)

db.users.insert(
	first_name="Jasmeet",
	last_name="Saini",
	email="jasmeet.sn@gmail.com",
	username="cs5110281",
	entry_no="2011CS50281",
	type_=0,
	password="1",
)

db.users.insert(
	first_name="Abhishek",
	last_name="Bansal",
	email="abhishek.bansal@gmail.com",
	username="cs5110271",
	entry_no="2011CS50271",
	type_=0,
	password="1",
)

db.users.insert(
	first_name="Rhythm",
	last_name="Gupta",
	email="cs1110247@cse.iitd.ac.in",
	username="cs1110247",
	entry_no="2011CS10247",
	type_=0,
	password="1",
)

db.users.insert(
	first_name="Gautam",
	last_name="Jain",
	email="gautampremjain@gmail.com",
	username="cs1110217",
	entry_no="2011CS10217",
	type_=0,
	password="1",
)

## create 3 professors
db.users.insert(
	first_name="Suresh",
	last_name="Gupta",
	email="scgupta@cse.moodle.in",
	username="scgupta",
	entry_no="scgupta",
	type_=1,
	password="1",
)

db.users.insert(
	first_name="Mausam",
	last_name="Mausam",
	email="mausam@cse.iitd.ac.in",
	username="mausam",
	entry_no="mausam",
	type_=1,
	password="1",
)

db.users.insert(
	first_name="Subodh",
	last_name="Kumar",
	email="subodh@cse.iitd.ac.in",
	username="subodh",
	entry_no="subodh",
	type_=1,
	password="1",
)


## create 9 courses
db.courses.insert(
	name="Software Engineering",
	code="csl740",
	description="Introduction to the concepts of Software Design and Engineering.",
	credits=4,
	l_t_p="3-0-2"
)

db.courses.insert(
	name="Parallel Programming",
	code="csl730",
	description="Introduction to concurrent systems and programming style.",
	credits=4,
	l_t_p="3-0-2"
)

db.courses.insert(
	name="Artificial Intelligence",
	code="csl333",
	description="Introduction to Artificial Intelligence.",
	credits=4,
	l_t_p="3-0-2"
)

db.courses.insert(
	name="Natural Language Processing",
	code="csl772",
	description="Introduction to Natural Language Processing.",
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
	name="Design Practices in Computer Science",
	code="csp301",
	description="Design Practices in Computer Science.",
	credits=3,
	l_t_p="1-0-4"
)

db.courses.insert(
	name="Advanced Computer Graphics",
	code="csl859",
	description="Graduate course on Advanced Computer Graphics",
	credits=4,
	l_t_p="3-0-2"
)

db.courses.insert(
	name="Data Structures",
	code="csl201",
	description="Introduction to Data Structures.",
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



## create 9 registered courses
db.registered_courses.insert(	
	course_id=1,
	professor=6,
	year_=2015,
	semester=2,
	starting_date=datetime(2015,1,1),
	ending_date=datetime(2015,5,10),
)

db.registered_courses.insert(
	course_id=2,
	professor=7,
	year_=2015,
	semester=2,
	starting_date=datetime(2015,1,1),
	ending_date=datetime(2015,5,10),
)

db.registered_courses.insert(
	course_id=3,
	professor=6,
	year_=2015,
	semester=2,
	starting_date=datetime(2015,1,1),
	ending_date=datetime(2015,5,10),
)

db.registered_courses.insert(
	course_id=4,
	professor=6,
	year_=2015,
	semester=2,
	starting_date=datetime(2015,1,1),
	ending_date=datetime(2015,5,10),
)

db.registered_courses.insert(
	course_id=5,
	professor=7,
	year_=2015,
	semester=2,
	starting_date=datetime(2015,1,1),
	ending_date=datetime(2015,5,10),
)

db.registered_courses.insert(
	course_id=6,
	professor=8,
	year_=2015,
	semester=2,
	starting_date=datetime(2015,1,1),
	ending_date=datetime(2015,5,10),
)

db.registered_courses.insert(
	course_id=7,
	professor=8,
	year_=2015,
	semester=1,
	starting_date=datetime(2014,7,1),
	ending_date=datetime(2014,12,10),
)

db.registered_courses.insert(
	course_id=8,
	professor=7,
	year_=2015,
	semester=1,
	starting_date=datetime(2014,7,1),
	ending_date=datetime(2014,12,10),
)

db.registered_courses.insert(
	course_id=8,
	professor=6,
	year_=2015,
	semester=2,
	starting_date=datetime(2015,1,1),
	ending_date=datetime(2015,5,10),
)

## register 3 students for 6 courses each out of 9 registered courses
db.student_registrations.insert(student_id=1,registered_course_id=1)
db.student_registrations.insert(student_id=1,registered_course_id=2)
db.student_registrations.insert(student_id=1,registered_course_id=5)
db.student_registrations.insert(student_id=1,registered_course_id=7)
db.student_registrations.insert(student_id=1,registered_course_id=8)
db.student_registrations.insert(student_id=1,registered_course_id=9)
db.student_registrations.insert(student_id=2,registered_course_id=1)
db.student_registrations.insert(student_id=2,registered_course_id=4)
db.student_registrations.insert(student_id=2,registered_course_id=6)
db.student_registrations.insert(student_id=2,registered_course_id=7)
db.student_registrations.insert(student_id=2,registered_course_id=8)
db.student_registrations.insert(student_id=2,registered_course_id=9)
db.student_registrations.insert(student_id=3,registered_course_id=1)
db.student_registrations.insert(student_id=3,registered_course_id=3)
db.student_registrations.insert(student_id=3,registered_course_id=5)
db.student_registrations.insert(student_id=3,registered_course_id=6)
db.student_registrations.insert(student_id=3,registered_course_id=8)
db.student_registrations.insert(student_id=3,registered_course_id=9)

## create 3 assignments in Software engineering course
db.events.insert(registered_course_id=1,type_=0,name="Project Submission 1: Draft Requirement Document",description="<p><br></p><p>Organise 2 hr meeting of the team to</p><p>-Choose one of the Projects discussed in the class on Wed 21st Jan</p><p>-Discuss the specification of the selected project. Identify the aspects to be explored by team members&nbsp;</p><p>-Document the discussion and the initial specs of the project</p><p><br></p><p>Organise 2nd 2 hr meeting &nbsp;to</p><p>-Share the homework done by each team member</p><p>-Discuss and finalise the specs of the projects</p><p>-Prepare 1 or 2 page document on the draft project specification&nbsp;</p><p><br></p><p>Submit the draft Project Requirement Document by Wed (28) mid night.</p><p>Add title of the project in the group excel sheet</p>",created_at=datetime.now(),deadline=datetime.now()-timedelta(days=-7),late_days_allowed=5)
db.events.insert(
	registered_course_id=1,
	type_=0,
	name="Project Submission 2: Requirement Document in IEEE template format",
	description="<p>Submission Deadline 20 Feb Midnight.</p><p id='yui_3_17_2_3_1431040674495_308'>Recommended Process</p><p>-Meeting1 &nbsp;</p><p>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; Compete listing &nbsp;of User requirements</p><p>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; Create System Architecture</p><p id='yui_3_17_2_3_1431040674495_309'>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; Identify Use cases, Users, draw Use Case Diagram<br></p><p>-Meeting2</p><p>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp;Translate user requirement into system requirements</p><p>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp;Discuss and document Use cases including relevant Models</p><p>-Meeting3&nbsp;</p><p>&nbsp; &nbsp; &nbsp; &nbsp; Discuss each section of the IEEE template&nbsp;</p><p>&nbsp; &nbsp; &nbsp; &nbsp; Create Document as per IEEE template</p><p><br></p><p>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp;</p><p>&nbsp;</p><p><br></p>",
	created_at=datetime.now(),
	deadline=datetime.now()-timedelta(days=-7),
	late_days_allowed=5)
db.events.insert(registered_course_id=1,type_=0,name="Project Submission 5 : Detailed Design Document",description="<p>Based on the Requirement Document, a detailed design document</p><p>will be created by each group.</p><p>It should have the following components</p><p>-Project Overview</p><p>-Architectural design with well identified Modules</p><p>-Modules specification &amp; its APIs</p><p>-Database Design</p><p>-User Interface Design</p><p>-Module internal data structures and processing if needed.</p><p>-Aprorpriate Diagrams as necessary</p><p>-Any other information as necessary</p><p>Design document should be complete from all aspects ( i.e Requirement &amp; design document should be adequate for any other programming team to develop the system without may further input)</p><p>You may use any apropriate format for this design document</p><p>Submission date 29th March.</p><p><br></p><p><br></p>",created_at=datetime.now(),deadline=datetime.now()-timedelta(days=-7),late_days_allowed=5)


## Grades
db.grades.insert(user_id=1, registered_course_id=1, name="Assignment 1", score=15, out_of=15, weightage=10)
db.grades.insert(user_id=1, registered_course_id=1, name="Assignment 2", score=18, out_of=20, weightage=15)
db.grades.insert(user_id=1, registered_course_id=1, name="Minor 1", score=25, out_of=30, weightage=25)

## create 4 threads in Different courses


## Create Static Variables
db.static_vars.insert(
	name="current_year",
	int_value=2015,
	string_value="2015"
)

db.static_vars.insert(
	name="current_sem",
	int_value=2,
	string_value="2"
)
