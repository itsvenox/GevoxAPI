# Project Name

Brief description of your project.

## Table of Contents

- [About](#about)
- [Features](#features)
- - [User Authentication](#user-authentication)
- - [Posts](#posts)
- - [Comments](#comments)
- - [Following/Unfollowing](#following/unfollowing)
- [Installation](#installation)
- [Usage](#usage)
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
   git clone https://github.com/yourusername/your-project.git
   cd your-project



## Usage

    Access the web application at http://localhost:8000.
    Register a new account or log in with existing credentials.
    Explore the platform by creating posts, liking posts, adding comments, and following other users.

## API Endpoints

Here are some of the main API endpoints available in the project. For detailed information, check the project's URLs and views files.

    POST /api/v1/auth/login/: Log in a user and get an authentication token.
    POST /api/v1/auth/signup/: Register a new user.
    POST /api/v1/post/create-post/: Create a new post.
    DELETE /api/v1/post/delete-post/<int:post_id>/: Delete a post.
    POST /api/v1/post/<int:post_id>/comment/add/: Add a comment to a post.
    DELETE /api/v1/post/comment/<int:comment_id>/delete/: Delete a comment.
    POST /api/v1/post/<int:post_id>/like/: Like or unlike a post.
