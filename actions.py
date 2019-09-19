class Action:
    def __init__(self, name: str, commands: list, description: str, action):
        self.name = name
        self.commands = commands
        self.action = action
        self.description = description
        
    def __str__(self):
        return f"{self.__class_.__name__} {self.name}"
        
    def __repr__(self):
        return f"<class {self.__class__.__name__} (name={self.name}, " \
               f"command={self.commands}, action={self.action}, description={self.description})"
               
    def show(self):
        return f"{self.commands} {self.description}"
        
    def called(self, command):
        return command in self.commands
        
    def execute(self):
        return self.action()

