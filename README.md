App Name: OH

iOS Repository: https://github.com/joiewyng/OfficeHours

Fulfillment of Backend Requirements:
- SQLAlchemy Modeling
    - db_security.py
        - contains model User (for authentication)
    - db_course.py
        - contains model Course
    - db_hours.py
        - contains model Hour (information on one block of OH (translates to one event (or recurring event over multiple days of the week) on iOS side)
    - db_votes.py
        - contains model Cand (represents one candidate being voted for)
        
        Course-Hour are in a one-to-many relationship.
        
        
- users_dao.py
    - has methods to query tables, which are used in routes_hack.py for easier access
    - methods available for Course and Hour (and all interrelated calls), methods for Cand still in progress
    
- routes_hack.py
    - GET
        - get_hours() -> get all hours for particular course specified by query arguments in URL
        - get_course() -> get particular course specified by query arguments in URL
    - POST
        - create_course() -> creates new course entry in courses table, only used behind-the-scenes when "graduating" a legitimate vote to course-status.
        - create_hour_foo() -> create hours for an existing class, only used behind-the-scenes when "graduating" a legitimate vote to hour-status.
    - DELETE
        - def delete_course_foo() -> deletes specific course, only used behind-the-scenes when removing an illegitimate vote to course-status.
