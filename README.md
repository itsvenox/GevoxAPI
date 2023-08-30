# GevoxAPI


## Table of Contents

- [About](#about)
- [Features](#features)
- - [User Authentication](#user-authentication)
- - [Posts](#posts)
- - [Comments](#comments)
- - [Following/Unfollowing](#following/unfollowing)
- [Installation](#installation)
- [API Endpoints](#api-endpoints)


## About

GevoxAPI is a Django-based web application that provides a platform for users to interact through posts, comments, and more.

## Features

### User Authentication

- Register a new account.
- Log in with email or username.
- Log out and revoke authentication tokens.
- Admin-only functionality to ban users.

### Posts

- Create, edit, and delete posts.
- Like and unlike posts.
- Retrieve individual posts or a feed of posts.
- Tag posts with relevant sparks.

### Comments

- Add, edit, and delete comments on posts.
- View comments associated with a post.

### Following/Unfollowing

- Follow and unfollow other users.
- View the followers and following count on user profiles.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/iitsvenox/gevoxapi.git





## API Endpoints

### Authentication

#### User Login
- Endpoint: `/api/v1/auth/login/`
- Method: POST
- Example Request:
 ```json
 {
   "email": "user@example.com",
   "password": "your_password"
 }
 ```
 or
 ```json
 {
   "username": "your_username",
   "password": "your_password"
 }
 ```

#### User Signup
- Endpoint: `/api/v1/auth/signup/`
- Method: POST
- Example Request:
 ```json
 {
   "username": "new_user",
   "email": "new_user@example.com",
   "password": "your_password"
 }
 ```

#### User Logout
- Endpoint: `/api/v1/auth/logout/`
- Method: POST
- Example Request: (Include Authorization Header with Token)
 ```json
 {
   "Authorization": "Token your_token_here"
 }
 ```

### User Profiles

#### Get User Profile
- Endpoint: `/api/v1/user/<int:pk>/profile/`
- Method: GET
- Example Request: (No additional data required)

#### Follow User
- Endpoint: `/api/v1/user/<int:id>/follow/`
- Method: POST
- Example Request: (Include Authorization Header with Token)
 ```json
 {
   "Authorization": "Token your_token_here"
 }
 ```

#### Unfollow User
- Endpoint: `/api/v1/user/<int:id>/unfollow/`
- Method: POST
- Example Request: (Include Authorization Header with Token)
 ```json
 {
   "Authorization": "Token your_token_here"
 }
 ```

### Posts

#### Create Post
- Endpoint: `/api/v1/post/create-post/`
- Method: POST
- Example Request: (Include Authorization Header with Token)
 ```json
 {
   "title": "New Post",
   "description": "This is a new post.",
   "author": "your_id_here",
   "sparks": []
 }
 ```

#### Delete Post
- Endpoint: `/api/v1/post/delete-post/<int:post_id>/`
- Method: DELETE
- Example Request: (Include Authorization Header with Token)

...

## Likes and Comments

#### Like or Unlike Post
- Endpoint: `/api/v1/post/like/<int:post_id>/`
- Method: POST
- Example Request: (Include Authorization Header with Token)

#### Add Comment to Post
- Endpoint: `/api/v1/post/<int:post_id>/comment/add/`
- Method: POST
- Example Request: (Include Authorization Header with Token)
 ```json
 {
   "content": "This is a comment."
 }
 ```

#### Delete Comment
- Endpoint: `/api/v1/post/comment/<int:comment_id>/delete/`
- Method: DELETE
- Example Request: (Include Authorization Header with Token)

...

## Conclusion

This documentation provides an overview of the GevoxAPI project's endpoints and example requests. Feel free to explore and integrate these endpoints into your applications.

For more detailed information and additional endpoints, please refer to the source code and the respective app documentation.

