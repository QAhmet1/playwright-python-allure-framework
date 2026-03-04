import pytest
import allure
from faker import Faker

fake = Faker()

@allure.epic("Database Persistence Layer")
@allure.feature("Employee and Department Management")
class TestDatabase:
    """
    EN: Full Database Regression suite for relational data integrity and complex SQL operations.
    """

    @allure.story("Join Operations")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Verify INNER JOIN between employees and departments.")
    def test_verify_employee_join(self, setup_database_schema):
        db = setup_database_schema
        emp_name = "Ahmet_QA"
        
        with allure.step(f"Insert test employee '{emp_name}' linked to QA"):
            db.execute_non_query("INSERT INTO employees VALUES (101, ?, 1)", (emp_name,))
        
        with allure.step("Execute INNER JOIN and validate department mapping"):
            query = "SELECT e.name, d.dept_name FROM employees e INNER JOIN departments d ON e.dept_id = d.id"
            result = db.execute_query(query)
            assert result[0][0] == emp_name
            assert result[0][1] == 'QA'

    @allure.story("Aggregation Operations")
    def test_verify_multiple_employees_in_dept(self, setup_database_schema):
        db = setup_database_schema
        
        with allure.step("Insert multiple employees into QA"):
            db.execute_non_query("INSERT INTO employees VALUES (101, 'Zeynep', 1), (103, 'Ayse', 1)")
            
        with allure.step("Verify employee count for QA department"):
            query = "SELECT COUNT(*) FROM employees WHERE dept_id = 1"
            count = db.execute_query(query)[0][0]
            assert count == 2

    @allure.story("Join Operations")
    @allure.description("Identify unassigned departments using LEFT JOIN.")
    def test_verify_unassigned_department_left_join(self, setup_database_schema):
        db = setup_database_schema
        
        with allure.step("Assign an employee to QA, leaving Dev empty"):
            db.execute_non_query("INSERT INTO employees VALUES (999, 'System_User', 1)")
            
        with allure.step("Query departments with no assigned employees"):
            query = """
                SELECT d.dept_name FROM departments d 
                LEFT JOIN employees e ON d.id = e.dept_id 
                WHERE e.name IS NULL
            """
            result = db.execute_query(query)
            unassigned = [row[0] for row in result]
            assert "Dev" in unassigned

    @allure.story("Search and Filtering")
    def test_search_employee_by_name_pattern(self, setup_database_schema):
        db = setup_database_schema
        name = "Demir_Test"
        
        with allure.step(f"Insert employee with name '{name}'"):
            db.execute_non_query("INSERT INTO employees VALUES (104, ?, 2)", (name,))
            
        with allure.step("Search using LIKE operator"):
            result = db.execute_query("SELECT name FROM employees WHERE name LIKE 'Dem%'")
            assert result[0][0] == name

    @allure.story("Data Integrity")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_verify_unique_employee_id_constraint(self, setup_database_schema):
        db = setup_database_schema
        
        with allure.step("Insert initial record with ID 105"):
            db.execute_non_query("INSERT INTO employees VALUES (105, 'User_A', 1)")
            
        with allure.step("Verify that duplicate ID raises IntegrityError"):
            with pytest.raises(Exception) as excinfo:
                db.execute_non_query("INSERT INTO employees VALUES (105, 'User_B', 1)")
            assert "UNIQUE constraint failed" in str(excinfo.value)

    @allure.story("Aggregation Operations")
    def test_get_max_employee_id(self, setup_database_schema):
        db = setup_database_schema
        
        with allure.step("Insert records with specific IDs"):
            db.execute_non_query("INSERT INTO employees VALUES (10, 'A', 1), (500, 'B', 2)")
            
        with allure.step("Validate MAX(id) aggregate function"):
            max_id = db.execute_query("SELECT MAX(id) FROM employees")[0][0]
            assert max_id == 500

    @allure.story("Search and Filtering")
    def test_verify_subquery_filtering(self, setup_database_schema):
        db = setup_database_schema
        
        with allure.step("Insert employee into Dev department"):
            db.execute_non_query("INSERT INTO employees VALUES (106, 'Steve_Dev', 2)")
            
        with allure.step("Filter employees using a subquery for departments"):
            query = "SELECT name FROM employees WHERE dept_id NOT IN (SELECT id FROM departments WHERE dept_name='QA')"
            result = db.execute_query(query)
            assert result[0][0] == 'Steve_Dev'

    @allure.story("Aggregation Operations")
    def test_verify_employee_count_by_group(self, setup_database_schema):
        db = setup_database_schema
        
        with allure.step("Seed data for GROUP BY test"):
            db.execute_non_query("INSERT INTO employees VALUES (107, 'Ali', 1), (108, 'Veli', 1), (109, 'Can', 2)")
            
        with allure.step("Verify employee counts per department via GROUP BY"):
            results = dict(db.execute_query("SELECT dept_id, COUNT(*) FROM employees GROUP BY dept_id"))
            assert results[1] == 2  # QA
            assert results[2] == 1  # Dev

    @allure.story("Data Integrity")
    def test_verify_empty_table_initially(self, setup_database_schema):
        with allure.step("Verify that employees table is truncated after fresh setup"):
            count = setup_database_schema.execute_query("SELECT COUNT(*) FROM employees")[0][0]
            assert count == 0

    @allure.story("Complex Queries")
    def test_complex_join_with_sorting(self, setup_database_schema):
        db = setup_database_schema
        
        with allure.step("Insert data to test DESC sorting"):
            db.execute_non_query("INSERT INTO employees VALUES (110, 'Zeynep', 1), (111, 'Ahmet', 1)")
            
        with allure.step("Execute JOIN with ORDER BY DESC"):
            query = """
                SELECT e.name FROM employees e
                JOIN departments d ON e.dept_id = d.id
                WHERE d.dept_name = 'QA'
                ORDER BY e.name DESC
            """
            result = db.execute_query(query)
            # Result: [('Zeynep',), ('Ahmet',)]
            assert result[0][0] == 'Zeynep'
            assert result[1][0] == 'Ahmet'
            