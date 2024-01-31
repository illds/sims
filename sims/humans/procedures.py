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

update_human_job_procedure = text('''
    CREATE PROCEDURE change_job(human_id INT, new_job_id INT)
    AS $$
    BEGIN
        UPDATE Human
        SET job_id = new_job_id
        WHERE ID = human_id;
    END;
    $$ LANGUAGE plpgsql;
''')

def update_human_location(human_id, x_coordinate, y_coordinate):
    # db.session.execute(update_human_location_procedure)

    db.session.execute(
        text("CALL update_human_location(:human_id, :x_coordinate, :y_coordinate)"),
        {"human_id": human_id, "x_coordinate": x_coordinate, "y_coordinate": y_coordinate}
    )

    db.session.commit()


def update_human_job(human_id, new_job_id):
    # db.session.execute(update_human_job_procedure)

    db.session.execute(
        text("CALL change_job(:human_id, :new_job_id)"),
        {"human_id": human_id, "new_job_id": new_job_id}
    )

    db.session.commit()