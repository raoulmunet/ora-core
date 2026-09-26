from ora_core import analyze_sql, normalize_identifier, split_statements


def test_insert_select_dependencies():
    sql = """
    INSERT INTO dwh.customer_dim (customer_id, customer_name)
    SELECT c.customer_id, c.customer_name
    FROM crm.customers c
    JOIN crm.customer_status s ON s.customer_id = c.customer_id
    WHERE s.active_flag = 'Y';
    """
    result = analyze_sql(sql)
    assert result.operations == ["INSERT"]
    assert result.write_objects == ["DWH.CUSTOMER_DIM"]
    assert result.read_objects == ["CRM.CUSTOMERS", "CRM.CUSTOMER_STATUS"]


def test_literals_do_not_create_fake_dependencies():
    result = analyze_sql("SELECT 'from fake.table' AS txt FROM dual;")
    assert result.read_objects == ["DUAL"]


def test_split_ignores_semicolon_in_literal():
    assert split_statements("select 'a;b' from dual; select 1 from dual;") == [
        "select 'a;b' from dual",
        "select 1 from dual",
    ]


def test_quoted_identifier_is_preserved():
    assert normalize_identifier('hr."MixedCase"') == 'HR."MixedCase"'
