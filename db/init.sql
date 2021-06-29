USE  todo_app;

CREATE TABLE IF NOT EXISTS priorities (
  id INT(11) AUTO_INCREMENT NOT NULL,
  priority VARCHAR(255) NOT NULL,
  created_at DATETIME NOT NULL,
  updated_at DATETIME NOT NULL,
  PRIMARY KEY (id),
  INDEX idx_id (id)
);

CREATE TABLE IF NOT EXISTS tasks (
  id INT(11) AUTO_INCREMENT NOT NULL,
  title VARCHAR(30) NOT NULL,
  description VARCHAR(1000) NOT NULL,
  priority_id int(11) NOT NULL,
  due_date DATE NOT NULL,
  created_at DATETIME NOT NULL,
  updated_at DATETIME NOT NULL,
  completed_at DATETIME,
  PRIMARY KEY (id),
  INDEX idx_id (id),
  FOREIGN KEY (priority_id) REFERENCES priorities (id)
);

INSERT INTO
  priorities (priority, created_at, updated_at)
VALUES
  ('high', NOW(), NOW()),
  ('medium', NOW(), NOW()),
  ('low', NOW(), NOW());

INSERT INTO
  tasks (title, description, priority_id, due_date, created_at, updated_at)
VALUES
  ('Shopping', 'buy eggs', 1, DATE_ADD(DATE(NOW()), INTERVAL 7 DAY), NOW(), NOW()),
  ('Homework', 'solve math problems', 1, DATE_ADD(DATE(NOW()), INTERVAL 1 DAY), NOW(), NOW()),
  ('Prepare document', 'create documents for the next meeting', 2, DATE_ADD(DATE(NOW()), INTERVAL 1 MONTH), NOW(), NOW()),
  ('Change home', 'preview new home', 3, DATE_ADD(DATE(NOW()), INTERVAL 1 YEAR), NOW(), NOW());
