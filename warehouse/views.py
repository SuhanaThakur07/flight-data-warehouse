from django.shortcuts import render

# Create your views here.
# from django.shortcuts import render
from django.db import connection

def format_rows(rows):
    """Convert all values in rows to strings to avoid Django formatting errors"""
    return [[str(col) if col is not None else '-' for col in row] for row in rows]

def dashboard(request):

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT 
                COALESCE(a.airline_name, 'GRAND TOTAL'),
                COALESCE(CAST(d.month AS TEXT), 'ALL'),
                COALESCE(ROUND(AVG(f.departure_delay)::numeric, 2), 0)::TEXT
            FROM warehouse_factflights f
            JOIN warehouse_dimairline a ON f.airline_id = a.id
            JOIN warehouse_dimdate d ON f.date_id = d.id
            GROUP BY ROLLUP(a.airline_name, d.month)
            ORDER BY a.airline_name, d.month
            LIMIT 20
        """)
        rollup_data = format_rows(cursor.fetchall())

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT a.airline_name, COUNT(*)::TEXT
            FROM warehouse_factflights f
            JOIN warehouse_dimairline a ON f.airline_id = a.id
            WHERE f.cancelled = TRUE
            GROUP BY a.airline_name
            ORDER BY COUNT(*) DESC
        """)
        cancelled_data = format_rows(cursor.fetchall())

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT 
                COALESCE(a.airline_name, 'ALL'),
                COALESCE(CAST(d.month AS TEXT), 'ALL'),
                COUNT(*)::TEXT
            FROM warehouse_factflights f
            JOIN warehouse_dimairline a ON f.airline_id = a.id
            JOIN warehouse_dimdate d ON f.date_id = d.id
            GROUP BY GROUPING SETS(
                (a.airline_name),
                (a.airline_name, d.month)
            )
            ORDER BY a.airline_name, d.month
            LIMIT 20
        """)
        drilldown_data = format_rows(cursor.fetchall())

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT 
                a.airline_name, 
                o.state,
                COALESCE(ROUND(AVG(f.arrival_delay)::numeric, 2), 0)::TEXT
            FROM warehouse_factflights f
            JOIN warehouse_dimairline a ON f.airline_id = a.id
            JOIN warehouse_dimairport o ON f.origin_id = o.id
            GROUP BY a.airline_name, o.state
            ORDER BY AVG(f.arrival_delay) DESC NULLS LAST
            LIMIT 20
        """)
        dice_data = format_rows(cursor.fetchall())

    return render(request, 'warehouse/dashboard.html', {
        'rollup_data': rollup_data,
        'cancelled_data': cancelled_data,
        'drilldown_data': drilldown_data,
        'dice_data': dice_data,
    })