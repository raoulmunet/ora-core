const META={"ora-core":["ora-core","Inspect read/write SQL structure with the shared analyzer."],"ora-impact":["SQL Impact Analyzer","Find read/write dependencies."],"ora-plan":["Execution Plan Explainer","Explain common DBMS_XPLAN operations."],"ora-lineage":["SQL Lineage Lite","Trace simple source-to-target lineage."],"ora-lint":["SQL / PL/SQL Linter","Find common anti-pattern candidates."],"ora-doc":["DDL Documentation Generator","Generate Markdown documentation from CREATE TABLE DDL."],"ora-bind":["Bind Variable Converter","Replace common literals with bind variables."],"ora-exception-flow":["PL/SQL Exception Flow","Inspect handlers and RAISE behavior."],"ora-join-viz":["SQL Join Visualizer","Show ANSI JOIN relationships."],"ora-sql-diff":["Structural SQL Diff","Compare supported structural SQL changes."],"ora-errors":["Oracle Error Decoder","Explain common ORA errors offline."],"ora-etl-log":["ETL Log Analyzer","Summarize simple timestamped batch logs."],"ora-data-quality":["Data Quality Rules","Generate baseline checks from DDL."],"ora-csv-loader":["CSV to Oracle Loader","Infer starter Oracle DDL from CSV."],"ora-migration-check":["Migration Compatibility Check","Flag Oracle migration hotspots."],"ora-sql-complexity":["SQL Complexity Metrics","Measure structural SQL features."],"ora-call-graph":["PL/SQL Call Graph","Find qualified routine calls."],"ora-dead-code":["PL/SQL Dead Code Finder","Find conservative dead-code candidates."],"ora-schema-explorer":["Schema Explorer","Summarize tables and dependencies."]};
const SAMPLES={"ora-core":[["Simple","SELECT customer_id, customer_name FROM customers;"],["Intermediate","SELECT c.customer_id, o.order_id FROM customers c JOIN orders o ON o.customer_id=c.customer_id WHERE o.status='OPEN';"],["Complex","MERGE INTO dwh.customer_dim d USING (SELECT c.customer_id,c.customer_name FROM crm.customers c JOIN crm.customer_status s ON s.customer_id=c.customer_id WHERE s.active_flag='Y') x ON (d.customer_id=x.customer_id) WHEN MATCHED THEN UPDATE SET d.customer_name=x.customer_name WHEN NOT MATCHED THEN INSERT (customer_id,customer_name) VALUES (x.customer_id,x.customer_name);"]],"ora-impact":[["Simple","INSERT INTO archive_customers SELECT * FROM customers;"],["Intermediate","INSERT INTO dwh.customer_dim (customer_id,customer_name) SELECT c.customer_id,c.customer_name FROM crm.customers c JOIN crm.customer_status s ON s.customer_id=c.customer_id WHERE s.active_flag='Y';"],["Complex","MERGE INTO dwh.account_fact f USING (SELECT a.account_id,t.txn_id,t.amount FROM core.accounts a JOIN core.transactions t ON t.account_id=a.account_id JOIN ref.currency c ON c.currency_id=t.currency_id WHERE t.booking_date>=DATE '2026-01-01') s ON (f.txn_id=s.txn_id) WHEN MATCHED THEN UPDATE SET f.amount=s.amount WHEN NOT MATCHED THEN INSERT (account_id,txn_id,amount) VALUES (s.account_id,s.txn_id,s.amount);"]],"ora-plan":[["Simple","| Id | Operation          | Name      | Rows | Cost |\n|  0 | SELECT STATEMENT   |           |   10 |   12 |\n|* 1 | TABLE ACCESS FULL  | CUSTOMERS |   10 |   12 |"],["Intermediate","| Id | Operation                    | Name          | Rows | Cost |\n|  0 | SELECT STATEMENT             |               |  100 |  120 |\n|  1 | NESTED LOOPS                 |               |  100 |  120 |\n|  2 | TABLE ACCESS FULL            | CUSTOMERS     | 1000 |   80 |\n|* 3 | INDEX RANGE SCAN             | IDX_ORDERS_C  |    1 |    2 |"],["Complex","| Id | Operation                    | Name           | Rows  | Cost |\n|  0 | SELECT STATEMENT             |                | 50000 | 9500 |\n|  1 | SORT ORDER BY                |                | 50000 | 9500 |\n|* 2 | HASH JOIN                    |                | 50000 | 8100 |\n|  3 | TABLE ACCESS FULL            | TRANSACTIONS   | 900000| 6200 |\n|  4 | TABLE ACCESS FULL            | ACCOUNTS       | 100000| 1200 |"]],"ora-lineage":[["Simple","INSERT INTO dwh.customer_dim (customer_id) SELECT customer_id FROM crm.customers;"],["Intermediate","INSERT INTO dwh.customer_dim (customer_id,customer_name) SELECT c.customer_id,c.customer_name FROM crm.customers c;"],["Complex","INSERT INTO dwh.monthly_sales (customer_id,month_key,total_amount) SELECT c.customer_id,TRUNC(o.order_date,'MM'),SUM(o.amount) FROM crm.customers c JOIN sales.orders o ON o.customer_id=c.customer_id WHERE o.status='PAID' GROUP BY c.customer_id,TRUNC(o.order_date,'MM');"]],"ora-lint":[["Simple","SELECT * FROM customers;"],["Intermediate","SELECT COUNT(*) FROM orders WHERE UPPER(status)='OPEN' AND customer_id NOT IN (SELECT customer_id FROM blacklist);"],["Complex","BEGIN FOR r IN (SELECT * FROM orders) LOOP UPDATE order_audit SET flag='Y' WHERE order_id=r.order_id; COMMIT; END LOOP; EXCEPTION WHEN OTHERS THEN NULL; END;"]],"ora-doc":[["Simple","CREATE TABLE customer (customer_id NUMBER NOT NULL, customer_name VARCHAR2(100));"],["Intermediate","CREATE TABLE orders (order_id NUMBER NOT NULL, customer_id NUMBER NOT NULL, order_date DATE, amount NUMBER(12,2), status VARCHAR2(20));"],["Complex","CREATE TABLE transaction_fact (txn_id NUMBER NOT NULL, account_id NUMBER NOT NULL, booking_ts TIMESTAMP, amount NUMBER(18,2), currency_code CHAR(3), channel VARCHAR2(30), status VARCHAR2(20), source_system VARCHAR2(30));"]],"ora-bind":[["Simple","SELECT * FROM customers WHERE customer_id=123;"],["Intermediate","SELECT * FROM customers WHERE customer_id=123 AND status='ACTIVE' AND created_date>=DATE '2026-01-01';"],["Complex","SELECT o.order_id,c.customer_name FROM orders o JOIN customers c ON c.customer_id=o.customer_id WHERE o.status='PAID' AND o.amount>2500.50 AND o.order_date BETWEEN DATE '2026-01-01' AND DATE '2026-12-31' AND c.country_code='RO';"]],"ora-exception-flow":[["Simple","BEGIN do_work; EXCEPTION WHEN OTHERS THEN RAISE; END;"],["Intermediate","BEGIN SELECT customer_name INTO v_name FROM customers WHERE customer_id=p_id; EXCEPTION WHEN NO_DATA_FOUND THEN log_error('missing'); RAISE; WHEN OTHERS THEN log_error('other'); END;"],["Complex","BEGIN load_batch; EXCEPTION WHEN DUP_VAL_ON_INDEX THEN log_warn('duplicate'); WHEN VALUE_ERROR THEN log_error('value'); RAISE; WHEN OTHERS THEN rollback_batch; log_error(SQLERRM); RAISE; END;"]],"ora-join-viz":[["Simple","SELECT * FROM customers c JOIN orders o ON o.customer_id=c.customer_id;"],["Intermediate","SELECT c.customer_id,o.order_id,i.product_id FROM customers c JOIN orders o ON o.customer_id=c.customer_id LEFT JOIN order_items i ON i.order_id=o.order_id;"],["Complex","SELECT c.customer_id,o.order_id,p.product_name,s.shipment_id FROM customers c INNER JOIN orders o ON o.customer_id=c.customer_id LEFT JOIN order_items i ON i.order_id=o.order_id LEFT JOIN products p ON p.product_id=i.product_id FULL JOIN shipments s ON s.order_id=o.order_id WHERE o.status='PAID';"]],"ora-sql-diff":[["Simple","SELECT customer_id FROM customers;","SELECT customer_id,customer_name FROM customers;"],["Intermediate","SELECT c.customer_id,o.order_id FROM customers c JOIN orders o ON o.customer_id=c.customer_id WHERE o.status='OPEN';","SELECT c.customer_id,o.order_id,o.amount FROM customers c LEFT JOIN orders o ON o.customer_id=c.customer_id WHERE o.status IN ('OPEN','PENDING');"],["Complex","SELECT c.customer_id,SUM(o.amount) total FROM customers c JOIN orders o ON o.customer_id=c.customer_id WHERE o.status='PAID' GROUP BY c.customer_id;","SELECT c.customer_id,SUM(o.amount) total,COUNT(*) cnt FROM customers c JOIN orders o ON o.customer_id=c.customer_id JOIN payments p ON p.order_id=o.order_id WHERE o.status IN ('PAID','SETTLED') GROUP BY c.customer_id HAVING SUM(o.amount)>1000;"]],"ora-errors":[["Simple","ORA-01722"],["Intermediate","ORA-02291"],["Complex","ORA-03113"]],"ora-etl-log":[["Simple","2026-09-26T08:00:00 START LOAD_CUSTOMERS\n2026-09-26T08:01:10 END LOAD_CUSTOMERS"],["Intermediate","2026-09-26T08:00:00 START BATCH nightly_dwh\n2026-09-26T08:00:02 START LOAD_CUSTOMERS\n2026-09-26T08:03:15 END LOAD_CUSTOMERS\n2026-09-26T08:03:16 START LOAD_ORDERS\n2026-09-26T08:10:04 END LOAD_ORDERS\n2026-09-26T08:10:05 END BATCH nightly_dwh"],["Complex","2026-09-26T08:00:00 START BATCH nightly_dwh\n2026-09-26T08:00:02 START LOAD_CUSTOMERS\n2026-09-26T08:03:15 END LOAD_CUSTOMERS\n2026-09-26T08:03:16 START LOAD_ORDERS\n2026-09-26T08:10:04 ERROR LOAD_ORDERS ORA-01722 invalid number\n2026-09-26T08:10:05 START RECONCILE\n2026-09-26T08:14:30 ERROR RECONCILE ORA-02291 parent key not found\n2026-09-26T08:14:31 END BATCH nightly_dwh"]],"ora-data-quality":[["Simple","CREATE TABLE customer (customer_id NUMBER NOT NULL);"],["Intermediate","CREATE TABLE customer (customer_id NUMBER NOT NULL, email VARCHAR2(200), country_code CHAR(2));"],["Complex","CREATE TABLE account (account_id NUMBER NOT NULL, customer_id NUMBER NOT NULL, iban VARCHAR2(34), email VARCHAR2(200), country_code CHAR(2), opened_date DATE, closed_date DATE, status VARCHAR2(20));"]],"ora-csv-loader":[["Simple","id,name\n1,Ana\n2,Mihai"],["Intermediate","customer_id,name,created_date,balance\n1,Ana,2026-01-01,120.50\n2,Mihai,2026-01-02,0"],["Complex","txn_id,account_id,booking_date,amount,currency,status,description\n1001,10,2026-09-20,1200.50,EUR,BOOKED,Transfer\n1002,11,2026-09-21,-50.25,RON,REVERSED,Fee reversal\n1003,10,2026-09-22,99999.99,USD,BOOKED,Large payment"]],"ora-migration-check":[["Simple","SELECT NVL(customer_name,'UNKNOWN') FROM customers;"],["Intermediate","SELECT DECODE(status,'A','ACTIVE','I','INACTIVE','OTHER'),SYSDATE FROM customers WHERE ROWNUM<=100;"],["Complex","SELECT LEVEL,employee_id,manager_id,NVL(salary,0) FROM employees START WITH manager_id IS NULL CONNECT BY PRIOR employee_id=manager_id AND ROWNUM<=1000;"]],"ora-sql-complexity":[["Simple","SELECT customer_id FROM customers;"],["Intermediate","SELECT c.customer_id,COUNT(*) cnt,SUM(o.amount) total FROM customers c JOIN orders o ON o.customer_id=c.customer_id GROUP BY c.customer_id;"],["Complex","WITH totals AS (SELECT customer_id,SUM(amount) total_amount,COUNT(*) cnt FROM orders GROUP BY customer_id) SELECT c.customer_id,CASE WHEN t.total_amount>10000 THEN 'HIGH' ELSE 'STANDARD' END segment,ROW_NUMBER() OVER (ORDER BY t.total_amount DESC) rn FROM customers c JOIN totals t ON t.customer_id=c.customer_id WHERE EXISTS (SELECT 1 FROM blacklist b WHERE b.customer_id=c.customer_id);"]],"ora-call-graph":[["Simple","CREATE OR REPLACE PROCEDURE p IS BEGIN pkg_log.write_log('start'); END;"],["Intermediate","CREATE OR REPLACE PACKAGE BODY pkg_batch AS PROCEDURE run_batch IS BEGIN pkg_customer.load_customers(); pkg_order.load_orders(); pkg_log.write_log('done'); END; END pkg_batch;"],["Complex","CREATE OR REPLACE PACKAGE BODY pkg_etl AS PROCEDURE extract IS BEGIN pkg_source.read_customers(); pkg_source.read_orders(); END; PROCEDURE transform IS BEGIN pkg_rules.apply_customer_rules(); pkg_rules.apply_order_rules(); END; PROCEDURE load IS BEGIN pkg_target.load_dimensions(); pkg_target.load_facts(); pkg_audit.finish_batch(); END; END pkg_etl;"]],"ora-dead-code":[["Simple","CREATE OR REPLACE PROCEDURE p AS v_unused NUMBER; BEGIN NULL; END;"],["Intermediate","CREATE OR REPLACE PROCEDURE p AS v_used NUMBER; v_unused VARCHAR2(20); BEGIN v_used:=1; DBMS_OUTPUT.PUT_LINE(v_used); END;"],["Complex","CREATE OR REPLACE PROCEDURE p AS v_used NUMBER; v_unused NUMBER; BEGIN v_used:=1; IF v_used=1 THEN RETURN; DBMS_OUTPUT.PUT_LINE('never'); END IF; RAISE; DBMS_OUTPUT.PUT_LINE('also never'); END;"]],"ora-schema-explorer":[["Simple","CREATE TABLE customers (customer_id NUMBER NOT NULL, customer_name VARCHAR2(200));"],["Intermediate","CREATE TABLE customers (customer_id NUMBER NOT NULL, customer_name VARCHAR2(200));\nCREATE TABLE orders (order_id NUMBER NOT NULL, customer_id NUMBER NOT NULL, amount NUMBER(12,2));\nINSERT INTO dwh.customer_dim SELECT * FROM customers;"],["Complex","CREATE TABLE customers (customer_id NUMBER NOT NULL, customer_name VARCHAR2(200), country_code CHAR(2));\nCREATE TABLE accounts (account_id NUMBER NOT NULL, customer_id NUMBER NOT NULL, iban VARCHAR2(34));\nCREATE TABLE transactions (txn_id NUMBER NOT NULL, account_id NUMBER NOT NULL, amount NUMBER(18,2));\nINSERT INTO dwh.customer_dim SELECT customer_id,customer_name,country_code FROM customers;\nINSERT INTO dwh.account_fact SELECT a.account_id,a.customer_id,SUM(t.amount) FROM accounts a JOIN transactions t ON t.account_id=a.account_id GROUP BY a.account_id,a.customer_id;"]]};

const $=s=>document.querySelector(s);
const uniq=a=>[...new Set(a)];
const collapse=s=>String(s||"").trim().replace(/\s+/g," ");
const norm=s=>String(s).split(".").map(p=>/^".*"$/.test(p)?p:p.toUpperCase()).join(".");
function mask(sql){return sql.replace(/\/\*[\s\S]*?\*\//g," ").replace(/--[^\n]*/g," ").replace(/'(?:''|[^'])*'/g," ")}
function analyze(sql){
  const reads=[],writes=[],ops=[];
  const statements=sql.split(";").map(x=>x.trim()).filter(Boolean);
  for(const st of statements){
    const t=mask(st),u=t.toUpperCase();
    ops.push(["SELECT","INSERT","UPDATE","DELETE","MERGE","CREATE","ALTER","DROP","TRUNCATE"].find(x=>u.startsWith(x))||"UNKNOWN");
    for(const re of [/\bFROM\s+([\w.$#"]+)/ig,/\bJOIN\s+([\w.$#"]+)/ig,/\bUSING\s+([\w.$#"]+)/ig]){
      let m; while((m=re.exec(t))) reads.push(norm(m[1]));
    }
    for(const re of [/\bINSERT\s+INTO\s+([\w.$#"]+)/ig,/\bUPDATE\s+([\w.$#"]+)/ig,/\bDELETE\s+FROM\s+([\w.$#"]+)/ig,/\bMERGE\s+INTO\s+([\w.$#"]+)/ig,/\bTRUNCATE\s+TABLE\s+([\w.$#"]+)/ig]){
      let m; while((m=re.exec(t))) writes.push(norm(m[1]));
    }
  }
  return {statement_count:statements.length,operations:ops,read_objects:uniq(reads),write_objects:uniq(writes)};
}
function parseTables(sql){
  const out=[]; let m;
  const re=/CREATE\s+TABLE\s+([\w.$#]+)\s*\(([\s\S]*?)\)\s*;/ig;
  while((m=re.exec(sql))){
    const cols=[];
    for(const raw of m[2].split(",")){
      const p=raw.trim();
      if(/^(CONSTRAINT|PRIMARY|FOREIGN|UNIQUE|CHECK)\b/i.test(p)) continue;
      const c=p.match(/^([\w$#]+)\s+([A-Za-z0-9_]+(?:\s*\([^)]*\))?)(.*)$/is);
      if(c) cols.push({name:c[1].toUpperCase(),datatype:c[2].replace(/\s+/g,"").toUpperCase(),nullable:!/\bNOT\s+NULL\b/i.test(c[3])});
    }
    out.push({name:m[1].toUpperCase(),columns:cols});
  }
  return out;
}
const ERRORS={
 "ORA-01722":["invalid number","A character-to-number conversion failed."],
 "ORA-02291":["parent key not found","A child row references a parent key that does not exist."],
 "ORA-03113":["end-of-file on communication channel","The Oracle client/server communication channel ended unexpectedly."],
 "ORA-12541":["no listener","The client could not reach an Oracle listener."],
 "ORA-12514":["listener does not know service","The listener is reachable but does not advertise the requested service."],
 "ORA-01555":["snapshot too old","Oracle could not reconstruct the required read-consistent version from undo."],
 "ORA-00942":["table or view does not exist","The referenced object is unavailable under current name resolution or privileges."]
};
function processTool(tool,a,b){
  const x=analyze(a),out=[];
  if(tool==="ora-core"||tool==="ora-impact") return "Statements : "+x.statement_count+"\nOperations : "+x.operations.join(", ")+"\nReads      : "+(x.read_objects.join(", ")||"-")+"\nWrites     : "+(x.write_objects.join(", ")||"-");
  if(tool==="ora-plan"){
    for(const l of a.split(/\n/)){
      if(!l.includes("|")) continue;
      const c=l.replace(/^\||\|$/g,"").split("|").map(v=>v.trim());
      if(!/^\*?\s*\d+$/.test(c[0]||"")) continue;
      const op=c[1]||"",name=c[2]||"";
      let meaning="Oracle execution-plan operation.",review="Interpret together with predicates, estimates and runtime statistics.";
      if(/TABLE ACCESS FULL/i.test(op)){meaning="Oracle scans table blocks rather than using an index access path.";review="Review when the table is large and the predicate is selective."}
      else if(/INDEX RANGE SCAN/i.test(op)){meaning="Oracle scans a bounded range of index entries.";review="Check selectivity and subsequent table access cost."}
      else if(/NESTED LOOPS/i.test(op)){meaning="Oracle probes the inner row source for rows from the outer source.";review="Review when the outer row count is large."}
      else if(/HASH JOIN/i.test(op)){meaning="Oracle hashes one row source and probes it with another.";review="Review estimates and memory, not the join type alone."}
      else if(/SORT/i.test(op)){meaning="Oracle performs a sort operation.";review="Check row volume and memory/TEMP pressure."}
      out.push(c[0]+". "+op+(name?" on "+name:"")+"\n   Meaning: "+meaning+"\n   Review: "+review);
    }
    return out.join("\n\n")||"No plan rows detected.";
  }
  if(tool==="ora-lineage") return x.read_objects.flatMap(r=>x.write_objects.map(w=>r+" -> "+w)).join("\n")||"No lineage detected.";
  if(tool==="ora-lint"){
    const rules=[[/\bSELECT\s+\*/ig,"SELECT * couples code to table shape."],[/\bWHEN\s+OTHERS\s+THEN\s+NULL\b/ig,"Exception is swallowed silently."],[/\bNOT\s+IN\s*\(/ig,"Review NULL semantics for NOT IN."],[/\bCOUNT\s*\(\s*\*\s*\)\s*(?:>|=)\s*0/ig,"Consider EXISTS for pure existence checks."],[/\bCOMMIT\b/ig,"Review transaction boundaries, especially inside loops."]];
    for(const [re,msg] of rules){let m;while((m=re.exec(a)))out.push("line "+a.slice(0,m.index).split("\n").length+": "+msg)}
    return out.join("\n")||"No configured warnings found.";
  }
  if(tool==="ora-doc"){
    const ts=parseTables(a);
    return ts.map(t=>"## "+t.name+"\n\n| Column | Type | Nullable |\n|---|---|---|\n"+t.columns.map(c=>"| "+c.name+" | "+c.datatype+" | "+(c.nullable?"Yes":"No")+" |").join("\n")).join("\n\n")||"No CREATE TABLE statements detected.";
  }
  if(tool==="ora-bind"){
    let n=0; const binds=[];
    const converted=a.replace(/\bDATE\s+'(?:''|[^'])*'|'(?:''|[^'])*'|(?<![\w$#.:])[-+]?\d+(?:\.\d+)?(?![\w$#])/g,m=>{const k=":b"+(++n);binds.push(k+" = "+m);return k});
    return converted+"\n\nBinds:\n"+(binds.join("\n")||"-");
  }
  if(tool==="ora-exception-flow"){
    const ex=(a.match(/\bEXCEPTION\b([\s\S]*?)(?:\bEND\b\s*;|$)/i)||[])[1];
    if(!ex)return"No EXCEPTION section detected.";
    const ms=[...ex.matchAll(/\bWHEN\s+(.+?)\s+THEN\b/ig)];
    return ms.map((m,i)=>{const body=ex.slice(m.index+m[0].length,ms[i+1]?.index??ex.length);return collapse(m[1]).toUpperCase()+" -> handler -> "+(/\bRAISE\s*;/i.test(body)?"RAISE":"handled")}).join("\n");
  }
  if(tool==="ora-join-viz"){
    const base=a.match(/\bFROM\s+([\w.$#]+)/i); if(!base)return"No FROM clause detected.";
    let left=base[1].toUpperCase(),m; const re=/\b(?:(INNER|LEFT|RIGHT|FULL|CROSS)\s+)?JOIN\s+([\w.$#]+)(?:\s+[A-Za-z][\w$#]*)?\s*(?:ON\s+([\s\S]*?))?(?=\b(?:INNER|LEFT|RIGHT|FULL|CROSS)?\s*JOIN\b|\bWHERE\b|\bGROUP\b|\bORDER\b|$)/ig;
    while((m=re.exec(a))){const right=m[2].toUpperCase();out.push(left+" --["+(m[1]||"INNER").toUpperCase()+(m[3]?": "+collapse(m[3]):"")+"]--> "+right);left=right}
    return out.join("\n")||"No ANSI JOINs detected.";
  }
  if(tool==="ora-sql-diff"){
    const y=analyze(b);
    for(const v of y.read_objects.concat(y.write_objects).filter(v=>!x.read_objects.concat(x.write_objects).includes(v)))out.push("OBJECT_ADDED: "+v);
    for(const v of x.read_objects.concat(x.write_objects).filter(v=>!y.read_objects.concat(y.write_objects).includes(v)))out.push("OBJECT_REMOVED: "+v);
    const wa=collapse((a.match(/\bWHERE\b([\s\S]*?)(?=\bGROUP\b|\bHAVING\b|\bORDER\b|$)/i)||[])[1]).toUpperCase();
    const wb=collapse((b.match(/\bWHERE\b([\s\S]*?)(?=\bGROUP\b|\bHAVING\b|\bORDER\b|$)/i)||[])[1]).toUpperCase();
    if(wa!==wb)out.push("WHERE_CHANGED");
    return out.join("\n")||"No supported structural changes detected.";
  }
  if(tool==="ora-errors"){
    const m=a.toUpperCase().match(/(?:ORA[- ]?)?(\d{1,5})/);if(!m)return"Enter an ORA error code.";
    const k="ORA-"+String(parseInt(m[1],10)).padStart(5,"0"),v=ERRORS[k];
    return v?k+" — "+v[0]+"\n\n"+v[1]:k+": not in browser catalog.";
  }
  if(tool==="ora-etl-log"){
    const lines=a.split(/\n/).filter(Boolean),errs=uniq(a.match(/ORA-\d{5}/ig)||[]);
    const starts={},dur=[];
    for(const line of lines){const m=line.match(/^(\S+)\s+(START|END|ERROR)\s+(\S+)/i);if(!m)continue;const t=new Date(m[1]),ev=m[2].toUpperCase(),name=m[3];if(ev==="START")starts[name]=t;else if((ev==="END"||ev==="ERROR")&&starts[name]){dur.push([name,(t-starts[name])/1000,ev]);delete starts[name]}}
    dur.sort((a,b)=>b[1]-a[1]);
    return "Lines: "+lines.length+"\nOracle errors: "+(errs.join(", ")||"-")+"\nLongest stage: "+(dur[0]?dur[0][0]+" ("+dur[0][1]+"s, "+dur[0][2]+")":"-");
  }
  if(tool==="ora-data-quality"){
    for(const t of parseTables(a))for(const c of t.columns){
      if(!c.nullable)out.push("SELECT COUNT(*) AS violations FROM "+t.name+" WHERE "+c.name+" IS NULL;");
      if(/EMAIL/i.test(c.name))out.push("SELECT COUNT(*) AS violations FROM "+t.name+" WHERE "+c.name+" IS NOT NULL AND ("+c.name+" NOT LIKE '%@%' OR "+c.name+" LIKE '% %');");
      if(/COUNTRY_CODE/i.test(c.name))out.push("SELECT COUNT(*) AS violations FROM "+t.name+" WHERE "+c.name+" IS NOT NULL AND LENGTH(TRIM("+c.name+"))<>2;");
    }
    return out.join("\n\n")||"No baseline rules generated.";
  }
  if(tool==="ora-csv-loader"){
    const rows=a.trim().split(/\r?\n/).map(r=>r.split(","));if(rows.length<2)return"Provide CSV with a header and data.";
    const table=($("#tableName").value||"STG_DATA").toUpperCase();
    const cols=rows[0].map((n,i)=>{const vals=rows.slice(1).map(r=>(r[i]||"").trim()).filter(Boolean);let dt="VARCHAR2("+Math.min(Math.max(Math.max(...vals.map(v=>v.length),1)*2,32),4000)+")";if(vals.length&&vals.every(v=>!isNaN(Number(v))))dt="NUMBER";else if(vals.length&&vals.every(v=>/^\d{4}-\d{2}-\d{2}$/.test(v)))dt="DATE";return n.trim().replace(/\W+/g,"_").toUpperCase()+" "+dt});
    return "CREATE TABLE "+table+" (\n  "+cols.join(",\n  ")+"\n);";
  }
  if(tool==="ora-migration-check"){
    const target=$("#target").value;
    const rules=[[/\bNVL\s*\(/ig,"NVL -> review COALESCE semantics"],[/\bDECODE\s*\(/ig,"DECODE -> rewrite as CASE"],[/\bSYSDATE\b/ig,"SYSDATE -> review target date/time equivalent"],[/\bROWNUM\b/ig,"ROWNUM -> rewrite top-N/pagination"],[/\bCONNECT\s+BY\b/ig,"CONNECT BY -> recursive CTE"]];
    for(const [re,msg] of rules)if(re.test(a))out.push(msg+" ("+target+")");
    return out.join("\n")||"No configured migration hotspots found.";
  }
  if(tool==="ora-sql-complexity"){
    const joins=(a.match(/\bJOIN\b/ig)||[]).length,cases=(a.match(/\bCASE\b/ig)||[]).length,aggs=(a.match(/\b(?:COUNT|SUM|AVG|MIN|MAX)\s*\(/ig)||[]).length,win=(a.match(/\bOVER\s*\(/ig)||[]).length,subs=Math.max(0,(a.match(/\bSELECT\b/ig)||[]).length-1);
    const score=uniq(x.read_objects.concat(x.write_objects)).length+joins*2+cases+aggs+win*2+subs*3;
    return "Objects: "+uniq(x.read_objects.concat(x.write_objects)).length+"\nJoins: "+joins+"\nSubqueries: "+subs+"\nCASE: "+cases+"\nAggregates: "+aggs+"\nWindow functions: "+win+"\nStructural score: "+score+"\nBand: "+(score<8?"low":score<18?"moderate":"high");
  }
  if(tool==="ora-call-graph"){
    const pkg=(a.match(/\bPACKAGE\s+BODY\s+([A-Za-z][\w$#]*)/i)||[])[1]||"",rr=[...a.matchAll(/\b(?:PROCEDURE|FUNCTION)\s+([A-Za-z][\w$#]*)\b/ig)];
    rr.forEach((r,i)=>{const caller=(pkg?pkg.toUpperCase()+".":"")+r[1].toUpperCase(),body=a.slice(r.index+r[0].length,rr[i+1]?.index??a.length);let m;const re=/\b([A-Za-z][\w$#]*)\.([A-Za-z][\w$#]*)\s*\(/g;while((m=re.exec(body)))out.push(caller+" -> "+m[1].toUpperCase()+"."+m[2].toUpperCase())});
    return uniq(out).join("\n")||"No qualified calls detected.";
  }
  if(tool==="ora-dead-code"){
    const d=a.match(/\b(?:IS|AS)\b([\s\S]*?)\bBEGIN\b/i);
    if(d){let m;const re=/^\s*([A-Za-z][\w$#]*)\s+(?:CONSTANT\s+)?(?:NUMBER|VARCHAR2|CHAR|DATE|TIMESTAMP|BOOLEAN|PLS_INTEGER|BINARY_INTEGER)\b/img;while((m=re.exec(d[1]))){const re2=new RegExp("\\b"+m[1]+"\\b","ig");if((a.match(re2)||[]).length===1)out.push("UNUSED_VARIABLE: "+m[1])}}
    if(/\bRETURN\s*;[\s\S]+\bEND\b/i.test(a))out.push("UNREACHABLE_CANDIDATE after RETURN");
    if(/\bRAISE\s*;[\s\S]+\bEND\b/i.test(a))out.push("UNREACHABLE_CANDIDATE after RAISE");
    return uniq(out).join("\n")||"No configured dead-code candidates found.";
  }
  if(tool==="ora-schema-explorer"){
    const ts=parseTables(a),deps=x.read_objects.flatMap(r=>x.write_objects.map(w=>r+" -> "+w));
    return "Detected tables: "+ts.length+"\n\n"+ts.map(t=>t.name+"\n"+t.columns.map(c=>"  - "+c.name+" "+c.datatype+(c.nullable?"":" NOT NULL")).join("\n")).join("\n\n")+"\n\nDependencies:\n"+(deps.join("\n")||"-");
  }
  return JSON.stringify(x,null,2);
}
function loadSamples(){
  const tool=$("#tool").value,sel=$("#sampleLevel");sel.innerHTML="";
  (SAMPLES[tool]||[]).forEach((s,i)=>{const o=document.createElement("option");o.value=i;o.textContent=s[0];sel.appendChild(o)});
  loadSelectedSample();
}
function loadSelectedSample(){
  const tool=$("#tool").value,arr=SAMPLES[tool]||[],s=arr[Number($("#sampleLevel").value)||0]||["",""];
  $("#input").value=s[1]||"";$("#input2").value=s[2]||"";
  $("#input2").classList.toggle("hide",tool!=="ora-sql-diff");
  $("#secondLabel").classList.toggle("hide",tool!=="ora-sql-diff");
  $("#targetWrap").classList.toggle("hide",tool!=="ora-migration-check");
  $("#tableWrap").classList.toggle("hide",tool!=="ora-csv-loader");
  runCurrent();
}
function runCurrent(){
  try{$("#output").textContent=processTool($("#tool").value,$("#input").value,$("#input2").value)}
  catch(e){$("#output").textContent="Error: "+String(e&&e.stack||e)}
}
function init(){
  const sel=$("#tool");
  Object.keys(META).forEach(k=>{const o=document.createElement("option");o.value=k;o.textContent=k;sel.appendChild(o)});
  const requested=new URLSearchParams(location.search).get("tool");
  sel.value=META[requested]?requested:"ora-impact";
  function toolChanged(){
    const tool=sel.value;$("#title").textContent=META[tool][0];$("#desc").textContent=META[tool][1];
    history.replaceState(null,"","?tool="+encodeURIComponent(tool));loadSamples();
  }
  sel.addEventListener("change",toolChanged);
  $("#sampleLevel").addEventListener("change",loadSelectedSample);
  $("#sample").addEventListener("click",loadSelectedSample);
  $("#run").addEventListener("click",runCurrent);
  toolChanged();
}
document.addEventListener("DOMContentLoaded",init);
