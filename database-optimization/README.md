# Database Optimization

## 1. What are indexes?

**Database Indexes:**
- **Data structures** that improve query performance by creating sorted references to data
- **B-tree structures** (most common) that allow fast lookups without scanning entire tables
- **Additional storage** that trades space for speed
- **Automatic maintenance** by the database engine

**Core Concepts:**
- **Index** is a separate data structure that stores sorted references to table data
- **Index scan** allows finding specific rows without reading entire table
- **Index selectivity** determines how effective an index is (higher selectivity = better performance)
- **Index maintenance** includes rebuilding, updating statistics, and handling concurrent modifications

**Index Types:**
- **B-tree**: Balanced tree structure, supports equality, range queries, and sorting
- **Hash**: Fast equality lookups only, no range support
- **GiST**: Generalized Search Tree for geometric and custom data types
- **GIN**: Generalized Inverted Index for arrays, JSON, and full-text search
- **BRIN**: Block Range INdex for large tables with natural ordering

## 2. How to use indexes?

**Index Usage Principles:**
- **WHERE clauses**: Indexes are most effective for filtering data in WHERE conditions
- **JOIN conditions**: Foreign key columns should be indexed for efficient joins
- **ORDER BY**: Indexes can eliminate sorting operations when data is already ordered
- **GROUP BY**: Indexes can optimize grouping operations
- **Composite indexes**: Order matters - most selective column should be first

**Index Effectiveness Factors:**
- **Selectivity**: Higher unique values = better index performance
- **Data distribution**: Even distribution improves index efficiency
- **Query patterns**: Indexes should match actual query conditions
- **Column order**: In composite indexes, order affects usability

**Common Index Patterns:**
- **Single column**: For simple equality and range queries
- **Composite**: For multi-condition queries, order by selectivity
- **Partial**: For filtered subsets of data
- **Functional**: For computed columns or expressions
- **Covering**: Include all needed columns to avoid table lookups

## 3. Which kind of columns must be indexed?

**Must Index:**
- **Primary Keys**: Automatically indexed, essential for uniqueness and joins
- **Foreign Keys**: Critical for join performance, should always be indexed
- **Frequently filtered columns**: Columns used in WHERE clauses with high selectivity
- **Join columns**: Any column used in JOIN conditions
- **Sort columns**: Columns used in ORDER BY clauses
- **Search columns**: Columns used for text search or pattern matching

**Should Consider Indexing:**
- **Date/time columns**: Often used for range queries and filtering
- **Status/enum columns**: If used frequently in WHERE clauses
- **Numeric columns**: Used in range queries or aggregations
- **Composite columns**: When multiple columns are frequently used together

**Avoid Indexing:**
- **Low cardinality columns**: Columns with few unique values (gender, status with 2-3 values)
- **Rarely queried columns**: Columns that are seldom used in WHERE clauses
- **Frequently updated columns**: High update frequency reduces index effectiveness
- **Large text columns**: Unless using specialized indexes (GIN, GiST)
- **Computed columns**: Unless the computation is deterministic and indexed

**Index Selection Criteria:**
- **Query frequency**: How often the column is used in queries
- **Selectivity**: Ratio of unique values to total rows
- **Update frequency**: How often the column is modified
- **Storage cost**: Size of the index relative to table size

## 4. Why can't index everything?

**Storage Overhead:**
- **Space consumption**: Each index requires additional disk space proportional to table size
- **Memory usage**: Indexes consume buffer cache memory, reducing space for data
- **Growth factor**: Multiple indexes can increase total storage by 50-200%

**Write Performance Impact:**
- **Insert overhead**: Every INSERT must update all indexes (O(log n) per index)
- **Update overhead**: UPDATE operations may require index maintenance
- **Delete overhead**: DELETE operations must clean up index entries
- **Concurrency**: Index updates can cause lock contention

**Maintenance Overhead:**
- **Statistics updates**: Database must maintain index statistics for query planning
- **Rebuilding**: Indexes may need periodic rebuilding for optimal performance
- **Fragmentation**: Indexes can become fragmented over time
- **Query planning complexity**: More indexes = more complex query optimization

**Performance Trade-offs:**
- **Read vs Write**: Indexes improve read performance but degrade write performance
- **Memory vs Disk**: Indexes consume memory that could be used for data caching
- **Maintenance vs Performance**: More indexes require more maintenance overhead

**Optimal Index Count:**
- **General rule**: 3-5 indexes per table for most applications
- **Large tables**: May benefit from more specialized indexes
- **OLTP systems**: Fewer indexes due to high write frequency
- **OLAP systems**: More indexes acceptable due to read-heavy workloads

## 5. Wisdom `SELECT`

**Column Selection Principles:**
- **Select only needed columns**: Avoid SELECT * to reduce data transfer and memory usage
- **Consider column order**: Most frequently accessed columns first
- **Use aliases**: Improve readability and reduce typing
- **Avoid computed columns**: Unless necessary, compute in application layer

**Result Set Management:**
- **Use LIMIT**: Always limit large result sets to prevent memory issues
- **Pagination**: Implement proper pagination for large datasets
- **Streaming**: For very large results, consider streaming approaches
- **Caching**: Cache frequently accessed, rarely changing data

**Query Optimization Techniques:**
- **Avoid DISTINCT**: Use GROUP BY or unique constraints instead
- **Use EXISTS over IN**: EXISTS stops at first match, IN loads all results
- **Approximate counts**: Use statistics for large table counts
- **Index hints**: Use query hints when optimizer makes poor choices

**Performance Considerations:**
- **Network transfer**: Minimize data transferred between database and application
- **Memory usage**: Large result sets consume application memory
- **Processing time**: More columns = more processing overhead
- **Index efficiency**: Selectivity affects index usage effectiveness

## 6. Subqueries performance

**Correlated vs Non-Correlated Subqueries:**
- **Correlated subqueries**: Reference outer query columns, execute for each row (O(n²) complexity)
- **Non-correlated subqueries**: Independent of outer query, execute once (O(n) complexity)
- **Performance impact**: Correlated subqueries can be 10-1000x slower than alternatives

**Subquery Optimization Strategies:**
- **JOIN with GROUP BY**: Replace correlated subqueries with joins and aggregations
- **Window functions**: Use OVER clause for row-by-row calculations
- **EXISTS over IN**: EXISTS stops at first match, IN loads all results into memory
- **CTEs (Common Table Expressions)**: Break complex queries into readable, reusable parts

**Performance Characteristics:**
- **Correlated subqueries**: Execute N times (where N = outer query rows)
- **JOIN approach**: Single pass through data with proper indexing
- **Window functions**: Single pass with partitioning
- **EXISTS**: Stops at first match, optimal for large datasets

**Best Practices:**
- **Avoid correlated subqueries** in SELECT clause
- **Use appropriate join types** (INNER, LEFT, RIGHT) based on data requirements
- **Consider query plan** when choosing between alternatives
- **Test with real data volumes** to validate performance improvements

## 7. Analyze queries with `EXPLAIN`

**EXPLAIN Command Types:**
- **EXPLAIN**: Shows query plan without execution
- **EXPLAIN ANALYZE**: Shows plan with actual execution statistics
- **EXPLAIN BUFFERS**: Shows memory usage information
- **EXPLAIN FORMAT**: Output in different formats (TEXT, JSON, XML)

**Key Metrics to Analyze:**
- **Planning time**: Time spent creating execution plan
- **Execution time**: Actual query execution time
- **Rows**: Number of rows processed at each step
- **Loops**: Number of times each operation was performed
- **Buffers**: Memory usage (shared, read, written, temp)

**Common Execution Plans:**
- **Sequential Scan**: Reads entire table (slow for large tables)
- **Index Scan**: Uses index to find specific rows (fast)
- **Index Only Scan**: Uses index without table access (fastest)
- **Nested Loop**: For small datasets, joins row by row
- **Hash Join**: For larger datasets, builds hash table
- **Merge Join**: For sorted data, merges sorted streams

**Performance Red Flags:**
- **Sequential scans** on large tables without WHERE conditions
- **High loop counts** indicating inefficient joins
- **Large buffer usage** suggesting memory pressure
- **Temporary files** indicating insufficient memory
- **Poor row estimates** indicating outdated statistics

## 8. Bulk insert

**Bulk Insert Methods:**
- **Multi-row INSERT**: Insert multiple rows in single statement (10-100x faster than single inserts)
- **COPY command**: Fastest method for large datasets, bypasses SQL parser
- **Batch processing**: Group inserts into transactions for optimal performance
- **External tools**: Use database-specific tools (pg_bulkload, mysqlimport)

**Performance Optimization:**
- **Batch size**: Optimal 1000-10000 rows per batch (depends on row size and memory)
- **Transaction size**: Balance between memory usage and commit overhead
- **Index management**: Disable indexes during bulk load, rebuild after
- **Constraint handling**: Disable foreign keys and triggers during bulk operations

**Memory and Resource Considerations:**
- **Buffer size**: Adjust work_mem for large bulk operations
- **WAL (Write-Ahead Log)**: Bulk operations generate significant WAL traffic
- **Checkpoint frequency**: May need to adjust checkpoint settings
- **Disk I/O**: Sequential writes are much faster than random writes

**Best Practices:**
- **Use COPY for large datasets** (>10,000 rows)
- **Batch appropriately** to balance memory and performance
- **Disable unnecessary constraints** during bulk load
- **Monitor system resources** during bulk operations
- **Plan for recovery** in case of bulk operation failure

## 9. VACUUM

**What is VACUUM:**
- **Purpose**: Reclaims storage from dead tuples (deleted/updated rows) and updates statistics
- **MVCC mechanism**: PostgreSQL uses Multi-Version Concurrency Control, keeping old versions for transaction isolation
- **Dead tuples**: Rows marked as deleted but not physically removed from disk
- **Statistics**: Query planner relies on table statistics for optimal execution plans

**VACUUM Types:**
- **VACUUM**: Reclaims space, doesn't block reads/writes, doesn't update statistics
- **VACUUM ANALYZE**: Reclaims space and updates statistics for query planning
- **VACUUM FULL**: Rewrites entire table, blocks all access, maximum space reclamation
- **Auto VACUUM**: Automatic background process that runs VACUUM and ANALYZE

**When to Use VACUUM:**
- **After large DELETE operations**: Reclaim space from deleted rows
- **After large UPDATE operations**: Clean up old row versions
- **Regular maintenance**: Weekly VACUUM ANALYZE on active tables
- **Performance degradation**: When queries slow down due to table bloat
- **Storage pressure**: When disk space becomes limited

**VACUUM Configuration:**
- **autovacuum_vacuum_threshold**: Minimum dead tuples before auto VACUUM (default: 50)
- **autovacuum_vacuum_scale_factor**: Percentage of live tuples (default: 0.2)
- **autovacuum_analyze_threshold**: Minimum dead tuples before auto ANALYZE (default: 50)
- **autovacuum_analyze_scale_factor**: Percentage for auto ANALYZE (default: 0.1)

**Performance Impact:**
- **VACUUM**: Minimal impact, can run concurrently with normal operations
- **VACUUM ANALYZE**: Slight performance impact, updates query statistics
- **VACUUM FULL**: Significant impact, blocks all access to table
- **Auto VACUUM**: Background process, minimal user impact

## 10. Calculations balance

**Database vs Application Level Processing:**

**Database Level (Good for):**
- **Aggregations**: COUNT, SUM, AVG, MIN, MAX, GROUP BY operations
- **Simple mathematical operations**: Addition, subtraction, multiplication, division
- **Date/time calculations**: Date arithmetic, extraction of date parts
- **String operations**: Concatenation, substring, case conversion
- **Conditional logic**: CASE statements, simple IF-THEN-ELSE logic
- **Set operations**: UNION, INTERSECT, EXCEPT
- **Window functions**: Row numbering, running totals, moving averages

**Application Level (Good for):**
- **Complex business logic**: Multi-step calculations with conditional branching
- **External integrations**: API calls, third-party service interactions
- **File operations**: Reading/writing files, image processing
- **Complex algorithms**: Machine learning, recommendation engines, scoring systems
- **Data transformations**: Complex data formatting, validation rules
- **User interface logic**: Presentation formatting, user interaction handling

**Decision Factors:**
- **Performance**: Database operations are optimized for data processing
- **Scalability**: Database can handle large datasets more efficiently
- **Maintainability**: Business logic in application is easier to test and modify
- **Network overhead**: Minimize data transfer between database and application
- **Resource utilization**: Balance CPU usage between database and application servers

**Best Practices:**
- **Push filtering to database**: Use WHERE clauses to reduce data transfer
- **Aggregate in database**: Use GROUP BY and window functions
- **Keep business logic in application**: Complex rules belong in application code
- **Use stored procedures sparingly**: Only for performance-critical, database-specific operations
- **Consider data volume**: Large datasets benefit from database processing

## 11. MATERIALIZED VIEWS

**What are Materialized Views:**
- **Definition**: Physical storage of query results, unlike regular views that are virtual
- **Purpose**: Pre-compute expensive queries and store results for fast access
- **Storage**: Materialized views consume disk space proportional to result set size
- **Refresh**: Must be manually or automatically refreshed to reflect data changes

**When to Use Materialized Views:**
- **Expensive aggregations**: Complex GROUP BY operations with large datasets
- **Frequently accessed data**: Queries that are run often but don't need real-time data
- **Complex joins**: Multi-table joins that are computationally expensive
- **Reporting queries**: Dashboards and reports that can tolerate slightly stale data
- **Data warehousing**: Pre-computed summaries for analytical queries

**Refresh Strategies:**
- **Manual refresh**: Explicit REFRESH command when needed
- **Scheduled refresh**: Automated refresh using cron jobs or schedulers
- **Concurrent refresh**: REFRESH CONCURRENTLY allows reads during refresh
- **Incremental refresh**: Refresh only changed portions (requires careful design)

**Performance Considerations:**
- **Storage cost**: Materialized views consume disk space
- **Refresh overhead**: Full refresh can be expensive for large views
- **Data freshness**: Balance between performance and data currency
- **Index optimization**: Create indexes on materialized views for better query performance

**Best Practices:**
- **Choose refresh frequency** based on data freshness requirements
- **Monitor storage usage** and clean up unused materialized views
- **Use partitioning** for large materialized views to improve refresh performance
- **Consider incremental updates** for frequently changing data
- **Test refresh performance** before implementing in production
