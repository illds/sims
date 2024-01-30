from sims import db
from sqlalchemy import text


update_human_location_procedure = text('''
    CREATE PROCEDURE update_human_location(
        p_human_id INT,
        p_x_coordinate INT,
        p_y_coordinate INT
    )
    AS $$
    BEGIN
        UPDATE Human SET x_coordinate = p_x_coordinate, y_coordinate = p_y_coordinate WHERE ID = p_human_id;
    END;
    $$ LANGUAGE plpgsql;
''')

# update_human_job_procedure = text('''
# CREATE OR REPLACE PROCEDURE change_job(IN human_id INT, IN new_job INT)
# LANGUAGE plpgsql
# AS $$
# BEGIN
#     UPDATE Human
#     SET job = new_job
#     WHERE ID = human_id;
#
#     RAISE NOTICE 'Job changed successfully for Human with ID %', human_id;
# END;
# $$;
# ''')

def update_human_location(human_id, x_coordinate, y_coordinate):
    db.session.execute(
        text("CALL update_human_location(:human_id, :x_coordinate, :y_coordinate)"),
        {"human_id": human_id, "x_coordinate": x_coordinate, "y_coordinate": y_coordinate}
    )

    db.session.commit()


# def update_human_job(human_id, job):
#     db.session.execute(update_human_job_procedure)
#
#     db.session.execute(
#         text("CALL update_human_location(:human_id, :job)"),
#         {"human_id": human_id, "job": job.name}
#     )
#
#     db.session.commit()