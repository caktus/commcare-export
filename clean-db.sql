DO $$
DECLARE r RECORD;
BEGIN FOR r IN (
	SELECT tablename,
		schemaname
	FROM pg_tables
	WHERE schemaname IN ('public', 'test')
) LOOP EXECUTE 'DROP TABLE ' || quote_ident(r.schemaname) || '.' || quote_ident(r.tablename) || ' CASCADE';
END LOOP;
END $$;