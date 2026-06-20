import tornado.web
import json
from app.controllers.base import BaseHandler
from app.models.system import DigitalEmployeeRepository


class DigitalEmployeeHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render("admin/digital_employee.html", title="数字员工管理", username=self.current_user)


class DigitalEmployeeApiHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        employees = DigitalEmployeeRepository.get_all()
        self.set_header("Content-Type", "application/json")
        self.write(json.dumps({"code": 0, "data": employees}))

    @tornado.web.authenticated
    def post(self):
        try:
            data = json.loads(self.request.body)
            name = data.get("name")
            if not name:
                self.write(json.dumps({"code": 1, "message": "名称不能为空"}))
                return
            
            employee_id = DigitalEmployeeRepository.create(data)
            self.write(json.dumps({"code": 0, "message": "创建成功", "data": {"id": employee_id}}))
        except Exception as e:
            self.write(json.dumps({"code": 1, "message": str(e)}))

    @tornado.web.authenticated
    def put(self, employee_id):
        try:
            data = json.loads(self.request.body)
            name = data.get("name")
            if not name:
                self.write(json.dumps({"code": 1, "message": "名称不能为空"}))
                return
            
            success = DigitalEmployeeRepository.update(employee_id, data)
            if success:
                self.write(json.dumps({"code": 0, "message": "更新成功"}))
            else:
                self.write(json.dumps({"code": 1, "message": "更新失败，员工不存在"}))
        except Exception as e:
            self.write(json.dumps({"code": 1, "message": str(e)}))

    @tornado.web.authenticated
    def delete(self, employee_id):
        try:
            success = DigitalEmployeeRepository.delete(employee_id)
            if success:
                self.write(json.dumps({"code": 0, "message": "删除成功"}))
            else:
                self.write(json.dumps({"code": 1, "message": "删除失败，员工不存在"}))
        except Exception as e:
            self.write(json.dumps({"code": 1, "message": str(e)}))