# solution_shop
## Database Table Definition
I used the MYSQL version 8.0database is used,
one table is define with the name of T_NOTIFIED :
The table `t_notified` is defined as bwlow:

* `a_id`: automatically is increased.

* `a_shop_id`: Signifies, which shop the notification of threshold is sent.

* `a_month`: Signifies the month that the notification of threshold is sent.

* `a_threshold`: the type of threshold which can be defined 50% or 100%

after running the sql.db, please run the migrate.sql as well,


# Stylight coding assessment - Budget notifications
after doing the above steps, simply run the following:
python solution.py

## Test Cases:
there is some test scenarios which are done in solutions in file test_solution, the next tests can be done in todo list.
simply run python test_solution.py to get the automated result of tests.

## Notes:
I used the generator to fetch the data from database gradually to avoid the cpu usage.

## Additional thoughts
Please answer the following questions in your readme:
* Does your solution avoid sending duplicate notifications?
First: I have defined unique index as (a_shop_id, a_month, a_threshold) in table t_notified
in whcih it avoid adding the two duplicate values of (a_shop_id, a_month, a_threshold).

* How does your solution handle a budget change after a notification has already been sent?

in get_budget function , the query is in a way that it joins the newly added table(t_notified) and only contains the a_online = 1 ,
inside of function start_analyzing: 
if the budget is more than 50% and smaller than 100%:
    if is was not notified(notifed is None) >  then call show message and insert into the t_notified table, otherwise dont call this function to show messages and inserting into the t_notified,

if the budget is bigger than 100:
 definitely it's online status is 1, and definitely it was not notified that it reached to 100%, it is because of the query which only contains online=1, and since the field of a_online in table a_shops is update to be 0, so next time this wont be queried

I handled this mostly in SQL because the speed of SQL is higher than python, then for analyzing them, I have done in python
