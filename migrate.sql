CREATE TABLE t_notified (
    a_id        INT(11)         NOT NULL AUTO_INCREMENT,
    a_shop_id       INT(11)         NOT NULL REFERENCES t_shops (a_id),
    a_month         DATE            NOT NULL,
    a_threshold ENUM('50%', '100%') NOT NULL,
    PRIMARY KEY (a_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE UNIQUE INDEX index_name ON t_notified(a_shop_id, a_month, a_threshold);

INSERT INTO t_budgets
    (a_shop_id, a_month, a_budget_amount, a_amount_spent)
VALUES
    (1, '2021-12-01', 870.00, 675.67),
    (2, '2021-12-01', 955.00, 851.63),
    (3, '2021-12-01', 610.00, 645.91),
    (4, '2021-12-01', 730.00, 736.92),
    (5, '2021-12-01', 530.00, 407.64),
    (6, '2021-12-01', 340.00, 646.32),
    (7, '2021-12-01', 880.00, 540.16),
    (8, '2021-12-01', 590.00, 765.64);