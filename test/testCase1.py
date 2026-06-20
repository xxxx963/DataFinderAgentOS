#单元测试用例

import os
import sys
import time


project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)
sys.path.append(project_root)

if project_root not in sys.path:
    sys.path.append(project_root)

from app.models.db import init_db
from app.models.user import UserRepository

init_db()
username = f"rexyang_{int(time.time())}"
password = "123456"

print("create1:",UserRepository.create_user(username,password))
print("create2:",UserRepository.create_user(username,password))
print("Verity Right:",UserRepository.verify_user(username,password))
print("Verity wrong:",UserRepository.verify_user("admin",password))
print("Verity wrong:",UserRepository.verify_user(username,"123"))
