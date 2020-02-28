TYPE=TRIGGERS
triggers='CREATE DEFINER=`root`@`%` TRIGGER dec_vendor BEFORE INSERT ON transactions\nFOR EACH ROW\nBEGIN\nDECLARE nr INTEGER;\nSELECT nr_items INTO nr FROM vendors WHERE id=NEW.vendorid;\nIF nr = 1 THEN\n    DELETE FROM vendors WHERE id=NEW.vendorid;\nELSE\n    UPDATE vendors SET nr_items=nr-1 WHERE id=NEW.vendorid;\nEND IF;\nEND'
sql_modes=1436549152
definers='root@%'
client_cs_names='utf8'
connection_cl_names='utf8_general_ci'
db_cl_names='latin1_swedish_ci'
created=157884995311
