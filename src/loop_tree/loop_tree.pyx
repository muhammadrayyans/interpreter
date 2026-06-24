class LoopTree:

    def __init__(self, exe_obj: object) -> None:
        self.exe_obj = exe_obj
    
    
    def execute(self):
        self.exe_obj.execute() # type: ignore
        