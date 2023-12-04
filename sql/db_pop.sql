-- Truncate tables
TRUNCATE TABLE `user_team`; -- Truncate user-team relationships
TRUNCATE TABLE `task`;
TRUNCATE TABLE `user`; -- Truncate users
TRUNCATE TABLE `team`;

-- Populate the database with new data
-- Sample Users
INSERT INTO `user` (username, email) VALUES
  ('user1', 'user1@example.com'),
  ('user2', 'user2@example.com'),
  ('user3', 'user3@example.com'),
  ('johndoe', 'johndoe@example.com'),
  ('janedoe', 'janedoe@example.com'),
  ('alice', 'alice@example.com'),
  ('bob', 'bob@example.com');

-- Sample Teams
INSERT INTO `team` (name, description) VALUES
  ('Team A', 'Sample team A'),
  ('Team B', 'Sample team B'),
  ('Development', 'Development Team'),
  ('Support', 'Customer Support Team');

-- User-Team Relationships
INSERT INTO `user_team` (user_id, team_id) VALUES
  (1, 1),  -- user1 in Team A
  (2, 1),  -- user2 in Team A
  (2, 2),  -- user2 in Team B
  (3, 2),  -- user3 in Team B
  (4, 3),  -- johndoe in Development Team
  (5, 3),  -- janedoe in Development Team
  (6, 4),  -- alice in Support Team
  (7, 4);  -- bob in Support Team;

-- Sample Tasks
INSERT INTO `task` (title, description, status, user_id) VALUES
  ('Task 1', 'Sample task 1', 'Planned', 1),
  ('Task 2', 'Sample task 2', 'In Progress', 2),
  ('Task 3', 'Sample task 3', 'Needs Review', 3),
  ('Task 4', 'Another task', 'Done', 4),
  ('Task 5', 'Important task', 'Planned', 5),
  ('Task 6', 'Urgent task', 'In Progress', 6),
  ('Task 7', 'Task for Bob', 'Done', 7);
