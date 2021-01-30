import subprocess
class Python:
    def __init__(self):
        pass

    def process(self,lang):
        proc = subprocess.Popen(['python',"python_run.py"],stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,encoding="utf-8")
        val = proc.communicate()
        return val
        
        
        

    def execute(self,data,language,input_val=[]):
        count = data.count('input()')
        for i in range(count):
            data = data.replace('input()',f'variables_input[{i}]',1)

        var = f'''def Solution(variables_input):
'''
        for i in data.split("\n"):
            var+='\t'
            var+=i
            var+='\n'

        var += f'''
Solution({input_val})
'''
        fp = open('python_run.py','w')
        fp.write(var)
        fp.close()

        result = self.process(language)
        if result[0]:
            result = result[0]
        else:
            result = result[1]
        result = [result,'N/A']
        return result



class Compiler(Python):
    def __init__(self):
        pass

    def execute(self,data,lang,input_val=[]):
        result = ""
        if lang == 'Python':
            result = Python.execute(self,data,lang,input_val)
            return result

        
            