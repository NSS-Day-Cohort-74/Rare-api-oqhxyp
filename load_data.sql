
DELETE FROM Users;
DELETE FROM DemotionQue;
DELETE FROM Subscriptions;
DELETE FROM Posts;
DELETE FROM Comments;
DELETE FROM Reactions;
DELETE FROM Tags;
DELETE FROM PostTags;
DELETE FROM Categories;

DROP TABLE IF EXISTS Users;
DROP TABLE IF EXISTS DemotionQue;
DROP TABLE IF EXISTS Subscriptions;
DROP TABLE IF EXISTS Comments;
DROP TABLE IF EXISTS Reactions;
DROP TABLE IF EXISTS Tags;
DROP TABLE IF EXISTS PostTags;
DROP TABLE IF EXISTS Categories;



CREATE TABLE "Users" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "first_name" varchar,
  "last_name" varchar,
  "email" varchar,
  "bio" varchar,
  "username" varchar,
  "password" varchar,
  "profile_image_url" varchar,
  "created_on" date,
  "active" bit,
  "is_admin" boolean
);

CREATE TABLE "DemotionQueue" (
  "action" varchar,
  "admin_id" INTEGER,
  "approver_one_id" INTEGER,
  FOREIGN KEY(`admin_id`) REFERENCES `Users`(`id`),
  FOREIGN KEY(`approver_one_id`) REFERENCES `Users`(`id`),
  PRIMARY KEY (action, admin_id, approver_one_id)
);


CREATE TABLE "Subscriptions" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "follower_id" INTEGER,
  "author_id" INTEGER,
  "created_on" date,
  FOREIGN KEY(`follower_id`) REFERENCES `Users`(`id`),
  FOREIGN KEY(`author_id`) REFERENCES `Users`(`id`)
);

CREATE TABLE "Posts" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "user_id" INTEGER,
  "category_id" INTEGER,
  "title" varchar,
  "publication_date" date,
  "image_url" varchar,
  "content" varchar,
  "approved" bit,
  FOREIGN KEY(`user_id`) REFERENCES `Users`(`id`)
);

CREATE TABLE "Comments" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "post_id" INTEGER,
  "author_id" INTEGER,
  "content" varchar,
  FOREIGN KEY(`post_id`) REFERENCES `Posts`(`id`),
  FOREIGN KEY(`author_id`) REFERENCES `Users`(`id`)
);

CREATE TABLE "Reactions" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "label" varchar,
  "image_url" varchar
);

CREATE TABLE "PostReactions" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "user_id" INTEGER,
  "reaction_id" INTEGER,
  "post_id" INTEGER,
  FOREIGN KEY(`user_id`) REFERENCES `Users`(`id`),
  FOREIGN KEY(`reaction_id`) REFERENCES `Reactions`(`id`),
  FOREIGN KEY(`post_id`) REFERENCES `Posts`(`id`)
);

CREATE TABLE "Tags" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "label" varchar
);

CREATE TABLE "PostTags" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "post_id" INTEGER,
  "tag_id" INTEGER,
  FOREIGN KEY(`post_id`) REFERENCES `Posts`(`id`),
  FOREIGN KEY(`tag_id`) REFERENCES `Tags`(`id`)
);

CREATE TABLE "Categories" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "label" varchar
);

INSERT INTO Categories (label) VALUES 
('News'), 
('Technology'), 
('Entertainment');

-- Inserting sample tags
INSERT INTO Tags (label) VALUES 
('JavaScript'), 
('Python'), 
('React');

-- Inserting sample reactions from AI
INSERT INTO Reactions (label, image_url) VALUES 
('happy', '😀'),
('sad', '😭'),
('angry', '😡');

-- Inserting sample users
INSERT INTO Users (first_name, last_name, email, bio, username, password, profile_image_url, created_on, active, is_admin) VALUES 
('John', 'Doe', 'john.doe@example.com', 'Software Engineer', 'johndoe', 'hashedpassword1', '🧔‍♂️', '2024-03-01', 1, 1),
('Jane', 'Smith', 'jane.smith@example.com', 'Web Developer', 'janesmith', 'hashedpassword2', '👩‍🔬', '2024-03-01', 1, 0),
('Alice', 'Johnson', 'alice.johnson@example.com', 'Tech Blogger', 'alicej', 'hashedpassword3', '🧟‍♀️', '2024-03-01', 1, 0);

-- Inserting sample subscriptions (User follows another user)
INSERT INTO Subscriptions (follower_id, author_id, created_on) VALUES 
(1, 2, '2024-03-01'),
(2, 3, '2024-03-01');

-- Inserting sample posts
INSERT INTO Posts (user_id, category_id, title, publication_date, image_url, content, approved) VALUES 
(1, 1, 'The Future of AI', '2024-03-02', 'https://w0.peakpx.com/wallpaper/209/381/HD-wallpaper-background-abstract-1-jpg-design-colors-blue-thumbnail.jpg', 'AI is growing fast...', 1),
(2, 2, 'JavaScript Best Practices', '2024-03-02', 'https://tinyjpg.com/images/social/website.jpg', 'Write cleaner JavaScript...', 1);

-- Inserting sample comments
INSERT INTO Comments (post_id, author_id, content) VALUES 
(1, 2, 'Great article on AI!'),
(2, 3, 'Loved the tips on JavaScript!');

-- Inserting sample post reactions
INSERT INTO PostReactions (user_id, reaction_id, post_id) VALUES 
(1, 1, 1), 
(2, 2, 2);

-- Inserting sample post tags (linking posts with tags)
INSERT INTO PostTags (post_id, tag_id) VALUES 
(1, 1), -- JavaScript tag for post 1
(2, 2); -- Python tag for post 2
