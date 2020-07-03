# A Flask based api with mongodb and docker

This is a project for the Subject Information Systems. The app's name is MovieFlix and was built with Flask, Mongodb and Docker.
In general, a user simple "user" has some functionalities that those functionalities are extend when a user is an "admin"(create a movie, edit movie etc. See below).


# Run project
To run the project, docker is needed with docker-compose.
Then in the root folder of the project you can run the following commands:

    $ docker-compose build

then

    $ docker-compose up
or

    $ docker-compose up -d
	
Then you can open `http://127.0.0.1:5000` in your browser.

*If you run docker-compose in detach mode(`-d` param in command) you can stop all containers with:* 

    $ docker-compose down



## Create an admin 
If you want to experience the functionalities of an admin(simple users are restricted to some functionalities), because there is not a root/admin user already in the db(nor there are test db data to import), you should register in the app, and the open the mongodb container in the terminal, and change the category of your user to admin. 
Example:
After `docker-compose up -d` you can:

 1. Run the command `docker ps -a`  in the terminal in order to find the container id of mongo container.

 2. Found container id of mongo: 
`$ docker exec -it containerId mongo,` where as containerId, you have to specify the container id of mongo that you found in Step 1.
 3. Use MovieFlix db: 
 `$ use MovieFlix`
 4. Make your account admin: 
  `db.Users.updateOne({"email": "your_email"}, { $set: {"category": "admin"}})`
  
Now you are admin.




## Functionalities

The app has a variaty of functionalities.

 1. On the right of the navbar there are the **Login** and the **Register** buttons. You can register in the app with an email, username and your password ofcourse. This will create a simple user. Moreover, if you have already an account, you can login in the app, with your email and your password. This functionality is supported by the Flask-Login lib. You email acts as an id for the user.
 
 2. The app supports two kind of users. The admin and the user(a simple user). The admin as you will guess, he will have extra functionalities(see section **Create an admin**). 

3. As a simple user you can:
	- Click "**Movies**" that is located in the navbar. This will navigate you in the Movies page. 
	- In **Movies** page, you can see all movies in the table, search movies by specific criteria, or open a movie in view mode(in **Movie View** page)
	- You can navigate to **Movie View** page of a movie from **Movies** page.
	- In  **Movie View**, you can see all the details of a movie(title, description, year, actors, rating and see all the comments from all the users in the comments section that is under the **Create Comment** Button. 
	- You can also create a comment in that movie(just type your comment and hit the **Create Comment**) button. The you will be able to see your comment in the comment section.
	- You can also your comment if you like, by clicking the **X** button in the top right of the comment box.
	- From the top **Nav**, you can also head to the **Profile** page.
	- From **Profile** page, you have the option to delete your account if you like.
	
4. As an admin you have all the above functionalities but also the following:
	You will notice that a new item in the Nav has appeared, the **Admin Panel**
	In **Admin Panel** page, you can: 
	- Delete simple users but not admin users.
    - Upgrade a user to admin.
    
	In **Movies** page, you can: 
	- Delete a movie by specifying a **Title**. This will delete the movie with that title. If there are more movies with this the specified title, the oldest movie will be deleted.
	- You can navigate to the **Create Movie** page by clicking the **Create Movie** from where you can create a movie.
	- In the the Movies Table, you will notice that there is an **Edit** button. This will navigate you to the **Movie Edit** page where you can edit the movie from there.

	In **Movie View** page, you will notice you have extra functionalities as admin: 
	- You can also delete comments that have been submitted by other users. Note that you cannot delete a comment that has been created by another admin.

	In **Movie Create** page, that we mentioned above you can : 
	- You can create a new movie. Note that title and at least an actor are mandatory. Also you have to be careful with actors. You have to delimit the actors by a comma. For example: `actor1,actor2,actor3,...,actorN`
	
	In **Movie Edit** page, that we mentioned above you can : 
	- You can edit a movie. Note that you cannot remove the title and and all actors. Also you have to be careful with actors. You have to delimit the actors by a comma. For example: `actor1,actor2,actor3,...,actorN`