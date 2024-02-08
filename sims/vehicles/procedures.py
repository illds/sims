from sqlalchemy import text
from sims import db

update_vehicle_color_procedure = text('''CREATE OR REPLACE PROCEDURE change_vehicle_color(p_vehicle_id INT, p_new_color Color)
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE Vehicle SET color = p_new_color WHERE ID = p_vehicle_id;
END;
$$;''')


def update_vehicle_color(vehicle_id: int, color: str) -> None:
    db.session.execute(
        text("CALL change_vehicle_color(:p_vehicle_id, :p_new_color);"),
        {"p_vehicle_id": vehicle_id, "p_new_color": color}
    )

    db.session.commit()
