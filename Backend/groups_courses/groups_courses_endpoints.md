## groups_courses Endpoints

### Group Endpoints

#### List and Create Groups
- **URL:** `/groups/`
- **Method:** `POST`
- **URL:** `/groups/list/`
- **Method:** `GET`

**Request (POST):**
```json
{
    "name": "Study Group",
    "description": "A group for studying",
    "join_type": "open",
    "post_permission": "members",
    "edit_permissions": "admins"
}
```

**Response (GET):**
```json
[
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
]
```

**Response (POST):**
```json
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
```

#### Retrieve, Update, and Delete Group
- **URL:** `/groups/<uuid:group_id>/`
- **Method:** `GET`, `PUT`, `DELETE`

**Response (GET):**
```json
{
    "id": "uuid",
    "owner": "user_id",
    "name": "Study Group",
    "description": "A group for studying",
    "join_type": "open",
    "post_permission": "members",
    "edit_permissions": "admins",
    "created_at": "timestamp",
    "members": [
        {
            "user": {
                "id": "user_id",
                "username": "username"
            },
            "user_role": "member",
            "joined_at": "timestamp"
        }
    ],
    "courses": [
        {
            "id": "uuid",
            "group": {
                "id": "uuid",
                "name": "Study Group"
            },
            "name": "Course Name",
            "description": "Course Description",
            "created_at": "timestamp"
        }
    ]
}
```

### Group Member Endpoints

#### List and Create Group Members
- **URL:** `/groups/<uuid:group_id>/members/`
- **Method:** `GET`
- **URL:** `/groups/<uuid:group_id>/members/create/`
- **Method:** `POST`

**Request (POST):**
```json
{
    "user": "user_id"
}
```

**Response (GET):**
```json
[
    {
        "user": {
            "id": "user_id",
            "username": "username"
        },
        "user_role": "member",
        "joined_at": "timestamp"
    }
]
```

**Response (POST):**
```json
{
    "user": {
        "id": "user_id",
        "username": "username"
    },
    "user_role": "member",
    "joined_at": "timestamp"
}
```

#### Retrieve, Update, and Delete Group Member
- **URL:** `/groups/<uuid:group_id>/members/<uuid:user_id>/`
- **Method:** `GET`, `PUT`, `DELETE`

**Response (GET):**
```json
{
    "user": {
        "id": "user_id",
        "username": "username"
    },
    "user_role": "member",
    "joined_at": "timestamp"
}
```

### Join Request Endpoints

#### List and Create Join Requests
- **URL:** `/groups/<uuid:group_id>/join-requests/`
- **Method:** `GET`, `POST`

**Request (POST):**
```json
{
    "group": "group_id",
    "user": "user_id"
}
```

**Response (GET):**
```json
[
    {
        "user": {
            "id": "user_id",
            "username": "username"
        },
        "created_at": "timestamp"
    }
]
```

**Response (POST):**
```json
{
    "user": {
        "id": "user_id",
        "username": "username"
    },
    "created_at": "timestamp"
}
```

#### Retrieve, Update, and Delete Join Request
- **URL:** `/join-requests/<uuid:join_request_id>/`
- **Method:** `GET`, `PUT`, `DELETE`

**Response (GET):**
```json
{
    "user": {
        "id": "user_id",
        "username": "username"
    },
    "created_at": "timestamp"
}
```

### Course Endpoints

#### List and Create Courses
- **URL:** `/groups/<uuid:group_id>/courses/`
- **Method:** `GET`, `POST`

**Request (POST):**
```json
{
    "name": "Course Name",
    "description": "Course Description"
}
```

**Response (GET):**
```json
[
    {
        "id": "uuid",
        "group": {
            "id": "uuid",
            "name": "Study Group"
        },
        "name": "Course Name",
        "description": "Course Description",
        "created_at": "timestamp"
    }
]
```

**Response (POST):**
```json
{
    "id": "uuid",
    "group": {
        "id": "uuid",
        "name": "Study Group"
    },
    "name": "Course Name",
    "description": "Course Description",
    "created_at": "timestamp"
}
```

#### Retrieve, Update, and Delete Course
- **URL:** `/courses/<uuid:course_id>/`
- **Method:** `GET`, `PUT`, `DELETE`

**Response (GET):**
```json
{
    "id": "uuid",
    "group": {
        "id": "uuid",
        "name": "Study Group"
    },
    "name": "Course Name",
    "description": "Course Description",
    "created_at": "timestamp"
}
```