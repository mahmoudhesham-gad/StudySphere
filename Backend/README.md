# API Endpoints

This document summarizes all API endpoints with details on request payloads and responses.

## User Endpoints
- **Register**  
  URL: `/user/register/`  
  Method: `POST`  
  Request Body:
  {
    "email": "string",
    "username": "string",
    "password": "string",
    "confirm_password": "string"
  }  
  Response (201 CREATED):
  {
    "user": "user_id"
  }  
  Cookies: HttpOnly cookies `access_token` and `refresh_token`.

- **Login**  
  URL: `/user/login/`  
  Method: `POST`  
  Request Body:
  {
    "email": "string",
    "password": "string"
  }  
  Response (200 OK):
  {
    "user": "user_id"
  }  
  Cookies: HttpOnly cookies `access_token` and `refresh_token`.

- **Logout**  
  URL: `/user/logout/`  
  Method: `POST`  
  Response (205 RESET CONTENT):
  {
    "message": "Logged out successfully"
  }  
  Effect: Refresh and access tokens are blacklisted and deleted via cookie removal.

- **Refresh Token**  
  URL: `/user/token/refresh/`  
  Method: `POST`  
  Requirement: Valid `refresh_token` cookie must be present  
  Response (200 OK):
  • Sets a new `access_token` cookie.

- **Verify Token**  
  URL: `/user/token/verify/`  
  Method: `POST`  
  Requirement: Valid `refresh_token` cookie must be present  
  Response (200 OK):
  {
    "message": "Token is valid"
  }

- **Profile**  
  URL: `/user/profile/`  
  Methods: `GET`, `PUT`  
  GET: Returns the user’s profile details as JSON.  
  PUT: Expects a JSON body with profile fields to update, and returns the updated profile.

## Materials Endpoints
- **Create Material**  
  URL: `/api/course/<uuid:course_id>/materials/create/`  
  Method: `POST`  
  Request Body Example:
  {
    "title": "Lecture Notes",
    "file": "<binary file upload>", // if type "document"
    "type": "document",            // or "url" for online resources
    "labels": [
        { "label": "uuid-of-label", "number": 1 }
    ]
  }  
  Response (201 CREATED):
  {
    "id": "uuid-of-material",
    "title": "Lecture Notes",
    "file": "/media/materials/<course_id>/file.pdf", // or "url": if applicable
    "type": "document",
    "created_at": "timestamp",
    "updated_at": "timestamp",
    "owner": "uuid-of-user"
  }

- **List Materials**  
  URL: `/api/course/<uuid:course_id>/materials/`  
  Method: `GET`  
  Response: JSON array where each object contains:
  {
    "id": "uuid-of-material",
    "title": "Lecture Notes",
    "file": "/media/materials/<course_id>/file.pdf", // may be null if URL is used
    "url": null,
    "type": "document",
    "created_at": "timestamp",
    "updated_at": "timestamp",
    "owner": "uuid-of-user"
  }

- **Update/Delete Material**  
  URL: `/api/materials/<uuid:material_id>/`  
  Methods: `PUT`, `DELETE`  
  PUT Request Example:
  {
    "title": "Updated Lecture Notes"
  }  
  PUT Response: Returns the updated material object as JSON.  
  DELETE Response: Returns a success status (e.g., 204 No Content).

- **Material Labels**  
  - *Add/Retrieve Labels for a Material*  
    URL: `/api/materials/<uuid:material_id>/labels/`  
    Methods: `GET`, `POST`  
    POST Request Example:
    {
      "labels": [
        { "label": "uuid-of-label", "number": 1 },
        { "label": "uuid-of-another-label", "number": 2 }
      ]
    }  
    GET Response: JSON array of label objects with embedded label details and assigned number.
  
  - *List Materials by Label*  
    URL: `/api/course/<uuid:course_id>/materials/labels/<label_id>/`  
    Method: `GET`  
    Response:
    {
      "label_name": "Priority",
      "materials": {
         "1": [ { "material": { ...material data... } } ],
         "2": [ { "material": { ...material data... } } ]
      }
    }

- **Material Comments**  
  - *Create Comment*  
    URL: `/api/comments/create/`  
    Method: `POST`  
    Request Body:
    {
      "material": "uuid-of-material",
      "Content": "This lecture was very helpful!"
    }  
    Response (201 CREATED):
    {
      "id": "uuid-of-comment",
      "material": "uuid-of-material",
      "User": "uuid-of-user",
      "Content": "This lecture was very helpful!",
      "CreatedAt": "timestamp"
    }
  
  - *List Comments for a Material*  
    URL: `/api/materials/<uuid:material_id>/comments/`  
    Method: `GET`  
    Response: JSON array of comment objects.
  
  - *Update/Delete Comment*  
    URL: `/api/comments/<uuid:comment_id>/`  
    Methods: `PUT`, `DELETE`  
    PUT Request Example:
    {
      "Content": "Updated comment text."
    }  
    PUT Response: Returns the updated comment object.

## Groups & Courses Endpoints
- **Groups**  
  - *List Groups*  
    URL: `/groups/list/`  
    Method: `GET`  
    Response: JSON array of group objects, where each group includes:
    {
      "id": "uuid",
      "owner": "user_id",
      "name": "Study Group",
      "description": "A group for studying",
      "join_type": "open",
      "post_permission": "members",
      "edit_permissions": "admins",
      "created_at": "timestamp"
    }
  
  - *Create Group*  
    URL: `/groups/`  
    Method: `POST`  
    Request Body:
    {
      "name": "Study Group",
      "description": "A group for studying",
      "join_type": "open",
      "post_permission": "members",
      "edit_permissions": "admins"
    }  
    Response: Returns the created group object.
  
  - *Retrieve/Update/Delete Group*  
    URL: `/groups/<uuid:group_id>/`  
    Methods: `GET`, `PUT`, `DELETE`  
    GET Response: Returns group details including nested arrays:
    {
      "id": "uuid",
      "owner": "user_id",
      "name": "Study Group",
      "description": "A group for studying",
      "join_type": "open",
      "post_permission": "members",
      "edit_permissions": "admins",
      "created_at": "timestamp",
      "members": [ { "user": { "id": "user_id", "username": "username" }, "user_role": "member", "joined_at": "timestamp" } ],
      "courses": [ { "id": "uuid", "group": { "id": "uuid", "name": "Study Group" }, "name": "Course Name", "description": "Course Description", "created_at": "timestamp" } ]
    }

- **Group Members**  
  - *List Group Members*  
    URL: `/groups/<uuid:group_id>/members/`  
    Method: `GET`  
    Response: JSON array of member objects.
  
  - *Add Group Member*  
    URL: `/groups/<uuid:group_id>/members/create/`  
    Method: `POST`  
    Request Body:
    {
      "user": "user_id"
    }  
    Response: Returns the new member object with user details, user_role, and joined_at timestamp.
  
  - *Retrieve/Update/Delete Group Member*  
    URL: `/groups/<uuid:group_id>/members/<uuid:user_id>/`  
    Methods: `GET`, `PUT`, `DELETE`  
    GET Response: Returns details of the specified group member.

- **Join Requests**  
  - *List and Create Join Requests*  
    URL: `/groups/<uuid:group_id>/join-requests/`  
    Methods: `GET`, `POST`  
    POST Request:
    {
      "group": "group_id",
      "user": "user_id"
    }  
    GET Response: Returns an array of join request objects.
  
  - *Retrieve/Update/Delete Join Request*  
    URL: `/join-requests/<uuid:join_request_id>/`  
    Methods: `GET`, `PUT`, `DELETE`  
    GET Response: Returns the join request details.

- **Courses**  
  - *List and Create Courses*  
    URL: `/groups/<uuid:group_id>/courses/`  
    Methods: `GET`, `POST`  
    POST Request:
    {
      "name": "Course Name",
      "description": "Course Description"
    }  
    GET Response: Returns an array of course objects including:
    {
      "id": "uuid",
      "group": { "id": "uuid", "name": "Study Group" },
      "name": "Course Name",
      "description": "Course Description",
      "created_at": "timestamp"
    }
  
  - *Retrieve/Update/Delete Course*  
    URL: `/courses/<uuid:course_id>/`  
    Methods: `GET`, `PUT`, `DELETE`  
    GET Response: Returns details of the course.
