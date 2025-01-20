# Task Management System

A Task Management System project implemented using Flask (RESTful API) and AWS serverless services (AWS Lambda, API Gateway and DynamoDB)


### Details
The system allows signing up as members and logging in as members or admin.

**Admins can:**
- View all tasks
- Create and assign new tasks with deadline to members
- Update old tasks with new details and assignee
- Delete tasks

**Members can:**
- View tasks assigned to them
- Update status of tasks assigned to them
- Enable or disable email notifications
- Request for admin access from other admins

The _system_ allows members to enable email notifications for update of tasks or creation of tasks assigned to them. They can also request for admin access which sends an email to other admins to approve and provide administrative access to user.

***NB:*** The system is currently hosted on [Render](https://tms-hwg6.onrender.com/) and can take a while to load when visited after a period of inactivity so kindly be patient

### In progress:
1. Refactor to use only static files for the frontend and host on AWS S3 bucket
1. Provide a CDK template and script(s) to deploy entire infrastructure on AWS
