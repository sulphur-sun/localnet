import os


class CLI():

    def ls(self):
        files = ", ".join([f for f in os.listdir(os.getcwd())])
        return f'{os.getcwd()} \n {files}'

    def cd(self, arg):
        if arg == '..':
            os.chdir(arg)
        else:
            os.chdir(arg.strip())