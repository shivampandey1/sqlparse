import pandas as pd

'''
need to implement the following:
SELECT ___ FROM ____ WHERE ____ LIMIT ____
e.g. SELECT city FROM df WHERE SALARY > 50000 LIMIT 5
-> return 5 cities in the df where the salary is above 50k

SELECT: what we are querying for (e.g. a specific column, like city)
-> done using dataframe column selection e.g. df['city']
FROM: this always has to be the provided JSON file, which is a single table (this assumption is backed by both the docs and my intuition)
-> done intuitively by df
WHERE: given a key(s), value(s) needs to meet condition(s) (e.g. age > 30 AND pop < 50000)
-> done using df.query(condition(s))
LIMIT: return the top n results, where n = LIMIT
-> done using df.head(n)
'''

def run_sql_query(sql_query, df):
    # Declare variables to be updated later
    where_part = None
    limit = None
    query_result = None

    # print("----------------------------")
    # print("sql query: ", sql_query)

    # Validating there is a table to query
    if 'FROM' not in sql_query:
        print("ERROR: Invalid query. Please provide a table to query")
        return

    # Extract SELECT, WHERE, LIMIT parts from the query
    select_part = sql_query.split("FROM")[0]
    select_part = select_part.replace("SELECT", "").strip()

    has_where = "WHERE" in sql_query
    has_limit = "LIMIT" in sql_query
    
    if has_where:
        where_part = sql_query.split("WHERE")[1]
        if has_limit:
            where_part = where_part.split("LIMIT")[0].strip()
        else:
            where_part = where_part.strip()
    
        # Modifying format for df.query syntax
        where_part = where_part.replace("AND", "&").replace("OR", "|").replace(" = ", " == ")

    if has_limit:
        limit_part = sql_query.split("LIMIT")[1]
        limit = int(limit_part.strip().rstrip(";"))

    # # Sanity Check
    # print("SELECT:", select_part)
    # print("WHERE:", where_part)
    # print("LIMIT", limit)
    
    # Execute query
    if has_where:
        query_result = df.query(where_part)
    else:
        query_result = df
    
    # Apply SELECT
    if select_part != '*':
        query_result = query_result[[col.strip() for col in select_part.split(",")]]
    
    # Apply LIMIT
    if has_limit:
        query_result = query_result.head(limit)

    # print(query_result)
    # print("----------------------------")
    return query_result

# ## Tests

# # Load the modified JSON data into a pandas DataFrame
# file_name = 'test.json'
# df = pd.read_json(file_name)

# # Test 1: Basic SELECT operation
# # This tests selecting a single column without any conditions.
# result = run_sql_query("SELECT state FROM df", df)
# assert len(result.columns) == 1 and 'state' in result.columns, "Test 1 Failed: SELECT operation is incorrect."

# # Test 2: SELECT with WHERE condition
# # Testing filtering with a single condition.
# result = run_sql_query("SELECT state FROM df WHERE pop > 20000000", df)
# assert len(result) == 4, "Test 2 Failed: WHERE condition filtering is incorrect."

# # Test 3: SELECT with complex WHERE condition (AND)
# # This tests the logical AND operation in filtering.
# result = run_sql_query("SELECT state FROM df WHERE pop > 10000000 AND region = 'South'", df)
# assert len(result) == 4, "Test 3 Failed: AND condition filtering is incorrect."

# # Test 4: SELECT with complex WHERE condition (OR)
# # Testing logical OR operation in filtering.
# result = run_sql_query("SELECT state FROM df WHERE region = 'Northeast' OR pop_male < 7000000", df)
# assert len(result) == 7, "Test 4 Failed: OR condition filtering is incorrect."

# # Test 5: SELECT with complex WHERE condition (OR)
# # Testing logical OR operation with nested AND operation in filtering.
# result = run_sql_query("SELECT * FROM df WHERE pop > 20000000 OR (pop_female > 5400000 AND region = 'South')", df)
# assert len(result) == 5, "Test 5 Failed: OR condition filtering is incorrect."

# # Test 6: Using LIMIT
# # This tests limiting the number of results returned.
# result = run_sql_query("SELECT * FROM df LIMIT 5", df)
# assert len(result) == 5, "Test 6 Failed: LIMIT is incorrect."

# # Test 7: Edge case with zero population
# # Testing behavior when population is zero.
# result = run_sql_query("SELECT state FROM df WHERE pop = 0", df)
# assert result.empty, "Test 7 Failed: Edge case for zero population is incorrect."

# # Test 8: != behaviour
# # Testing behavior when != operator is used.
# result = run_sql_query("SELECT region FROM df WHERE pop_male != 19453561", df)
# assert len(result) == 9, "Test 8 Failed: != operator filtering is incorrect."

# # Test 9: SELECT with multiple columns
# # Testing behavior when multiple columns are selected
# result = run_sql_query("SELECT state, region FROM df WHERE pop_female > 10000000", df)
# assert len(result) == 4, "Test 9 Failed: multiple column selection is incorrect."

# # Test 10: WHERE with comparing multiple columns
# # Testing behavior when multiple columns are compared to each other
# result = run_sql_query("SELECT state, region FROM df WHERE pop_female > pop_male AND pop > 20000000 LIMIT 1", df)
# assert len(result) == 1, "Test 10 Failed: multiple column comparison is incorrect."

# # Test 11: SELECT with complex nested WHERE condition (OR)
# # Testing logical OR operation with multiple nested AND operation in filtering.
# result = run_sql_query("SELECT * FROM df WHERE pop > 20000000 OR (pop_female > 5400000 AND (region = 'South' OR region = 'Midwest'))", df)
# assert len(result) == 7, "Test 11 Failed: Nested OR condition filtering is incorrect."
