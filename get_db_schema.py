import sys
sys.path.append('D:/workspaces/mcp-work/mcp-mysql-client/server/app')
from database import get_db_schema
print(get_db_schema())