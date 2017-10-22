DROP TABLE IF EXISTS portfolio;

CREATE TABLE portfolio
(
  ticker      VARCHAR(6),
  strategy_id INT,
  qty         INT,
  purch_cost  NUMERIC,
  sale_cost   NUMERIC,
  purchase_dt DATETIME,
  sale_dt     DATETIME
);


DROP TABLE IF EXISTS curr_price;
CREATE TABLE curr_price
(
  ticker  VARCHAR(6),
  curr_price  NUMERIC
);


DROP TABLE IF EXISTS curr_price;
CREATE TABLE curr_price
(
  ticker  VARCHAR(6),
  curr_price  NUMERIC
);


DROP TABLE IF EXISTS tickers;

CREATE TABLE tickers
(
  tid INT,
  ticker VARCHAR(6),
  company_name VARCHAR(30)
);