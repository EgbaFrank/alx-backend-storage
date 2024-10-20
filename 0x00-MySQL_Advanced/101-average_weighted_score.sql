-- computes and store the average weighted score for all students
DELIMITER |

CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
	DECLARE done INT DEFAULT 0;
	DECLARE user_id INT;
	DECLARE weight_sum FLOAT;
	DECLARE num_weight_sum FLOAT;

	DECLARE cur_users CURSOR FOR SELECT id FROM users;

	DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;

	OPEN cur_users;

	WHILE done = 0 DO
		FETCH cur_users INTO user_id;

		-- Summing weights only for projects that the user participated in
		SELECT SUM(p.weight) INTO weight_sum
		FROM projects p
		JOIN corrections c ON p.id = c.project_id
		WHERE c.user_id = user_id;

		-- Calculating the weighted sum of scores for the user
		SELECT SUM(c.score * p.weight) INTO num_weight_sum
		FROM corrections c
		JOIN projects p ON c.project_id = p.id
		WHERE c.user_id = user_id;

		IF weight_sum > 0 THEN
			UPDATE users
			SET average_score = num_weight_sum / weight_sum
			WHERE id = user_id;
		ELSE
			UPDATE users
			SET average_score = 0
			WHERE id = user_id;
		END IF;
	END WHILE;

	CLOSE cur_users;
END |

DELIMITER ;
