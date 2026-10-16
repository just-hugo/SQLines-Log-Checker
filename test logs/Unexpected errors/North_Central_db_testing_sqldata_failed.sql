-- SQLines Data 3.3.773 x64 - Database Migration and Validation Tool.
-- Copyright (c) 2024 SQLines. All Rights Reserved.

-- Failed DDL SQL statements executed for the target database

-- Current timestamp: 2026-09-18 14:22:28.189

ALTER TABLE GROUP1.[mailord_item_tb] ADD DEFAULT dbo.UUIDtoSTR(newid()) FOR [moi_id];

-- Failed (0 ms)
-- [Microsoft][ODBC Driver 17 for SQL Server][SQL Server]Column "dbo" is not allowed in this context, and the user-defined function or aggregate "dbo.UUIDtoSTR" could not be found.

ALTER TABLE GROUP1.[mailord_shipment_tb] ADD DEFAULT dbo.UUIDtoSTR(newid()) FOR [mos_id];

-- Failed (0 ms)
-- [Microsoft][ODBC Driver 17 for SQL Server][SQL Server]Column "dbo" is not allowed in this context, and the user-defined function or aggregate "dbo.UUIDtoSTR" could not be found.

ALTER TABLE GROUP1.[payment_form_tb] ADD DEFAULT dbo.UUIDtoSTR(newid()) FOR [pf_id];

-- Failed (0 ms)
-- [Microsoft][ODBC Driver 17 for SQL Server][SQL Server]Column "dbo" is not allowed in this context, and the user-defined function or aggregate "dbo.UUIDtoSTR" could not be found.

ALTER TABLE GROUP1.[receiving_tb] ADD DEFAULT dbo.UUIDtoSTR(newid()) FOR [re_id];

-- Failed (0 ms)
-- [Microsoft][ODBC Driver 17 for SQL Server][SQL Server]Column "dbo" is not allowed in this context, and the user-defined function or aggregate "dbo.UUIDtoSTR" could not be found.

ALTER TABLE GROUP1.[user_tb] ADD DEFAULT dbo.UUIDtoSTR(newid()) FOR [us_id];

-- Failed (0 ms)
-- [Microsoft][ODBC Driver 17 for SQL Server][SQL Server]Column "dbo" is not allowed in this context, and the user-defined function or aggregate "dbo.UUIDtoSTR" could not be found.

ALTER TABLE GROUP1.[inv_discrepancy_tb] ADD DEFAULT dbo.UUIDtoSTR(newid()) FOR [invdis_id];

-- Failed (0 ms)
-- [Microsoft][ODBC Driver 17 for SQL Server][SQL Server]Column "dbo" is not allowed in this context, and the user-defined function or aggregate "dbo.UUIDtoSTR" could not be found.

ALTER TABLE GROUP1.[promo_item_tb] ADD DEFAULT dbo.UUIDtoSTR(newid()) FOR [pm_itm_id];

-- Failed (0 ms)
-- [Microsoft][ODBC Driver 17 for SQL Server][SQL Server]Column "dbo" is not allowed in this context, and the user-defined function or aggregate "dbo.UUIDtoSTR" could not be found.

ALTER TABLE GROUP1.[promo_dept_tb] ADD DEFAULT dbo.UUIDtoSTR(newid()) FOR [pm_dept_id];

-- Failed (0 ms)
-- [Microsoft][ODBC Driver 17 for SQL Server][SQL Server]Column "dbo" is not allowed in this context, and the user-defined function or aggregate "dbo.UUIDtoSTR" could not be found.

ALTER TABLE GROUP1.[promo_catgy_tb] ADD DEFAULT dbo.UUIDtoSTR(newid()) FOR [pm_cat_id];

-- Failed (15 ms)
-- [Microsoft][ODBC Driver 17 for SQL Server][SQL Server]Column "dbo" is not allowed in this context, and the user-defined function or aggregate "dbo.UUIDtoSTR" could not be found.

ALTER TABLE GROUP1.[promo_vendor_tb] ADD DEFAULT dbo.UUIDtoSTR(newid()) FOR [pm_vend_id];

-- Failed (0 ms)
-- [Microsoft][ODBC Driver 17 for SQL Server][SQL Server]Column "dbo" is not allowed in this context, and the user-defined function or aggregate "dbo.UUIDtoSTR" could not be found.

ALTER TABLE GROUP1.[mailord_shipment_item_tb] ADD DEFAULT dbo.UUIDtoSTR(newid()) FOR [mosi_id];

-- Failed (0 ms)
-- [Microsoft][ODBC Driver 17 for SQL Server][SQL Server]Column "dbo" is not allowed in this context, and the user-defined function or aggregate "dbo.UUIDtoSTR" could not be found.

ALTER TABLE GROUP1.[site_tb] ADD DEFAULT dbo.UUIDtoSTR(newid()) FOR [site_id];

-- Failed (0 ms)
-- [Microsoft][ODBC Driver 17 for SQL Server][SQL Server]Column "dbo" is not allowed in this context, and the user-defined function or aggregate "dbo.UUIDtoSTR" could not be found.

ALTER TABLE GROUP1.[ProcessQueue] ADD DEFAULT dbo.UUIDtoSTR(newid()) FOR [ProcessId];

-- Failed (0 ms)
-- [Microsoft][ODBC Driver 17 for SQL Server][SQL Server]Column "dbo" is not allowed in this context, and the user-defined function or aggregate "dbo.UUIDtoSTR" could not be found.

ALTER TABLE GROUP1.[transaction_audit_tb] ADD DEFAULT dbo.UUIDtoSTR(newid()) FOR [ta_id];

-- Failed (0 ms)
-- [Microsoft][ODBC Driver 17 for SQL Server][SQL Server]Column "dbo" is not allowed in this context, and the user-defined function or aggregate "dbo.UUIDtoSTR" could not be found.

ALTER TABLE GROUP1.[language_translation_tb] ADD DEFAULT dbo.UUIDtoSTR(newid()) FOR [lt_id];

-- Failed (0 ms)
-- [Microsoft][ODBC Driver 17 for SQL Server][SQL Server]Column "dbo" is not allowed in this context, and the user-defined function or aggregate "dbo.UUIDtoSTR" could not be found.

ALTER TABLE GROUP1.[isbn_alias] ADD DEFAULT dbo.UUIDtoSTR(newid()) FOR [ai_id];

-- Failed (0 ms)
-- [Microsoft][ODBC Driver 17 for SQL Server][SQL Server]Column "dbo" is not allowed in this context, and the user-defined function or aggregate "dbo.UUIDtoSTR" could not be found.

ALTER TABLE GROUP1.[signature_capture_tb] ADD DEFAULT dbo.UUIDtoSTR(newid()) FOR [sig_id];

-- Failed (0 ms)
-- [Microsoft][ODBC Driver 17 for SQL Server][SQL Server]Column "dbo" is not allowed in this context, and the user-defined function or aggregate "dbo.UUIDtoSTR" could not be found.

ALTER TABLE GROUP1.[security_override_audit_tb] ADD DEFAULT dbo.UUIDtoSTR(newid()) FOR [soa_id];

-- Failed (0 ms)
-- [Microsoft][ODBC Driver 17 for SQL Server][SQL Server]Column "dbo" is not allowed in this context, and the user-defined function or aggregate "dbo.UUIDtoSTR" could not be found.

ALTER TABLE GROUP1.[chargeback_item_tb] ADD DEFAULT dbo.UUIDtoSTR(newid()) FOR [cbi_id];

-- Failed (16 ms)
-- [Microsoft][ODBC Driver 17 for SQL Server][SQL Server]Column "dbo" is not allowed in this context, and the user-defined function or aggregate "dbo.UUIDtoSTR" could not be found.

ALTER TABLE GROUP1.[follett_shipment_item_tb] ADD DEFAULT dbo.UUIDtoSTR(newid()) FOR [fsi_id];

-- Failed (0 ms)
-- [Microsoft][ODBC Driver 17 for SQL Server][SQL Server]Column "dbo" is not allowed in this context, and the user-defined function or aggregate "dbo.UUIDtoSTR" could not be found.

ALTER TABLE GROUP1.[follett_inventory_tb] ADD DEFAULT dbo.UUIDtoSTR(newid()) FOR [fi_id];

-- Failed (0 ms)
-- [Microsoft][ODBC Driver 17 for SQL Server][SQL Server]Column "dbo" is not allowed in this context, and the user-defined function or aggregate "dbo.UUIDtoSTR" could not be found.

ALTER TABLE GROUP1.[price_change_transaction_audit_tb] ADD DEFAULT dbo.UUIDtoSTR(newid()) FOR [pcta_id];

-- Failed (0 ms)
-- [Microsoft][ODBC Driver 17 for SQL Server][SQL Server]Column "dbo" is not allowed in this context, and the user-defined function or aggregate "dbo.UUIDtoSTR" could not be found.

ALTER TABLE GROUP1.[salespost_error_log_tb] ADD DEFAULT dbo.UUIDtoSTR(newid()) FOR [sperr_id];

-- Failed (0 ms)
-- [Microsoft][ODBC Driver 17 for SQL Server][SQL Server]Column "dbo" is not allowed in this context, and the user-defined function or aggregate "dbo.UUIDtoSTR" could not be found.

ALTER TABLE GROUP1.[customer_notes_tb] ADD DEFAULT dbo.UUIDtoSTR(newid()) FOR [cn_id];

-- Failed (0 ms)
-- [Microsoft][ODBC Driver 17 for SQL Server][SQL Server]Column "dbo" is not allowed in this context, and the user-defined function or aggregate "dbo.UUIDtoSTR" could not be found.

ALTER TABLE GROUP1.[membership_tb] ADD DEFAULT dbo.UUIDtoSTR(newid()) FOR [mb_id];

-- Failed (0 ms)
-- [Microsoft][ODBC Driver 17 for SQL Server][SQL Server]Column "dbo" is not allowed in this context, and the user-defined function or aggregate "dbo.UUIDtoSTR" could not be found.

ALTER TABLE GROUP1.[customer_membership_tb] ADD DEFAULT dbo.UUIDtoSTR(newid()) FOR [cumb_id];

-- Failed (0 ms)
-- [Microsoft][ODBC Driver 17 for SQL Server][SQL Server]Column "dbo" is not allowed in this context, and the user-defined function or aggregate "dbo.UUIDtoSTR" could not be found.

ALTER TABLE GROUP1.[customer_oas_tb_deleted] ADD DEFAULT dbo.UUIDtoSTR(newid()) FOR [oas_del_id];

-- Failed (0 ms)
-- [Microsoft][ODBC Driver 17 for SQL Server][SQL Server]Column "dbo" is not allowed in this context, and the user-defined function or aggregate "dbo.UUIDtoSTR" could not be found.

ALTER TABLE GROUP1.[used_book_parm_tb] ADD DEFAULT dbo.UUIDtoSTR(newid()) FOR [ub_id];

-- Failed (0 ms)
-- [Microsoft][ODBC Driver 17 for SQL Server][SQL Server]Column "dbo" is not allowed in this context, and the user-defined function or aggregate "dbo.UUIDtoSTR" could not be found.

ALTER TABLE GROUP1.[used_book_condition_parm_tb] ADD DEFAULT dbo.UUIDtoSTR(newid()) FOR [ubc_id];

-- Failed (0 ms)
-- [Microsoft][ODBC Driver 17 for SQL Server][SQL Server]Column "dbo" is not allowed in this context, and the user-defined function or aggregate "dbo.UUIDtoSTR" could not be found.

ALTER TABLE GROUP1.[used_bought_item_tb] ADD DEFAULT dbo.UUIDtoSTR(newid()) FOR [ubi_id];

-- Failed (0 ms)
-- [Microsoft][ODBC Driver 17 for SQL Server][SQL Server]Column "dbo" is not allowed in this context, and the user-defined function or aggregate "dbo.UUIDtoSTR" could not be found.

ALTER TABLE GROUP1.[rental_return_audit_tb] ADD DEFAULT dbo.UUIDtoSTR(newid()) FOR [rra_id];

-- Failed (0 ms)
-- [Microsoft][ODBC Driver 17 for SQL Server][SQL Server]Column "dbo" is not allowed in this context, and the user-defined function or aggregate "dbo.UUIDtoSTR" could not be found.

ALTER TABLE GROUP1.[book_volume_import_tb] ADD DEFAULT dbo.UUIDtoSTR(newid()) FOR [bvi_id];

-- Failed (0 ms)
-- [Microsoft][ODBC Driver 17 for SQL Server][SQL Server]Column "dbo" is not allowed in this context, and the user-defined function or aggregate "dbo.UUIDtoSTR" could not be found.

ALTER TABLE GROUP1.[ebook_vendor_tb] ADD DEFAULT dbo.UUIDtoSTR(newid()) FOR [ebv_id];

-- Failed (0 ms)
-- [Microsoft][ODBC Driver 17 for SQL Server][SQL Server]Column "dbo" is not allowed in this context, and the user-defined function or aggregate "dbo.UUIDtoSTR" could not be found.

ALTER TABLE GROUP1.[customer_credit_limit_audit_tb] ADD DEFAULT dbo.UUIDtoSTR(newid()) FOR [ccla_id];

-- Failed (0 ms)
-- [Microsoft][ODBC Driver 17 for SQL Server][SQL Server]Column "dbo" is not allowed in this context, and the user-defined function or aggregate "dbo.UUIDtoSTR" could not be found.

ALTER TABLE GROUP1.[monthly_inventory_by_vendor_tb] ADD DEFAULT dbo.UUIDtoStr(newid()) FOR [miv_id];

-- Failed (0 ms)
-- [Microsoft][ODBC Driver 17 for SQL Server][SQL Server]Column "dbo" is not allowed in this context, and the user-defined function or aggregate "dbo.UUIDtoStr" could not be found.

ALTER TABLE GROUP1.[monthly_inventory_tb] ADD DEFAULT dbo.UUIDtoSTR(newid()) FOR [min_id];

-- Failed (0 ms)
-- [Microsoft][ODBC Driver 17 for SQL Server][SQL Server]Column "dbo" is not allowed in this context, and the user-defined function or aggregate "dbo.UUIDtoSTR" could not be found.

ALTER TABLE GROUP1.[serialized_inventory_tb] ADD DEFAULT dbo.UUIDtoSTR(newid()) FOR [sit_id];

-- Failed (15 ms)
-- [Microsoft][ODBC Driver 17 for SQL Server][SQL Server]Column "dbo" is not allowed in this context, and the user-defined function or aggregate "dbo.UUIDtoSTR" could not be found.

ALTER TABLE GROUP1.[color_set_tb] ADD DEFAULT dbo.UUIDtoSTR(newid()) FOR [cs_id];

-- Failed (0 ms)
-- [Microsoft][ODBC Driver 17 for SQL Server][SQL Server]Column "dbo" is not allowed in this context, and the user-defined function or aggregate "dbo.UUIDtoSTR" could not be found.

ALTER TABLE GROUP1.[size_set_tb] ADD DEFAULT dbo.UUIDtoSTR(newid()) FOR [ss_id];

-- Failed (0 ms)
-- [Microsoft][ODBC Driver 17 for SQL Server][SQL Server]Column "dbo" is not allowed in this context, and the user-defined function or aggregate "dbo.UUIDtoSTR" could not be found.

ALTER TABLE GROUP1.[inventory_uom_pkg_tb] ADD DEFAULT dbo.UUIDtoSTR(newid()) FOR [uom_id];

-- Failed (0 ms)
-- [Microsoft][ODBC Driver 17 for SQL Server][SQL Server]Column "dbo" is not allowed in this context, and the user-defined function or aggregate "dbo.UUIDtoSTR" could not be found.

ALTER TABLE GROUP1.[bookscan_dept_export_tb] ADD DEFAULT dbo.UUIDtoSTR(newid()) FOR [bde_id];

-- Failed (0 ms)
-- [Microsoft][ODBC Driver 17 for SQL Server][SQL Server]Column "dbo" is not allowed in this context, and the user-defined function or aggregate "dbo.UUIDtoSTR" could not be found.

ALTER TABLE GROUP1.[risklessrentalimport_audit_tb] ADD DEFAULT dbo.UUIDtoSTR(newid()) FOR [rri_id];

-- Failed (0 ms)
-- [Microsoft][ODBC Driver 17 for SQL Server][SQL Server]Column "dbo" is not allowed in this context, and the user-defined function or aggregate "dbo.UUIDtoSTR" could not be found.

ALTER TABLE GROUP1.[bindingtype_tb] ADD DEFAULT dbo.UUIDtoSTR(newid()) FOR [bt_id];

-- Failed (0 ms)
-- [Microsoft][ODBC Driver 17 for SQL Server][SQL Server]Column "dbo" is not allowed in this context, and the user-defined function or aggregate "dbo.UUIDtoSTR" could not be found.

ALTER TABLE GROUP1.[standing_order_type_tb] ADD DEFAULT dbo.UUIDtoSTR(newid()) FOR [sto_id];

-- Failed (0 ms)
-- [Microsoft][ODBC Driver 17 for SQL Server][SQL Server]Column "dbo" is not allowed in this context, and the user-defined function or aggregate "dbo.UUIDtoSTR" could not be found.

ALTER TABLE GROUP1.[standing_order_type_item_tb] ADD DEFAULT dbo.UUIDtoSTR(newid()) FOR [sto_itm_id];

-- Failed (0 ms)
-- [Microsoft][ODBC Driver 17 for SQL Server][SQL Server]Column "dbo" is not allowed in this context, and the user-defined function or aggregate "dbo.UUIDtoSTR" could not be found.

ALTER TABLE GROUP1.[standing_order_item_tb] ADD DEFAULT dbo.UUIDtoSTR(newid()) FOR [stoi_id];

-- Failed (0 ms)
-- [Microsoft][ODBC Driver 17 for SQL Server][SQL Server]Column "dbo" is not allowed in this context, and the user-defined function or aggregate "dbo.UUIDtoSTR" could not be found.

ALTER TABLE GROUP1.[standing_order_shipment_tb] ADD DEFAULT dbo.UUIDtoSTR(newid()) FOR [stos_id];

-- Failed (0 ms)
-- [Microsoft][ODBC Driver 17 for SQL Server][SQL Server]Column "dbo" is not allowed in this context, and the user-defined function or aggregate "dbo.UUIDtoSTR" could not be found.

ALTER TABLE GROUP1.[user_list_tb] ADD DEFAULT dbo.UUIDtoSTR(newid()) FOR [ul_id];

-- Failed (0 ms)
-- [Microsoft][ODBC Driver 17 for SQL Server][SQL Server]Column "dbo" is not allowed in this context, and the user-defined function or aggregate "dbo.UUIDtoSTR" could not be found.

ALTER TABLE GROUP1.[user_list_inv_tb] ADD DEFAULT dbo.UUIDtoSTR(newid()) FOR [ul_itm_id];

-- Failed (16 ms)
-- [Microsoft][ODBC Driver 17 for SQL Server][SQL Server]Column "dbo" is not allowed in this context, and the user-defined function or aggregate "dbo.UUIDtoSTR" could not be found.

ALTER TABLE GROUP1.[inv_description_tb] ADD DEFAULT dbo.UUIDtoSTR(newid()) FOR [invd_id];

-- Failed (0 ms)
-- [Microsoft][ODBC Driver 17 for SQL Server][SQL Server]Column "dbo" is not allowed in this context, and the user-defined function or aggregate "dbo.UUIDtoSTR" could not be found.

ALTER TABLE GROUP1.[inv_readernote_tb] ADD DEFAULT dbo.UUIDtoSTR(newid()) FOR [invr_id];

-- Failed (0 ms)
-- [Microsoft][ODBC Driver 17 for SQL Server][SQL Server]Column "dbo" is not allowed in this context, and the user-defined function or aggregate "dbo.UUIDtoSTR" could not be found.

ALTER TABLE GROUP1.[service_heartbeat_tb] ADD DEFAULT dbo.UUIDtoSTR(newid()) FOR [hb_id];

-- Failed (0 ms)
-- [Microsoft][ODBC Driver 17 for SQL Server][SQL Server]Column "dbo" is not allowed in this context, and the user-defined function or aggregate "dbo.UUIDtoSTR" could not be found.

ALTER TABLE GROUP1.[receiving_cost_tb] ADD DEFAULT dbo.UUIDToStr(newid()) FOR [rc_id];

-- Failed (0 ms)
-- [Microsoft][ODBC Driver 17 for SQL Server][SQL Server]Column "dbo" is not allowed in this context, and the user-defined function or aggregate "dbo.UUIDToStr" could not be found.

ALTER TABLE GROUP1.[accounting_audit_header_tb] ADD DEFAULT dbo.UUIDToStr(newid()) FOR [aah_id];

-- Failed (0 ms)
-- [Microsoft][ODBC Driver 17 for SQL Server][SQL Server]Column "dbo" is not allowed in this context, and the user-defined function or aggregate "dbo.UUIDToStr" could not be found.

ALTER TABLE GROUP1.[accounting_audit_item_tb] ADD DEFAULT dbo.UUIDToStr(newid()) FOR [aai_id];

-- Failed (0 ms)
-- [Microsoft][ODBC Driver 17 for SQL Server][SQL Server]Column "dbo" is not allowed in this context, and the user-defined function or aggregate "dbo.UUIDToStr" could not be found.

ALTER TABLE GROUP1.[ebookcoord_deletion_audit_tb] ADD DEFAULT dbo.UUIDToStr(newid()) FOR [ebd_id];

-- Failed (0 ms)
-- [Microsoft][ODBC Driver 17 for SQL Server][SQL Server]Column "dbo" is not allowed in this context, and the user-defined function or aggregate "dbo.UUIDToStr" could not be found.

ALTER TABLE GROUP1.[mailord_gc_tb] ADD DEFAULT dbo.UUIDToStr(newid()) FOR [mogc_id];

-- Failed (0 ms)
-- [Microsoft][ODBC Driver 17 for SQL Server][SQL Server]Column "dbo" is not allowed in this context, and the user-defined function or aggregate "dbo.UUIDToStr" could not be found.

ALTER TABLE GROUP1.[inventory_tbt_tb] ADD DEFAULT dbo.UUIDtoSTR(newid()) FOR [itbt_id];

-- Failed (0 ms)
-- [Microsoft][ODBC Driver 17 for SQL Server][SQL Server]Column "dbo" is not allowed in this context, and the user-defined function or aggregate "dbo.UUIDtoSTR" could not be found.

ALTER TABLE GROUP1.[square_tb] ADD DEFAULT dbo.UUIDToStr(newid()) FOR [sq_id];

-- Failed (0 ms)
-- [Microsoft][ODBC Driver 17 for SQL Server][SQL Server]Column "dbo" is not allowed in this context, and the user-defined function or aggregate "dbo.UUIDToStr" could not be found.

ALTER TABLE GROUP1.[customer_alt_id] ADD DEFAULT dbo.UUIDtoSTR(newid()) FOR [cu_alt_id_id];

-- Failed (0 ms)
-- [Microsoft][ODBC Driver 17 for SQL Server][SQL Server]Column "dbo" is not allowed in this context, and the user-defined function or aggregate "dbo.UUIDtoSTR" could not be found.

ALTER TABLE GROUP1.[category_to_bisac_tb] ADD DEFAULT dbo.UUIDtoSTR(newid()) FOR [ctb_id];

-- Failed (15 ms)
-- [Microsoft][ODBC Driver 17 for SQL Server][SQL Server]Column "dbo" is not allowed in this context, and the user-defined function or aggregate "dbo.UUIDtoSTR" could not be found.

ALTER TABLE GROUP1.[qb_account_tb] ADD DEFAULT dbo.UUIDToStr(newid()) FOR [qba_id];

-- Failed (0 ms)
-- [Microsoft][ODBC Driver 17 for SQL Server][SQL Server]Column "dbo" is not allowed in this context, and the user-defined function or aggregate "dbo.UUIDToStr" could not be found.

ALTER TABLE GROUP1.[customer_qty_restrict_defaults_tb] ADD DEFAULT dbo.UUIDToStr(newid()) FOR [cqrd_id];

-- Failed (0 ms)
-- [Microsoft][ODBC Driver 17 for SQL Server][SQL Server]Column "dbo" is not allowed in this context, and the user-defined function or aggregate "dbo.UUIDToStr" could not be found.

ALTER TABLE GROUP1.[square_tax_ids] ADD DEFAULT dbo.UUIDToStr(newid()) FOR [sqtx_id];

-- Failed (0 ms)
-- [Microsoft][ODBC Driver 17 for SQL Server][SQL Server]Column "dbo" is not allowed in this context, and the user-defined function or aggregate "dbo.UUIDToStr" could not be found.

ALTER TABLE GROUP1.[square_cat_ids] ADD DEFAULT dbo.UUIDToStr(newid()) FOR [sqctg_id];

-- Failed (16 ms)
-- [Microsoft][ODBC Driver 17 for SQL Server][SQL Server]Column "dbo" is not allowed in this context, and the user-defined function or aggregate "dbo.UUIDToStr" could not be found.

ALTER TABLE GROUP1.[square_in_ids] ADD DEFAULT dbo.UUIDToStr(newid()) FOR [sqin_id];

-- Failed (16 ms)
-- [Microsoft][ODBC Driver 17 for SQL Server][SQL Server]Column "dbo" is not allowed in this context, and the user-defined function or aggregate "dbo.UUIDToStr" could not be found.

ALTER TABLE GROUP1.[qb_audit_tb] ADD DEFAULT dbo.UUIDToStr(newid()) FOR [qba_id];

-- Failed (0 ms)
-- [Microsoft][ODBC Driver 17 for SQL Server][SQL Server]Column "dbo" is not allowed in this context, and the user-defined function or aggregate "dbo.UUIDToStr" could not be found.

ALTER TABLE GROUP1.[event_header_tb] ADD DEFAULT dbo.UUIDtoSTR(newid()) FOR [event_id];

-- Failed (0 ms)
-- [Microsoft][ODBC Driver 17 for SQL Server][SQL Server]Column "dbo" is not allowed in this context, and the user-defined function or aggregate "dbo.UUIDtoSTR" could not be found.

ALTER TABLE GROUP1.[event_presenters_tb] ADD DEFAULT dbo.UUIDtoSTR(newid()) FOR [evnp_id];

-- Failed (0 ms)
-- [Microsoft][ODBC Driver 17 for SQL Server][SQL Server]Column "dbo" is not allowed in this context, and the user-defined function or aggregate "dbo.UUIDtoSTR" could not be found.

ALTER TABLE GROUP1.[event_type_tb] ADD DEFAULT dbo.UUIDtoSTR(newid()) FOR [evnt_id];

-- Failed (0 ms)
-- [Microsoft][ODBC Driver 17 for SQL Server][SQL Server]Column "dbo" is not allowed in this context, and the user-defined function or aggregate "dbo.UUIDtoSTR" could not be found.

ALTER TABLE GROUP1.[event_tickets_tb] ADD DEFAULT dbo.UUIDtoSTR(newid()) FOR [evnx_id];

-- Failed (0 ms)
-- [Microsoft][ODBC Driver 17 for SQL Server][SQL Server]Column "dbo" is not allowed in this context, and the user-defined function or aggregate "dbo.UUIDtoSTR" could not be found.

ALTER TABLE GROUP1.[event_items_tb] ADD DEFAULT dbo.UUIDtoSTR(newid()) FOR [evni_id];

-- Failed (0 ms)
-- [Microsoft][ODBC Driver 17 for SQL Server][SQL Server]Column "dbo" is not allowed in this context, and the user-defined function or aggregate "dbo.UUIDtoSTR" could not be found.

CREATE UNIQUE INDEX [pbcatt_x] ON GROUP1.[pbcattbl] ([pbt_tnam], [pbt_ownr]);

-- Failed (0 ms)
-- [Microsoft][ODBC Driver 17 for SQL Server][SQL Server]The operation failed because an index or statistics with name 'pbcatt_x' already exists on table 'GROUP1.pbcattbl'.

CREATE UNIQUE INDEX [pbcatc_x] ON GROUP1.[pbcatcol] ([pbc_tnam], [pbc_ownr], [pbc_cnam]);

-- Failed (0 ms)
-- [Microsoft][ODBC Driver 17 for SQL Server][SQL Server]The operation failed because an index or statistics with name 'pbcatc_x' already exists on table 'GROUP1.pbcatcol'.

CREATE UNIQUE INDEX [pbcatf_x] ON GROUP1.[pbcatfmt] ([pbf_name]);

-- Failed (0 ms)
-- [Microsoft][ODBC Driver 17 for SQL Server][SQL Server]The operation failed because an index or statistics with name 'pbcatf_x' already exists on table 'GROUP1.pbcatfmt'.

CREATE UNIQUE INDEX [pbcatv_x] ON GROUP1.[pbcatvld] ([pbv_name]);

-- Failed (0 ms)
-- [Microsoft][ODBC Driver 17 for SQL Server][SQL Server]The operation failed because an index or statistics with name 'pbcatv_x' already exists on table 'GROUP1.pbcatvld'.

CREATE UNIQUE INDEX [pbcate_x] ON GROUP1.[pbcatedt] ([pbe_name], [pbe_seqn]);

-- Failed (0 ms)
-- [Microsoft][ODBC Driver 17 for SQL Server][SQL Server]The operation failed because an index or statistics with name 'pbcate_x' already exists on table 'GROUP1.pbcatedt'.

CREATE UNIQUE INDEX [idx_fa_interface_code] ON GROUP1.[termyear_tb] ([term_fa_interface_code]);

-- Failed (0 ms)
-- [Microsoft][ODBC Driver 17 for SQL Server][SQL Server]The CREATE UNIQUE INDEX statement terminated because a duplicate key was found for the object name 'GROUP1.termyear_tb' and the index name 'idx_fa_interface_code'. The duplicate key value is (<NULL>).

CREATE INDEX [ix_cnt_diffweeks] ON GROUP1.[weeksales_post_tb] ();

-- Failed (0 ms)
-- [Microsoft][ODBC Driver 17 for SQL Server][SQL Server]Incorrect syntax near ')'.

ALTER TABLE GROUP1.[alternate_sku_tb] ADD DEFAULT dbo.UUIDtoSTR(newid()) FOR [as_id];

-- Failed (0 ms)
-- [Microsoft][ODBC Driver 17 for SQL Server][SQL Server]Column "dbo" is not allowed in this context, and the user-defined function or aggregate "dbo.UUIDtoSTR" could not be found.

ALTER TABLE GROUP1.[stock_trans_item_tb] ADD DEFAULT dbo.UUIDtoSTR(newid()) FOR [ti_id];

-- Failed (0 ms)
-- [Microsoft][ODBC Driver 17 for SQL Server][SQL Server]Column "dbo" is not allowed in this context, and the user-defined function or aggregate "dbo.UUIDtoSTR" could not be found.

ALTER TABLE GROUP1.[rental_tb] ADD DEFAULT dbo.UUIDtoSTR(newid()) FOR [r_id];

-- Failed (0 ms)
-- [Microsoft][ODBC Driver 17 for SQL Server][SQL Server]Column "dbo" is not allowed in this context, and the user-defined function or aggregate "dbo.UUIDtoSTR" could not be found.