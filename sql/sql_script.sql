-- Create 'user' table
CREATE TABLE IF NOT EXISTS `user` (
  user_id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(50) NOT NULL,
  email VARCHAR(100) NOT NULL
);

-- Create 'team' table
CREATE TABLE IF NOT EXISTS `team` (
  team_id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  description TEXT
);

-- Create 'user_team' table for user-team relationships
CREATE TABLE IF NOT EXISTS `user_team` (
  user_id INT,
  team_id INT,
  PRIMARY KEY (user_id, team_id),
  FOREIGN KEY (user_id) REFERENCES `user` (user_id),
  FOREIGN KEY (team_id) REFERENCES `team` (team_id)
);

-- Create 'task' table
CREATE TABLE IF NOT EXISTS `task` (
  task_id INT AUTO_INCREMENT PRIMARY KEY,
  title VARCHAR(255) NOT NULL,
  description TEXT,
  status VARCHAR(20) NOT NULL,
  user_id INT,
  FOREIGN KEY (user_id) REFERENCES `user` (user_id)
);

-- Insert sample data into 'user' table
INSERT INTO `user` (username, email) VALUES
  ('user1', 'user1@example.com'),
  ('user2', 'user2@example.com'),
  ('user3', 'user3@example.com'),
  ('johndoe', 'johndoe@example.com'),
  ('janedoe', 'janedoe@example.com'),
  ('alice', 'alice@example.com'),
  ('bob', 'bob@example.com');

-- Insert sample data into 'team' table
INSERT INTO `team` (name, description) VALUES
  ('Team A', 'Sample team A'),
  ('Team B', 'Sample team B'),
  ('Development', 'Development Team'),
  ('Support', 'Customer Support Team');

-- Insert sample data into 'user_team' table for user-team relationships
INSERT INTO `user_team` (user_id, team_id) VALUES
  (1, 1),  -- user1 in Team A
  (2, 1),  -- user2 in Team A
  (2, 2),  -- user2 in Team B
  (3, 2),  -- user3 in Team B
  (4, 3),  -- johndoe in Development Team
  (5, 3),  -- janedoe in Development Team
  (6, 4),  -- alice in Support Team
  (7, 4);  -- bob in Support Team;

-- Insert sample data into 'task' table
INSERT INTO `task` (title, description, status, user_id) VALUES
  ('Task 1', 'Sample task 1', 'Planned', 1),
  ('Task 2', 'Sample task 2', 'In Progress', 2),
  ('Task 3', 'Sample task 3', 'Needs Review', 3),
  ('Task 4', 'Another task', 'Done', 4),
  ('Task 5', 'Important task', 'Planned', 5),
  ('Task 6', 'Urgent task', 'In Progress', 6),
  ('Task 7', 'Task for Bob', 'Done', 7);
