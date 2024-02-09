from sims import db
from sqlalchemy import text

from sims.models import Human

create_get_family_money = text('''
CREATE OR REPLACE FUNCTION get_family_money(IN p_family_id INT)
RETURNS INTEGER AS $$
DECLARE
    total_salary INTEGER := 0;
    job_record RECORD;
BEGIN
    FOR job_record IN SELECT jobs.salary FROM human
                      JOIN jobs ON human.job_id = jobs.id
                      WHERE human.family_id = p_family_id
    LOOP
        total_salary := total_salary + job_record.salary;
    END LOOP;

    RETURN total_salary;
END;
$$ LANGUAGE plpgsql;
''')

create_get_family_members = text('''
CREATE OR REPLACE FUNCTION get_family_member_ids(IN p_family_id INT)
RETURNS TABLE (human_id INT)
AS $$
BEGIN
    RETURN QUERY
    SELECT id
    FROM human
    WHERE family_id = p_family_id;
END;
$$ LANGUAGE plpgsql;

''')


def get_family_money(family_id):
    # db.session.execute(create_get_family_money)

    result = db.session.execute(
        text("SELECT get_family_money(:family_id)"),
        {"family_id": family_id}
    )

    return result.scalar()


def get_family_members(family_id):
    result = db.session.execute(
        text("SELECT * FROM get_family_member_ids(:family_id)"),
        {"family_id": family_id}
    )

    humans = []
    for human_id in [row[0] for row in result.fetchall()]:
        humans.append(Human.query.get(human_id))

    return humans
