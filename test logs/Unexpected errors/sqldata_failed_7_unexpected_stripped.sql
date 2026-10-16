
ALTER TABLE GROUP1.[vendor_tb] ADD PRIMARY KEY ([ve_code]);

-- Failed (312 ms)
-- [Microsoft][ODBC Driver 17 for SQL Server][SQL Server]The CREATE UNIQUE INDEX statement terminated because a duplicate key was found for the object name 'GROUP1.vendor_tb' and the index name 'PK__vendor_t__9CD71C9DE38E565E'. The duplicate key value is (ACME ).

CREATE UNIQUE INDEX [idx_fa_interface_code] ON GROUP1.[termyear_tb] ([term_fa_interface_code]);

-- Failed (0 ms)
-- [Microsoft][ODBC Driver 17 for SQL Server][SQL Server]The CREATE UNIQUE INDEX statement terminated because a duplicate key was found for the object name 'GROUP1.termyear_tb' and the index name 'idx_fa_interface_code'. The duplicate key value is (<NULL>).

CREATE UNIQUE INDEX [idx_sect_nbr_course_term] ON GROUP1.[section_tb] ([section_number], [course_id], [term_id]);

-- Failed (312 ms)
-- [Microsoft][ODBC Driver 17 for SQL Server][SQL Server]The CREATE UNIQUE INDEX statement terminated because a duplicate key was found for the object name 'GROUP1.section_tb' and the index name 'idx_sect_nbr_course_term'. The duplicate key value is (002 , 131099, 131216).


ALTER TABLE GROUP1.[ret_item_worklist_tb] ADD CONSTRAINT [fk_ret_item_work_to_vend] FOREIGN KEY ([ve_code]) REFERENCES GROUP1.[vendor_tb] ([ve_code]);

-- Failed (0 ms)
-- [Microsoft][ODBC Driver 17 for SQL Server][SQL Server]There are no primary or candidate keys in the referenced table 'GROUP1.vendor_tb' that match the referencing column list in the foreign key 'fk_ret_item_work_to_vend'.

ALTER TABLE GROUP1.[ret_header_whl_tb] ADD CONSTRAINT [fk_ret_head_to_vendor2] FOREIGN KEY ([ve_code]) REFERENCES GROUP1.[vendor_tb] ([ve_code]);

-- Failed (0 ms)
-- [Microsoft][ODBC Driver 17 for SQL Server][SQL Server]There are no primary or candidate keys in the referenced table 'GROUP1.vendor_tb' that match the referencing column list in the foreign key 'fk_ret_head_to_vendor2'.

ALTER TABLE GROUP1.[ret_header_tb] ADD CONSTRAINT [fk_ret_head_to_vendor] FOREIGN KEY ([ve_code]) REFERENCES GROUP1.[vendor_tb] ([ve_code]);

-- Failed (0 ms)
-- [Microsoft][ODBC Driver 17 for SQL Server][SQL Server]There are no primary or candidate keys in the referenced table 'GROUP1.vendor_tb' that match the referencing column list in the foreign key 'fk_ret_head_to_vendor'.

ALTER TABLE GROUP1.[ret_manual_invc_header_tb] ADD CONSTRAINT [fk_ret_man_inv_hdr_to_vendor] FOREIGN KEY ([ve_code]) REFERENCES GROUP1.[vendor_tb] ([ve_code]);

-- Failed (0 ms)
-- [Microsoft][ODBC Driver 17 for SQL Server][SQL Server]There are no primary or candidate keys in the referenced table 'GROUP1.vendor_tb' that match the referencing column list in the foreign key 'fk_ret_man_inv_hdr_to_vendor'.
