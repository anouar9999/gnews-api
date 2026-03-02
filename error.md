 From HTTP Request
Error code

ECONNREFUSED

Full message

connect ECONNREFUSED 127.0.0.1:8000
Request

{ "body": { "username": "admin", "password": "admin@00" }, "headers": { "accept": "application/json,text/html,application/xhtml+xml,application/xml,text/*;q=0.9, image/*;q=0.8, */*;q=0.7" }, "method": "POST", "uri": "http://127.0.0.1:8000/api/auth/login/", "gzip": true, "rejectUnauthorized": true, "followRedirect": true, "resolveWithFullResponse": true, "sendCredentialsOnCrossOriginRedirect": false, "followAllRedirects": true, "timeout": 300000, "encoding": null, "json": false, "useStream": true }
 Other info
Item Index

38

Node type

n8n-nodes-base.httpRequest

Node version

4.4 (Latest)

n8n version

2.8.4 (Self Hosted)

Time

2/24/2026, 4:52:24 PM

Stack trace

NodeApiError: The service refused the connection - perhaps it is offline at ExecuteContext.execute (C:\Users\sabir\AppData\Local\npm-cache\_npx\a8a7eec953f1f314\node_modules\n8n-nodes-base\nodes\HttpRequest\V3\HttpRequestV3.node.ts:864:16) at processTicksAndRejections (node:internal/process/task_queues:105:5) at WorkflowExecute.executeNode (C:\Users\sabir\AppData\Local\npm-cache\_npx\a8a7eec953f1f314\node_modules\n8n-core\src\execution-engine\workflow-execute.ts:1039:8) at WorkflowExecute.runNode (C:\Users\sabir\AppData\Local\npm-cache\_npx\a8a7eec953f1f314\node_modules\n8n-core\src\execution-engine\workflow-execute.ts:1218:11) at C:\Users\sabir\AppData\Local\npm-cache\_npx\a8a7eec953f1f314\node_modules\n8n-core\src\execution-engine\workflow-execute.ts:1655:27 at C:\Users\sabir\AppData\Local\npm-cache\_npx\a8a7eec953f1f314\node_modules\n8n-core\src\execution-engine\workflow-execute.ts:2298:11