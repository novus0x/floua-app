########## Modules ##########
import inspect

from sqlalchemy.orm import Session
from typing import Dict, List, Any, Callable

from db.model import User, User_Role

########## Variables ##########


########## Function Caller ##########
class Function_Caller:
    def __init__(self):
        self.available_functions = {}

    def register_function(self, function_name: str, function: Callable, description: str, parameters: Dict):
        self.available_functions[function_name] = {
            "function": function,
            "description": description,
            "parameters": parameters,
            "require_auth": False
        }

    def can_call_function(self, function_name: str, user: User):
        if function_name not in self.available_functions:
            return False
        
        function_info = self.available_functions[function_name]

        if function_info.get("requires_admin") and user.role not in [User_Role.admin]:
            return False
        
        if function_info.get("requires_mod") and user.role not in [User_Role.admin, User_Role.moderator]:
            return False

        return True

    def call_function(self, db: Session, function_name: str, parameters: Dict, user: User):
        if not self.can_call_function(function_name, user):
            return {
                "success": False,
                "error": f"Function '{function_name}' not available or permission denied"
            }

        try:
            function_info = self.available_functions[function_name]
            function = function_info["function"]

            func_params = inspect.available_functions[function_name]
            call_params = {}

            for param_name in func_params:

                if param_name in parameters:
                    call_params[param_name] = parameters[param_name]
                elif param_name == "db":
                    call_params[param_name] = db
                elif param_name == "user_id":
                    call_params[param_name] = user.id

            result = function(**call_params)

            return {
                "success": True,
                "result": result,
                "function_called": function_name
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": f"Error calling function {function_name}: {str(e)}"
            }

    def get_available_functions_info(self, user: User):
        available = []

        for name, info in self.available_functions.items():
            if self.can_call_function(name, user):
                available.append({
                    "name": name,
                    "description": info["description"],
                    "parameters": info["parameters"]
                })

        return available
        
########## Functions ##########
